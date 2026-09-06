# PS26001 — ML Service Integration Guide

## Purpose

This is the AI/ML service for SIH 2026 PS26001 — AI-Powered Landslide Early Warning & Risk Monitoring System for the North Eastern Region (NER).

The service provides:
- Current landslide probability prediction
- Risk severity
- Susceptibility, trigger and exposure scores
- Final risk score
- SHAP explanations
- Forecast-based early warning
- REST APIs for backend/frontend integration

The service is independent from the main backend. The backend communicates with it through HTTP REST APIs.

## Folder Structure

```text
ml-service/
├── app/
│   ├── main.py
│   ├── predictor.py
│   ├── explainer.py
│   ├── risk_engine.py
│   └── forecast_engine.py
├── config/
│   ├── feature_list.txt
│   ├── model_config.json
│   └── PS26001_Final_Calibrated_Model_Config.json
├── model/
│   ├── PS26001_Final_RandomForest_Model.pkl
│   └── PS26001_Final_Calibrated_RandomForest_Model.pkl
└── requirements.txt
```

| File | Responsibility |
|---|---|
| `main.py` | FastAPI app and endpoints |
| `predictor.py` | Loads model and performs prediction |
| `risk_engine.py` | Susceptibility, trigger, exposure, final risk and alerts |
| `explainer.py` | SHAP explanations |
| `forecast_engine.py` | Forecast rainfall and projected risk |
| `feature_list.txt` | Exact model feature order |
| `PS26001_Final_Calibrated_Model_Config.json` | Model/calibration configuration |
| `PS26001_Final_Calibrated_RandomForest_Model.pkl` | Current production model |

## Run the Service

From repository root:

```powershell
.\.venv\Scripts\Activate.ps1
cd ml-service
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Service:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

## Requirements

```text
fastapi
uvicorn[standard]
pydantic
pandas
numpy
scikit-learn==1.6.1
joblib
shap
requests
```

Use scikit-learn 1.6.1 for model compatibility.

## Production Model

```text
Model: Random Forest + Sigmoid Calibration
Version: rf-calibrated-v1.0
Risk Engine: risk-engine-v1.0
Trees: 500
Class weighting: balanced
Random state: 42
Calibration: Sigmoid
Calibration CV: 5
```

The calibrated Random Forest is the model used by `/predict`.

## Model Features

The model expects exactly 21 features:

```text
elevation_m
slope_deg
aspect_sin
aspect_cos
curvature
rainfall_1d_mm
rainfall_3d_mm
rainfall_7d_mm
max_rainfall_7d_mm
rainfall_anomaly_z
soil_moisture_m3_m3
soil_moisture_anomaly
historical_landslide_density
historical_event_frequency
land_cover_class
ndvi
distance_to_road_km
distance_to_river_km
distance_to_fault_km
population_density
settlement_exposure
```

### Feature groups

**Terrain:** elevation, slope, aspect sin/cos, curvature

**Rainfall:** 1-day, 3-day, 7-day rainfall, maximum 7-day rainfall, rainfall anomaly

**Environmental:** soil moisture, soil moisture anomaly, land cover, NDVI

**Historical:** historical landslide density, historical event frequency

**Exposure/infrastructure:** road distance, river distance, fault distance, population density, settlement exposure

Latitude, longitude, state and district are primarily used for mapping, grouping and GIS operations rather than direct model prediction.

## Data Rules

Historical features must contain only information available before the prediction timestamp.

Do not calculate historical features using future landslide events.

Synthetic/demo rows must not be presented as real observations.

Prototype-estimated environmental fields must not be described as live sensor/satellite measurements.

# REST API

## 1. GET /

Basic service health.

Example:

```json
{
  "success": true,
  "service": "PS26001 Landslide Early Warning API",
  "model": "Random Forest + Sigmoid Calibration",
  "version": "rf-calibrated-v1.0",
  "status": "online"
}
```

## 2. GET /model-info

Returns model, calibration, risk-engine and explainability information.

Example:

```json
{
  "success": true,
  "model": "Random Forest + Sigmoid Calibration",
  "version": "rf-calibrated-v1.0",
  "features": 21,
  "threshold": 0.5,
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
    "version": "risk-engine-v1.0",
    "enabled": true,
    "components": [
      "ML probability",
      "susceptibility",
      "trigger",
      "exposure"
    ]
  },
  "explainability": {
    "enabled": true,
    "method": "SHAP",
    "top_factors": 5
  }
}
```

## 3. POST /predict

Predicts current-condition landslide risk.

### Request

```json
{
  "elevation_m": 1200,
  "slope_deg": 42,
  "aspect_sin": 0.7,
  "aspect_cos": 0.7,
  "curvature": 0.3,
  "rainfall_1d_mm": 150,
  "rainfall_3d_mm": 350,
  "rainfall_7d_mm": 550,
  "max_rainfall_7d_mm": 220,
  "rainfall_anomaly_z": 2.2,
  "soil_moisture_m3_m3": 0.75,
  "soil_moisture_anomaly": 2.5,
  "historical_landslide_density": 250,
  "historical_event_frequency": 18,
  "land_cover_class": 10,
  "ndvi": 0.30,
  "distance_to_road_km": 0.5,
  "distance_to_river_km": 0.8,
  "distance_to_fault_km": 5,
  "population_density": 300,
  "settlement_exposure": 0.8
}
```

### Response

```json
{
  "success": true,
  "landslide_probability": 0.7249,
  "landslide_prediction": 1,
  "risk_level": "HIGH",
  "warning": "LANDSLIDE RISK DETECTED",
  "model": "Random Forest + Sigmoid Calibration",
  "model_version": "rf-calibrated-v1.0",
  "risk_engine_version": "risk-engine-v1.0",
  "susceptibility_score": 0.58,
  "susceptibility_level": "HIGH",
  "trigger_score": 0.7602,
  "trigger_level": "EXTREME",
  "exposure_score": 0.673,
  "exposure_level": "HIGH",
  "final_risk_score": 0.6978,
  "alert_status": "WATCH",
  "top_factors": [
    {
      "feature": "elevation_m",
      "value": 1200,
      "shap_value": 0.1351,
      "direction": "increases_risk"
    },
    {
      "feature": "slope_deg",
      "value": 42,
      "shap_value": 0.0464,
      "direction": "increases_risk"
    }
  ],
  "prediction_timestamp": "2026-09-06T17:05:06+00:00"
}
```

### Important output fields

`landslide_probability`: calibrated ML probability from 0 to 1.

`landslide_prediction`:

```text
probability >= 0.50 -> 1
probability < 0.50  -> 0
```

`risk_level`: final operational risk severity.

`final_risk_score`: combined risk score from the risk engine.

## 4. POST /forecast-risk

Estimates future risk using supplied forecast rainfall.

Difference:

```text
/predict
    = current-condition ML prediction

