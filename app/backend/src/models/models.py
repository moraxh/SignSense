import os
import joblib
import pandas as pd
from utils.logger_config import logger
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from utils.constants import DATASET_FILE, BEST_MODEL_FILE, LABEL_ENCODER_FILE, current_state, ServerState

def train_model():
  model = RandomForestClassifier(n_estimators=100)

  df = pd.read_csv(DATASET_FILE)

  X = df.drop(columns=["label"])
  y = df["label"]

  # Codify labels
  le = LabelEncoder()
  y_encoded = le.fit_transform(y)

  # Split data
  X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

  model.fit(X_train, y_train)
  preds = model.predict(X_test)

  # Get accuracy
  acc = accuracy_score(y_test, preds)

  logger.info(f"Random Forest Accuracy: {acc:.4f}")

  return model, le

def initialize_model():
  current_state['state'] = ServerState.TESTING_MODELS
  if (not os.path.exists(BEST_MODEL_FILE)):
    logger.info("No best model found, training new model...") 
    model, le = train_model()
    joblib.dump(model, BEST_MODEL_FILE)
    joblib.dump(le, LABEL_ENCODER_FILE)
  logger.info("The model is ready to use.")