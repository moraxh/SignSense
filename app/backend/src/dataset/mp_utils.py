import mediapipe as mp

def get_hands_processor():
  mp_hands = mp.solutions.hands
  hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
  return hands