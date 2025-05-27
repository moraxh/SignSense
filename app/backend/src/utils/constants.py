import os
from enum import Enum

class ServerState(str, Enum):
  LOADING_SERVER = "Loading server"
  EXTRACTING_FEATURES = "Extracting features"
  TESTING_MODELS = "Testing models"
  READY = "Ready"

current_state = {
  'state': ServerState.LOADING_SERVER,
}

CACHE_DIR = "./cache"
DATASET_DIR = "./dataset" 
BEST_MODEL_FILE = f"{CACHE_DIR}/best_model.pkl"
LABEL_ENCODER_FILE = f"{CACHE_DIR}/label_encoder.pkl"

DATASET_FILE = f"{CACHE_DIR}/dataset.csv"

LANDMARKS_PAIRS = [
    # Tip-to-tip (neighboring fingers)
    (4, 8), (8, 12), (12, 16), (16, 20),

    # Wrist to each fingertip
    (0, 4), (0, 8), (0, 12), (0, 16), (0, 20),

    # Tip to base of the same finger (to capture bending)
    (4, 3), (8, 6), (12, 10), (16, 14), (20, 18),

    # Thumb to other fingertips (e.g., letters like G, L)
    (4, 12), (4, 16), (4, 20),

    # Palm width: base-to-base
    (5, 17), (2, 20)
]
LANDMARKS_TRIPLETS = [
    # Index finger
    (5, 6, 7), (6, 7, 8),

    # Middle finger
    (9, 10, 11), (10, 11, 12),

    # Ring finger
    (13, 14, 15), (14, 15, 16),

    # Pinky finger
    (17, 18, 19), (18, 19, 20),

    # Thumb
    (1, 2, 3), (2, 3, 4),

    # Palm structure
    (0, 5, 9), (0, 9, 13), (0, 13, 17)
]
LANDMARKS_TIPS = [4, 8, 12, 16, 20]
LANDMARKS_PIPS = [3, 6, 10, 14, 18]

os.makedirs(CACHE_DIR, exist_ok=True)