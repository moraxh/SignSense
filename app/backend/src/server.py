import json
import asyncio
import websockets
from utils.logger_config import logger
from utils.constants import ServerState, current_state

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

async def predict_websocket_handler(websocket):
  pass

async def start_model_info_websocket():
  server = await websockets.serve(model_info_websocket_handler, '0.0.0.0', 5100)
  await server.wait_closed()

async def start_predicting_websocket():
  server = await websockets.serve(predict_websocket_handler, '0.0.0.0', 5101)
  await server.wait_closed()