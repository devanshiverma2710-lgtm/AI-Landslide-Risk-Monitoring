import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR
    / "model"
    / "PS26001_Final_Calibrated_RandomForest_Model.pkl"
)

FEATURE_PATH = (
    BASE_DIR
    / "config"
    / "feature_list.txt"
)

CONFIG_PATH = (
    BASE_DIR
    / "config"
    / "PS26001_Final_Calibrated_Model_Config.json"
)


# ============================================================
# MODEL METADATA
# ============================================================

MODEL_NAME = "Random Forest + Sigmoid Calibration"
MODEL_VERSION = "rf-calibrated-v1.0"
RISK_ENGINE_VERSION = "risk-engine-v1.0"

THRESHOLD = 0.50


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
# LOAD MODEL CONFIG
# ============================================================

with open(CONFIG_PATH, "r", encoding="utf-8") as file:
    CONFIG = json.load(file)


# ============================================================
# FEATURE VALIDATION
# ============================================================

def validate_features(input_data: dict):
    """
    Validate that all required ML features are present.

    Returns:
        list of missing features
    """

    missing_features = [
        feature
        for feature in FEATURES
        if feature not in input_data
    ]

    return missing_features


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
    """
    Run calibrated Random Forest landslide prediction.

    The model receives exactly the 21 training features
    in the original training order.
    """

    # --------------------------------------------------------
    # Validate required features
    # --------------------------------------------------------

    missing_features = validate_features(
        input_data
    )

    if missing_features:
        raise ValueError(
            "Missing required features: "
            + ", ".join(missing_features)
        )

    # --------------------------------------------------------
    # Create dataframe using exact feature order
    # --------------------------------------------------------

    X = pd.DataFrame(
        [
            {
                feature: input_data[feature]
                for feature in FEATURES
            }
        ]
    )

    # --------------------------------------------------------
    # Validate numeric values
    # --------------------------------------------------------

    if X.isnull().any().any():
        raise ValueError(
            "Input contains null or missing values"
        )
    if not np.isfinite(X.to_numpy(dtype=float)).all():
       raise ValueError("Input contains non-finite values")

    # --------------------------------------------------------
    # Predict probability
    # --------------------------------------------------------

    probability = float(
        model.predict_proba(X)[0, 1]
    )

    # --------------------------------------------------------
    # Apply operational threshold
    # --------------------------------------------------------

    prediction = int(
        probability >= THRESHOLD
    )

    # --------------------------------------------------------
    # Determine risk level
    # --------------------------------------------------------

    risk_level = get_risk_level(
        probability
    )

    # --------------------------------------------------------
    # Warning
    # --------------------------------------------------------

    if prediction == 1:
        warning = (
            "LANDSLIDE RISK DETECTED"
        )
    else:
        warning = (
            "NO IMMEDIATE LANDSLIDE RISK DETECTED"
        )

    return {
        "success": True,

        "landslide_probability": round(
            probability,
            4
        ),

        "landslide_prediction":
            prediction,

        "risk_level":
            risk_level,

        "warning":
            warning,

        "model":
            MODEL_NAME,

        "model_version":
            MODEL_VERSION,

        "risk_engine_version":
            RISK_ENGINE_VERSION
    }