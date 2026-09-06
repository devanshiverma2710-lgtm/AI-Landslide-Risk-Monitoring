from fastapi import FastAPI
from pydantic import BaseModel

from app.predictor import FEATURES, THRESHOLD, predict_landslide
from app.explainer import explain_prediction
from app.risk_engine import calculate_risk


# ============================================================
# PS26001 — LANDSLIDE EARLY WARNING ML API
# ============================================================

app = FastAPI(
    title="PS26001 Landslide Early Warning API",
    description="AI-powered landslide risk prediction service for the North Eastern Region",
    version="1.0.0"
)


# ============================================================
# INPUT SCHEMA
# ============================================================

class LandslideInput(BaseModel):
    elevation_m: float
    slope_deg: float
    aspect_sin: float
    aspect_cos: float
    curvature: float
    rainfall_1d_mm: float
    rainfall_3d_mm: float
    rainfall_7d_mm: float
    max_rainfall_7d_mm: float
    rainfall_anomaly_z: float
    soil_moisture_m3_m3: float
    soil_moisture_anomaly: float
    historical_landslide_density: float
    historical_event_frequency: float
    land_cover_class: float
    ndvi: float
    distance_to_road_km: float
    distance_to_river_km: float
    distance_to_fault_km: float
    population_density: float
    settlement_exposure: float


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/")
def home():
    return {
        "success": True,
        "service": "PS26001 Landslide Early Warning API",
        "model": "Random Forest + Sigmoid Calibration",
        "version": "rf-calibrated-v1.0",
        "status": "online"
    }


# ============================================================
# MODEL INFORMATION
# ============================================================

@app.get("/model-info")
def model_info():
    return {
        "success": True,

        "model": "Random Forest + Sigmoid Calibration",

        "version": "rf-calibrated-v1.0",

        "features": len(FEATURES),

        "threshold": THRESHOLD,

        "calibration": {
            "method": "sigmoid",
            "cv": 5
        },

        "risk_bands": {
            "LOW": "< 0.25",
            "MODERATE": "0.25 - < 0.50",
            "HIGH": "0.50 - < 0.75",
            "CRITICAL": ">= 0.75"
        },

        "risk_engine": {
            "enabled": True,
            "components": [
                "ML probability",
                "susceptibility",
                "trigger",
                "exposure"
            ]
        },

        "explainability": {
            "enabled": True,
            "method": "SHAP",
            "top_factors": 5
        }
    }


# ============================================================
# PREDICTION ENDPOINT
# ============================================================

@app.post("/predict")
def predict(data: LandslideInput):

    # --------------------------------------------------------
    # Convert input to dictionary
    # --------------------------------------------------------

    if hasattr(data, "model_dump"):
        input_data = data.model_dump()
    else:
        input_data = data.dict()

    # --------------------------------------------------------
    # 1. ML prediction
    # --------------------------------------------------------

    result = predict_landslide(input_data)

    ml_probability = result["landslide_probability"]

    # --------------------------------------------------------
    # 2. Risk Engine
    # --------------------------------------------------------

    risk_result = calculate_risk(
        input_data,
        ml_probability
    )

    # --------------------------------------------------------
    # 3. SHAP explanation
    # --------------------------------------------------------

    top_factors = explain_prediction(
        input_data,
        top_n=5
    )

    # --------------------------------------------------------
    # 4. Add Risk Engine results
    # --------------------------------------------------------

    result["susceptibility_score"] = (
        risk_result["susceptibility_score"]
    )

    result["susceptibility_level"] = (
        risk_result["susceptibility_level"]
    )

    result["trigger_score"] = (
        risk_result["trigger_score"]
    )

    result["trigger_level"] = (
        risk_result["trigger_level"]
    )

    result["exposure_score"] = (
        risk_result["exposure_score"]
    )

    result["exposure_level"] = (
        risk_result["exposure_level"]
    )

    result["final_risk_score"] = (
        risk_result["final_risk_score"]
    )

    result["risk_level"] = (
        risk_result["final_risk_level"]
    )

    result["alert_status"] = (
        risk_result["alert_status"]
    )

    # --------------------------------------------------------
    # 5. Warning
    # --------------------------------------------------------

    if risk_result["final_risk_level"] in [
        "HIGH",
        "CRITICAL"
    ]:
        result["warning"] = "LANDSLIDE RISK DETECTED"
    else:
        result["warning"] = "NO IMMEDIATE LANDSLIDE WARNING"

    # --------------------------------------------------------
    # 6. SHAP top factors
    # --------------------------------------------------------

    result["top_factors"] = top_factors

    return result