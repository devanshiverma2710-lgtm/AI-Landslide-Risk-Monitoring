# ============================================================
# PS26001 — LANDSLIDE RISK ENGINE
# ============================================================

import numpy as np


# ------------------------------------------------------------
# NORMALIZATION
# ------------------------------------------------------------

def normalize(value, minimum, maximum):
    """
    Normalize a value to 0-1.

    NOTE:
    The min/max values used here are prototype reference ranges.
    In production, these should be replaced by validated
    domain-specific thresholds or statistics.
    """

    if maximum == minimum:
        return 0.0

    score = (value - minimum) / (maximum - minimum)

    return float(np.clip(score, 0.0, 1.0))


# ------------------------------------------------------------
# SUSCEPTIBILITY
# ------------------------------------------------------------

def calculate_susceptibility(data):
    """
    Estimates background susceptibility based on
    terrain, historical and environmental characteristics.
    """

    elevation = normalize(
        data["elevation_m"],
        0,
        2000
    )

    slope = normalize(
        data["slope_deg"],
        0,
        60
    )

    curvature = normalize(
        abs(data["curvature"]),
        0,
        1
    )

    historical_density = normalize(
        data["historical_landslide_density"],
        0,
        500
    )

    historical_frequency = normalize(
        data["historical_event_frequency"],
        0,
        30
    )

    ndvi_score = normalize(
        1 - data["ndvi"],
        0,
        1
    )

    score = (
        0.25 * elevation
        + 0.25 * slope
        + 0.10 * curvature
        + 0.20 * historical_density
        + 0.15 * historical_frequency
        + 0.05 * ndvi_score
    )

    return float(np.clip(score, 0.0, 1.0))


# ------------------------------------------------------------
# TRIGGER
# ------------------------------------------------------------

def calculate_trigger(data):
    """
    Estimates current triggering conditions using
    rainfall and soil-moisture indicators.
    """

    rainfall_1d = normalize(
        data["rainfall_1d_mm"],
        0,
        200
    )

    rainfall_3d = normalize(
        data["rainfall_3d_mm"],
        0,
        500
    )

    rainfall_7d = normalize(
        data["rainfall_7d_mm"],
        0,
        700
    )

    max_rainfall_7d = normalize(
        data["max_rainfall_7d_mm"],
        0,
        300
    )

    rainfall_anomaly = normalize(
        data["rainfall_anomaly_z"],
        -3,
        3
    )

    soil_moisture = normalize(
        data["soil_moisture_m3_m3"],
        0,
        1
    )

    soil_moisture_anomaly = normalize(
        data["soil_moisture_anomaly"],
        -3,
        5
    )

    score = (
        0.10 * rainfall_1d
        + 0.15 * rainfall_3d
        + 0.25 * rainfall_7d
        + 0.15 * max_rainfall_7d
        + 0.15 * rainfall_anomaly
        + 0.10 * soil_moisture
        + 0.10 * soil_moisture_anomaly
    )

    return float(np.clip(score, 0.0, 1.0))


# ------------------------------------------------------------
# EXPOSURE
# ------------------------------------------------------------

def calculate_exposure(data):
    """
    Estimates human/infrastructure exposure.
    """

    population = normalize(
        data["population_density"],
        0,
        1000
    )

    settlement = normalize(
        data["settlement_exposure"],
        0,
        1
    )

    road = 1 - normalize(
        data["distance_to_road_km"],
        0,
        10
    )

    river = 1 - normalize(
        data["distance_to_river_km"],
        0,
        10
    )

    score = (
        0.35 * population
        + 0.30 * settlement
        + 0.20 * road
        + 0.15 * river
    )

    return float(np.clip(score, 0.0, 1.0))


# ------------------------------------------------------------
# RISK LEVEL
# ------------------------------------------------------------

def get_risk_level(score):

    if score < 0.25:
        return "LOW"

    elif score < 0.50:
        return "MODERATE"

    elif score < 0.75:
        return "HIGH"

    else:
        return "CRITICAL"


# ------------------------------------------------------------
# TRIGGER LEVEL
# ------------------------------------------------------------

def get_trigger_level(score):

    if score < 0.25:
        return "LOW"

    elif score < 0.50:
        return "MODERATE"

    elif score < 0.75:
        return "HIGH"

    else:
        return "EXTREME"


# ------------------------------------------------------------
# SUSCEPTIBILITY LEVEL
# ------------------------------------------------------------

def get_susceptibility_level(score):

    if score < 0.25:
        return "LOW"

    elif score < 0.50:
        return "MODERATE"

    elif score < 0.75:
        return "HIGH"

    else:
        return "VERY HIGH"


# ------------------------------------------------------------
# EXPOSURE LEVEL
# ------------------------------------------------------------

def get_exposure_level(score):

    if score < 0.25:
        return "LOW"

    elif score < 0.50:
        return "MODERATE"

    elif score < 0.75:
        return "HIGH"

    else:
        return "VERY HIGH"


# ------------------------------------------------------------
# ALERT DECISION
# ------------------------------------------------------------

def get_alert_status(
    final_risk_score,
    ml_probability,
    trigger_score
):

    risk_level = get_risk_level(final_risk_score)
    trigger_level = get_trigger_level(trigger_score)

    # Critical emergency alert
    if (
        risk_level == "CRITICAL"
        and ml_probability >= 0.75
        and trigger_level in ["HIGH", "EXTREME"]
    ):
        return "ALERT"

    # High-risk monitoring
    elif (
        risk_level == "HIGH"
        and ml_probability >= 0.50
        and trigger_level in ["HIGH", "EXTREME"]
    ):
        return "WATCH"

    return "NO_ALERT"


# ------------------------------------------------------------
# COMPLETE RISK ENGINE
# ------------------------------------------------------------

def calculate_risk(data, ml_probability):
    """
    Combines:

        ML probability
        + susceptibility
        + trigger
        + exposure

    into an operational final risk score.
    """

    susceptibility = calculate_susceptibility(data)

    trigger = calculate_trigger(data)

    exposure = calculate_exposure(data)

    # ML remains the primary signal
    final_score = (
        0.50 * ml_probability
        + 0.20 * susceptibility
        + 0.20 * trigger
        + 0.10 * exposure
    )

    final_score = float(
        np.clip(final_score, 0.0, 1.0)
    )

    risk_level = get_risk_level(
        final_score
    )

    trigger_level = get_trigger_level(
        trigger
    )

    susceptibility_level = get_susceptibility_level(
        susceptibility
    )

    exposure_level = get_exposure_level(
        exposure
    )

    alert_status = get_alert_status(
        final_score,
        ml_probability,
        trigger
    )

    return {
        "susceptibility_score": round(
            susceptibility,
            4
        ),

        "susceptibility_level":
            susceptibility_level,

        "trigger_score": round(
            trigger,
            4
        ),

        "trigger_level":
            trigger_level,

        "exposure_score": round(
            exposure,
            4
        ),

        "exposure_level":
            exposure_level,

        "final_risk_score": round(
            final_score,
            4
        ),

        "final_risk_level":
            risk_level,

        "alert_status":
            alert_status
    }