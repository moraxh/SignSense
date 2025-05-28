import numpy as np
import mediapipe as mp

def get_hands_processor():
  mp_hands = mp.solutions.hands
  hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
  return hands

def get_landmarks_from_img(hands_processor, img_rgb):
  results = hands_processor.process(img_rgb)

  points = []

  if results.multi_hand_landmarks:
    for hand in results.multi_hand_landmarks:
      h, w, _ = img_rgb.shape
      for lm in hand.landmark:
        x = lm.x * w
        y = lm.y * h
        points.append([x, y])
      
      points = np.array(points)

  return points