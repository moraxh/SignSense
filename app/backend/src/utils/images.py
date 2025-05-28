import cv2
import numpy as np

def get_img_rgb_from_bytes(data):
  img_np = np.frombuffer(data, np.uint8)
  img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
  img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  return img_rgb  