/forecast-risk
    = projected risk if supplied forecast rainfall occurs
```

### Request

```json
{
  "elevation_m": 1200,
  "slope_deg": 42,
  "aspect_sin": 0.7,
  "aspect_cos": 0.7,
  "curvature": 0.3,
  "rainfall_1d_mm": 150,
  "rainfall_3d_mm": 350,
  "rainfall_7d_mm": 550,
  "max_rainfall_7d_mm": 220,
  "rainfall_anomaly_z": 2.2,
  "soil_moisture_m3_m3": 0.75,
  "soil_moisture_anomaly": 2.5,
  "historical_landslide_density": 250,
  "historical_event_frequency": 18,
  "land_cover_class": 10,
  "ndvi": 0.30,
  "distance_to_road_km": 0.5,
  "distance_to_river_km": 0.8,
  "distance_to_fault_km": 5,
  "population_density": 300,
  "settlement_exposure": 0.8,
  "forecast_rainfall_mm": [150, 120, 100, 80, 60]
}
```

`forecast_rainfall_mm` accepts 1 to 7 forecast periods.

### Response

```json
{
  "success": true,
  "ml_probability": 0.7249,
  "current_risk_note": "ML probability represents the current-condition model signal.",
  "forecast_total_rainfall_mm": 510,
  "projected_rainfall_1d_mm": 150,
  "projected_rainfall_3d_mm": 720,
  "projected_rainfall_7d_mm": 1060,
  "projected_max_rainfall_7d_mm": 220,
  "projected_trigger_score": 0.8588,
  "projected_trigger_level": "EXTREME",
  "projected_susceptibility_score": 0.58,
  "projected_susceptibility_level": "HIGH",
  "projected_exposure_score": 0.673,
  "projected_exposure_level": "HIGH",
  "projected_risk_score": 0.7175,
  "projected_risk_level": "HIGH",
  "early_warning": true,
  "warning": "EARLY WARNING: ELEVATED LANDSLIDE RISK EXPECTED",
  "forecast_periods": 5,
  "model": "Random Forest + Sigmoid Calibration",
  "model_version": "rf-calibrated-v1.0",
  "risk_engine_version": "risk-engine-v1.0"
}
```

The forecast engine is a prototype projection, not a hydrological simulation.

The ML service does not currently fetch live IMD/weather data itself. Recommended flow:

```text
Weather/IMD Forecast API
        |
        v
