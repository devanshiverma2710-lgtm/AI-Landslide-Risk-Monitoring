from datetime import datetime, timezone

from fastapi import FastAPI,HTTPException
from pydantic import BaseModel, Field

from app.predictor import (
    FEATURES,
    THRESHOLD,
    MODEL_NAME,
    MODEL_VERSION,
    RISK_ENGINE_VERSION,
    predict_landslide
)

from app.explainer import explain_prediction
from app.risk_engine import calculate_risk
from app.forecast_engine import calculate_forecast_risk


# ============================================================
# PS26001 — LANDSLIDE EARLY WARNING ML API
# ============================================================

app = FastAPI(
    title="PS26001 Landslide Early Warning API",
    description=(
        "AI-powered landslide risk prediction service "
        "for the North Eastern Region"
    ),
    version="1.0.0"
)


# ============================================================
# CURRENT-RISK INPUT SCHEMA
# ============================================================

class LandslideInput(BaseModel):

    elevation_m: float = Field(..., ge=-500, le=9000)
    slope_deg: float = Field(..., ge=0, le=90)

    aspect_sin: float
    aspect_cos: float
    curvature: float

    rainfall_1d_mm: float = Field(..., ge=0)
    rainfall_3d_mm: float = Field(..., ge=0)
    rainfall_7d_mm: float = Field(..., ge=0)
    max_rainfall_7d_mm: float = Field(..., ge=0)
    rainfall_anomaly_z: float

    soil_moisture_m3_m3: float = Field(..., ge=0, le=1)
    soil_moisture_anomaly: float

    historical_landslide_density: float
    historical_event_frequency: float

    land_cover_class: float
    ndvi: float = Field(..., ge=-1, le=1)

    distance_to_road_km: float = Field(..., ge=0)
    distance_to_river_km: float = Field(..., ge=0)
    distance_to_fault_km: float = Field(..., ge=0)
    population_density: float = Field(..., ge=0)
    settlement_exposure: float = Field(..., ge=0, le=1)


# ============================================================
# FORECAST INPUT SCHEMA
# ============================================================

class ForecastInput(LandslideInput):

    forecast_rainfall_mm: list[float] = Field(
        ...,
        min_length=1,
        max_length=7,
        description=(
            "Forecast rainfall values in mm for "
            "the next 1 to 7 forecast periods."
        )
    )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/")
def home():

    return {
        "success": True,
        "service": "PS26001 Landslide Early Warning API",
        "model": MODEL_NAME,
        "version": MODEL_VERSION,
        "status": "online"
    }


# ============================================================
# MODEL INFORMATION
# ============================================================

@app.get("/model-info")
def model_info():

    return {
        "success": True,

        "model": MODEL_NAME,

        "version": MODEL_VERSION,

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
            "version": RISK_ENGINE_VERSION,
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
# CURRENT-RISK PREDICTION
# ============================================================

@app.post("/predict")
def predict(data: LandslideInput):
    prediction_timestamp = datetime.now(timezone.utc).isoformat()

    try:
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
        # 4. Add risk-engine results
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
            result["warning"] = (
                "LANDSLIDE RISK DETECTED"
            )
        else:
            result["warning"] = (
                "NO IMMEDIATE LANDSLIDE WARNING"
            )

        # --------------------------------------------------------
        # 6. SHAP + timestamp
        # --------------------------------------------------------

        result["top_factors"] = top_factors
        result["prediction_timestamp"] = prediction_timestamp

        return result

    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail=str(e)
        )


# ============================================================
# FORECAST-BASED EARLY WARNING
# ============================================================

@app.post("/forecast-risk")
def forecast_risk(data: ForecastInput):
    try:
        if hasattr(data, "model_dump"):
            input_data = data.model_dump()
        else:
            input_data = data.dict()

        forecast_rainfall = input_data.pop("forecast_rainfall_mm")

        current_prediction = predict_landslide(input_data)

        ml_probability = current_prediction["landslide_probability"]

        result = calculate_forecast_risk(
            current_data=input_data,
            ml_probability=ml_probability,
            forecast_rainfall_mm=forecast_rainfall
        )

        result["forecast_periods"] = len(forecast_rainfall)
        result["model"] = MODEL_NAME
        result["model_version"] = MODEL_VERSION
        result["risk_engine_version"] = RISK_ENGINE_VERSION

        return result

    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail=str(e)
        )