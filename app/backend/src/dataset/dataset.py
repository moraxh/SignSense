import os
import cv2
import numpy as np
import pandas as pd
from tqdm import tqdm
from utils.logger_config import logger
from dataset.mp_utils import get_hands_processor, get_landmarks_from_img
from utils.constants import DATASET_DIR, DATASET_FILE, LANDMARKS_PAIRS, LANDMARKS_TRIPLETS, LANDMARKS_TIPS, LANDMARKS_PIPS, current_state, ServerState
from dataset.features import normalize_landmarks, pairwise_distances, angles, convex_hull_area, hand_orientation_angle, count_extended_fingers, bounding_box_features

def get_sample_from_points(points):
  points = normalize_landmarks(points)
  dist_feats = pairwise_distances(points, LANDMARKS_PAIRS)
  ang_feats = angles(points, LANDMARKS_TRIPLETS)
  area = convex_hull_area(points)
  angle = hand_orientation_angle(points)
  n_extended = count_extended_fingers(points, LANDMARKS_TIPS, LANDMARKS_PIPS)
  width, height, aspect_ratio = bounding_box_features(points)

  sample = {}

  for i, val in enumerate(dist_feats):
    sample[f"dist_{i}"] = val
  
  for i, val in enumerate(ang_feats):
    sample[f"ang_{i}"] = val

  sample["area"] = area
  sample["angle"] = angle
  sample["width"] = width
  sample["height"] = height
  sample["aspect_ratio"] = aspect_ratio
  sample["n_extended"] = n_extended

  return sample

def create_dataset():
  data = []

  hands_processor = get_hands_processor()

  for label in tqdm(os.listdir(DATASET_DIR), desc="Reading and extracting", unit="label"):
    label_path = os.path.join(DATASET_DIR, label)
    for image in os.listdir(label_path):
      image_path = os.path.join(label_path, image)

      img = cv2.imread(image_path)
      img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
      points = get_landmarks_from_img(hands_processor, img_rgb)

      if len(points) == 0:
        print(f"Warning: No landmarks found in {image_path}. Skipping...")
        continue

      sample = get_sample_from_points(points)
      sample["label"] = label

      data.append(sample)

  df = pd.DataFrame(data)
  df.to_csv(DATASET_FILE, index=False)
    
def initialize_dataset():
  current_state["state"] = ServerState.EXTRACTING_FEATURES
  if not os.path.exists(DATASET_FILE):
    logger.info("Not found dataset file, creating...")
    create_dataset()
  else:
    logger.info("Dataset file found, loading...")