Main Backend / Data Pipeline
        |
        v
POST /forecast-risk
        |
        v
Projected Risk / Early Warning
```

# Risk Engine

## Risk Bands

| Score | Level |
|---|---|
| `< 0.25` | LOW |
| `0.25 - < 0.50` | MODERATE |
| `0.50 - < 0.75` | HIGH |
| `>= 0.75` | CRITICAL |

These are prototype operational thresholds and are configurable engineering thresholds, not scientifically validated disaster thresholds.

## Final Risk Formula

```text
Final Risk =
    0.50 × ML Probability
  + 0.20 × Susceptibility
  + 0.20 × Trigger
  + 0.10 × Exposure
```

The final score is clipped to 0–1.

## Susceptibility

Represents relatively persistent location vulnerability.

Components:

```text
Elevation
Slope
Curvature
Historical landslide density
Historical event frequency
NDVI
```

Prototype weights:

```text
Elevation                 0.25
Slope                     0.25
Curvature                 0.10
Historical density        0.20
Historical frequency      0.15
1 - NDVI                  0.05
```

## Trigger

Represents short-term conditions that may increase landslide likelihood.

Components:

```text
Rainfall 1 day
Rainfall 3 days
Rainfall 7 days
Maximum rainfall
Rainfall anomaly
Soil moisture
Soil moisture anomaly
```

Prototype weights:

```text
Rainfall 1d              0.10
Rainfall 3d              0.15
Rainfall 7d              0.25
Maximum rainfall 7d      0.15
Rainfall anomaly         0.15
Soil moisture            0.10
Soil moisture anomaly    0.10
```

Trigger levels:

| Score | Level |
|---|---|
| `< 0.25` | LOW |
| `0.25 - < 0.50` | MODERATE |
| `0.50 - < 0.75` | HIGH |
| `>= 0.75` | EXTREME |

## Exposure

Represents people/infrastructure that may be affected.

Components:

```text
Population density
Settlement exposure
Road proximity
River proximity
```

Prototype weights:

```text
Population density     0.35
Settlement exposure    0.30
Road proximity         0.20
River proximity        0.15
```

## Alert Logic

```text
ALERT
if final risk = CRITICAL
AND ML probability >= 0.75
AND trigger = HIGH or EXTREME
```

```text
WATCH
if final risk = HIGH
AND ML probability >= 0.50
AND trigger = HIGH or EXTREME
```

Otherwise:

```text
NO_ALERT
```

The main backend should persist alerts and handle notifications.

# SHAP Explainability

`POST /predict` returns local SHAP explanations.

Example:

```json
{
  "feature": "elevation_m",
  "value": 1200,
  "shap_value": 0.1351,
  "direction": "increases_risk"
}
```

`increases_risk` means that feature contributed toward the positive landslide prediction for that input.

`decreases_risk` means it contributed in the opposite direction.

SHAP explains model behavior/reliance and is not proof of causation.

# Input Validation

Current validation includes:

| Field | Constraint |
|---|---|
| `elevation_m` | -500 to 9000 |
| `slope_deg` | 0 to 90 |
| Rainfall values | >= 0 |
| `soil_moisture_m3_m3` | 0 to 1 |
| `ndvi` | -1 to 1 |
| Distances | >= 0 |
| `population_density` | >= 0 |
| `settlement_exposure` | 0 to 1 |

Missing/invalid/null values return HTTP 422.

Non-finite numeric values are rejected.

# Backend Integration

The main backend should call `/predict` for current risk and `/forecast-risk` for forecast risk.

```text
Sensor / Weather / GIS Data
          |
          v
      Main Backend
          |
          +---- POST /predict --------+
          |                           |
          +---- POST /forecast-risk --+
                                      |
                                      v
                              FastAPI ML Service
                                      |
                         +------------+------------+
                         |            |            |
                         v            v            v
                       Model      Risk Engine     SHAP
                         |            |            |
                         +------------+------------+
                                      |
                                      v
                              Prediction + Risk
                                      |
                    +-----------------+----------------+
                    |                 |                |
                    v                 v                v
                Database           Alerts           Frontend/GIS
