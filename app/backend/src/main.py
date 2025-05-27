import asyncio
from utils.logger_config import logger  
from models.models import initialize_model
from dataset.dataset import initialize_dataset
from utils.constants import ServerState, current_state
from server import start_model_info_websocket, start_predicting_websocket

def initialize():
  initialize_dataset()
  initialize_model()
  current_state["state"] = ServerState.READY

async def run_main():
  asyncio.create_task(start_model_info_websocket())
  asyncio.create_task(start_predicting_websocket())

  await asyncio.to_thread(initialize)

  await asyncio.Future()  # Run forever

def main():
  asyncio.run(run_main())

if __name__ == "__main__":
  main()