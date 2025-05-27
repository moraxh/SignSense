import numpy as np
from scipy.spatial import ConvexHull

def normalize_landmarks(points):
  center = points[0]
  points = points - center

  scale = np.linalg.norm(points[0] - points[9])
  if scale != 0:
    points = points / scale
  
  return points

def pairwise_distances(landmarks, pairs):
  dists = []
  for i, j in pairs:
    dists.append(np.linalg.norm(landmarks[i] - landmarks[j]))
  return np.array(dists)

def angles(landmarks, triples):
  angs = []
  for i, j, k in triples:
    v1 = landmarks[i] - landmarks[j]
    v2 = landmarks[k] - landmarks[j]
    # cosθ = (v1·v2) / (‖v1‖‖v2‖)
    cosang = np.dot(v1, v2) / (np.linalg.norm(v1)*np.linalg.norm(v2) + 1e-8)
    θ = np.degrees(np.arccos(np.clip(cosang, -1, 1)))
    angs.append(θ)
  return np.array(angs)

def convex_hull_area(landmarks):
  hull = ConvexHull(landmarks)
  return hull.area

def count_extended_fingers(landmarks, finger_tips, finger_pips):
  wrist = landmarks[0]
  count = 0
  for tip, pip in zip(finger_tips, finger_pips):
    d_tip = np.linalg.norm(landmarks[tip] - wrist)
    d_pip = np.linalg.norm(landmarks[pip] - wrist)
    if d_tip > d_pip:
      count += 1
  return count

def bounding_box_features(landmarks):
  x = [pt[0] for pt in landmarks]
  y = [pt[1] for pt in landmarks]
  width = max(x) - min(x)
  height = max(y) - min(y)
  aspect_ratio = width / (height + 1e-6)
  return width, height, aspect_ratio

def hand_orientation_angle(landmarks):
  wrist = np.array(landmarks[0])
  middle_base = np.array(landmarks[9])
  vec = middle_base - wrist
  angle = np.arctan2(vec[1], vec[0])
  return angle