```

The backend should not reproduce the ML logic and the frontend should not load the `.pkl` model.

# Recommended Database Fields

Store at least:

```text
location_id
latitude
longitude
prediction_timestamp
input_data_timestamp
landslide_probability
landslide_prediction
risk_level
final_risk_score
susceptibility_score
trigger_score
exposure_score
alert_status
model_version
risk_engine_version
top_factors
```

Keep historical predictions for audit/history instead of overwriting them.

# GIS Integration

The backend/GIS layer can associate predictions with:

```text
latitude
longitude
state
district
roads
rivers
settlements
infrastructure
administrative boundaries
```

A GIS marker can display:

```text
Location
Risk Level
ML Probability
Final Risk Score
Susceptibility
Trigger
Exposure
Rainfall
Top Risk Factors
Prediction Timestamp
```

Recommended architecture:

```text
ML Service
    |
    v
Main Backend
    |
    v
PostgreSQL / PostGIS
    |
    v
Risk Map API
    |
    v
React / GIS Frontend
```

# Alerts

The ML service returns:

```text
NO_ALERT
WATCH
ALERT
```

The main backend is responsible for:

- Alert persistence
- Alert acknowledgement
- SMS/email/push notification integration
- Alert history
- Escalation workflow
- Authority dashboard

# Offline and Low-Network Support

Offline functionality belongs mainly to frontend/backend.

The frontend can cache:

```text
Latest risk map
Critical locations
Last predictions
Emergency contacts
GIS information
```

When connectivity returns, cached data can synchronize with the backend.

# Multilingual Notifications

The ML service returns structured values such as:

```json
{
  "risk_level": "CRITICAL",
  "alert_status": "ALERT"
}
```

The backend/notification layer can convert these into English, Hindi and regional-language messages.

# Validation Summary

The model was evaluated with:

```text
Random stratified validation
Date-grouped validation
Spatial validation
```

Real benchmark data:

```text
1,184 rows
592 positive
592 negative
```

Approximate real-only random holdout results:

| Model | Accuracy | F1 | ROC-AUC |
|---|---:|---:|---:|
| Random Forest | 0.776 | 0.782 | 0.876 |
| HistGradientBoosting | 0.806 | 0.805 | 0.883 |
| XGBoost | 0.798 | 0.797 | 0.881 |
| Logistic Regression | 0.768 | 0.764 | 0.792 |

The production artifact is the calibrated Random Forest.

Random validation should not be presented as guaranteed future performance.

A temporal experiment trained on 2007–2009 and tested on 2024–2025 showed substantially weaker performance, demonstrating temporal distribution shift.

Calibration using sigmoid calibration improved probability-quality metrics such as Brier score and log loss. It should still be revalidated when the production data distribution changes.

# Important Limitations

This is an engineering prototype, not a certified disaster-warning system.

1. The real benchmark dataset is relatively small.
2. Temporal distribution shift exists.
3. Some environmental fields are prototype estimates rather than live measurements.
4. Forecast projection is simplified.
5. Risk thresholds are prototype operational thresholds.
6. Risk-engine weights are engineering choices, not learned physical relationships.
7. Historical features require strict timestamp-aware construction.
8. Larger real-world sensor, weather, satellite and landslide datasets are required for operational deployment.
9. Probability calibration should be revalidated on future production data.

# Data Provenance

Use these descriptions correctly:

**Real data**
```text
Real benchmark / historical data
```

**Prototype-estimated fields**
```text
Prototype-estimated environmental features
```

**Synthetic rows**
```text
Synthetic / prototype data
```

Never present synthetic data as real sensor or satellite observations.

# Current ML Status

Completed:

- [x] Real-data ML dataset
- [x] 21-feature schema
- [x] Random Forest model
- [x] Sigmoid probability calibration
- [x] Prediction API
- [x] Input validation
- [x] Risk severity
- [x] Susceptibility score
- [x] Trigger score
- [x] Exposure score
- [x] Final risk score
- [x] Alert status
- [x] SHAP explanations
- [x] Forecast rainfall endpoint
- [x] Projected trigger
- [x] Projected risk
- [x] Early warning flag
- [x] Model versioning
- [x] Risk-engine versioning
- [x] Swagger documentation
- [x] Service health endpoint

# Main Backend / Frontend Responsibilities

## Backend

- [ ] Start/connect to ML service
- [ ] Call `/predict`
- [ ] Call `/forecast-risk`
- [ ] Store predictions
- [ ] Store timestamps and model versions
- [ ] Store alerts
- [ ] Alert acknowledgement
- [ ] Connect weather/forecast APIs
- [ ] Connect sensor data
- [ ] Connect GIS data
- [ ] Expose risk-map/location/history APIs

## Database / GIS

- [ ] PostgreSQL
- [ ] PostGIS
- [ ] Administrative boundaries
- [ ] Historical landslides
- [ ] Roads
- [ ] Rivers
- [ ] Settlements
- [ ] Infrastructure
- [ ] Predictions
- [ ] Alerts
- [ ] Rainfall/forecast records

## Frontend

- [ ] Dashboard
- [ ] Interactive GIS risk map
- [ ] Location details
- [ ] Current risk
- [ ] Forecast risk
- [ ] Rainfall charts
- [ ] SHAP/top-factor display
- [ ] Alert dashboard
- [ ] Historical analytics
- [ ] Reports
- [ ] Offline/PWA support
- [ ] Multilingual notifications

# Recommended Integration Order

```text
1. Start ML service
2. Test GET /
3. Test GET /model-info
4. Test POST /predict
5. Integrate /predict with backend
6. Store prediction + risk
7. Display risk on frontend
8. Connect GIS location data
9. Integrate /forecast-risk
10. Implement alert workflow
11. Connect live weather/sensor sources
12. Add offline and multilingual functionality
```

# Quick Testing

Start:

```powershell
uvicorn app.main:app --reload
```

Health:

```text
GET http://127.0.0.1:8000/
```

Model info:

```text
GET http://127.0.0.1:8000/model-info
```

Prediction:

```text
POST http://127.0.0.1:8000/predict
```

Forecast:

```text
POST http://127.0.0.1:8000/forecast-risk
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

