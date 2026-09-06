import json
from pathlib import Path

import joblib
import pandas as pd


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "model" / "PS26001_Final_RandomForest_Model.pkl"
FEATURE_PATH = BASE_DIR / "config" / "feature_list.txt"
CONFIG_PATH = BASE_DIR / "config" / "model_config.json"


# ============================================================
# LOAD MODEL
# ============================================================

model = joblib.load(MODEL_PATH)


# ============================================================
# LOAD FEATURE LIST
# ============================================================

with open(FEATURE_PATH, "r", encoding="utf-8") as file:
    FEATURES = [
        line.strip()
        for line in file
        if line.strip()
    ]


# ============================================================
# LOAD CONFIG
# ============================================================

with open(CONFIG_PATH, "r", encoding="utf-8") as file:
    CONFIG = json.load(file)


# The validated operational threshold for the prototype
THRESHOLD = 0.50


# ============================================================
# RISK LEVEL
# ============================================================

def get_risk_level(probability: float) -> str:

    if probability < 0.25:
        return "LOW"

    elif probability < 0.50:
        return "MODERATE"

    elif probability < 0.75:
        return "HIGH"

    else:
        return "CRITICAL"


# ============================================================
# PREDICTION
# ============================================================

def predict_landslide(input_data: dict) -> dict:

    # Create dataframe using the exact training feature order
    X = pd.DataFrame(
        [input_data],
        columns=FEATURES
    )

    # Predict landslide probability
    probability = float(
        model.predict_proba(X)[0, 1]
    )

    # Apply operational threshold
    prediction = int(
        probability >= THRESHOLD
    )

    # Determine risk level
    risk_level = get_risk_level(probability)

    # Warning message
    if prediction == 1:
        warning = "LANDSLIDE RISK DETECTED"
    else:
        warning = "NO IMMEDIATE LANDSLIDE RISK DETECTED"

    return {
        "success": True,
        "landslide_probability": round(probability, 4),
        "landslide_prediction": prediction,
        "risk_level": risk_level,
        "warning": warning
    }