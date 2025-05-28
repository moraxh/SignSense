import io
import json
import joblib
import asyncio
import websockets
import pandas as pd
from PIL import Image
from utils.logger_config import logger
from utils.images import get_img_rgb_from_bytes
from dataset.dataset import get_sample_from_points
from dataset.mp_utils import get_hands_processor, get_landmarks_from_img
from utils.constants import ServerState, current_state, DATASET_FILE, BEST_MODEL_FILE, LABEL_ENCODER_FILE

async def model_info_websocket_handler(websocket):
  update_interval = 1
  try:
    while True:
      await asyncio.sleep(update_interval)

      # If the server is ready, update the interval to 5 seconds
      if current_state['state'] == ServerState.READY:
        update_interval = 5
      
      await websocket.send(json.dumps(current_state))
  except websockets.exceptions.ConnectionClosed:
    await websocket.close()
  except Exception as e:
    logger.error(f"Error in model_info_websocket_handler: {e}")
    await websocket.close()
  pass

async def wait_for_model_ready(interval=2):
  while not current_state['state'] == ServerState.READY:
    await asyncio.sleep(interval)

async def predict_websocket_handler(websocket):
  try: 
    logger.info("Waiting for model to be ready...")
    await wait_for_model_ready()
    logger.info("Model is ready, starting prediction handler...")
    hands_processor = get_hands_processor()
    columns_reference = pd.read_csv(DATASET_FILE, nrows=0).columns.tolist()
    if 'label' in columns_reference:
      columns_reference.remove('label')
    model = joblib.load(BEST_MODEL_FILE)
    le = joblib.load(LABEL_ENCODER_FILE)
    while True:
      try:
        data = await websocket.recv()

        if (isinstance(data, bytes)):
          img_rgb = get_img_rgb_from_bytes(data)

          if img_rgb is None:
            logger.error("Failed to decode image data.")
            await websocket.send(json.dumps({"predict": ""}))
            continue

          points = get_landmarks_from_img(hands_processor, img_rgb)

          if len(points) == 0:  
            await websocket.send(json.dumps({"predict": ""}))
            continue

          sample = get_sample_from_points(points)
          sample_df = pd.DataFrame([sample])
          sample_df = sample_df.reindex(columns=columns_reference, fill_value=0)
          pred = model.predict(sample_df)[0]
          pred_label = le.inverse_transform([pred])[0]
          logger.info(f"Prediction made: {pred_label}")
          await websocket.send(json.dumps({"predict": pred_label}))
        else:
          logger.error(f"Received unexpected data type: {type(data)}")
      except Exception as e:
        logger.error(f"Error receiving data: {e}")
        await websocket.close()
        return
  except websockets.exceptions.ConnectionClosed:
    await websocket.close()
  except Exception as e:
    logger.error(f"Error in predict_websocket_handler: {e}")
    await websocket.close()

async def start_model_info_websocket():
  server = await websockets.serve(model_info_websocket_handler, '0.0.0.0', 5100)
  await server.wait_closed()

async def start_predicting_websocket():
  server = await websockets.serve(predict_websocket_handler, '0.0.0.0', 5101)
  await server.wait_closed()