# Integration Contract

### Current prediction input

21 validated terrain, rainfall, environmental, historical and exposure features.

### Current prediction output

```text
ML probability
ML prediction
Risk level
Final risk score
Susceptibility
Trigger
Exposure
Alert status
SHAP factors
Model version
Prediction timestamp
```

### Forecast input

```text
Current 21 features
+
1–7 forecast rainfall values
```

### Forecast output

```text
Projected rainfall
Projected trigger
Projected susceptibility
Projected exposure
Projected risk
Early warning
Warning message
Model version
Risk engine version
```

# Final Architecture

```text
                    DATA SOURCES
                         |
       +-----------------+------------------+
       |                 |                  |
    Rainfall          Sensors          GIS/Satellite
       |                 |                  |
       +-----------------+------------------+
                         |
                         v
                   MAIN BACKEND
                         |
             +-----------+-----------+
             |                       |
             v                       v
       Current Data            Forecast Data
             |                       |
             v                       v
        POST /predict       POST /forecast-risk
             |                       |
             +-----------+-----------+
                         |
                         v
                 FASTAPI ML SERVICE
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
      ML Model       Risk Engine      SHAP
          |              |              |
          +--------------+--------------+
                         |
                         v
                Prediction + Risk
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
       Database       Alerts          GIS Map
          |              |              |
          +--------------+--------------+
                         |
                         v
                      FRONTEND
                         |
             +-----------+-----------+
             |                       |
             v                       v
       Authorities              Communities
```

# Final Handoff

The ML service is an independent FastAPI component of PS26001.

The main backend should call the ML service rather than reproduce the ML logic.

Primary endpoints:

```text
GET  /
GET  /model-info
POST /predict
POST /forecast-risk
```

The current service provides:

```text
Current ML prediction
+
Calibrated probability
+
Risk severity
+
Susceptibility
+
Trigger
+
Exposure
+
Final risk score
+
Alert status
+
SHAP explanation
+
Forecast-based early warning
```

Live IMD/weather feeds, real-time sensors, GIS storage, notification delivery, offline synchronization and multilingual UI are platform-level integrations handled by the corresponding backend/frontend/data components.
