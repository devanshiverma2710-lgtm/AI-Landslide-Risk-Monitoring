# ============================================================
# PS26001 — FORECAST-BASED EARLY WARNING ENGINE
# ============================================================

from copy import deepcopy

from app.risk_engine import (
    calculate_trigger,
    calculate_susceptibility,
    calculate_exposure,
    get_risk_level,
    get_trigger_level,
)


# ------------------------------------------------------------
# FORECAST RAINFALL PROCESSING
# ------------------------------------------------------------

def calculate_forecast_rainfall(forecast_rainfall_mm):
    """
    Calculate forecast rainfall accumulation.

    Expected input:
        List of forecast rainfall values in mm.

    Example:
        [40, 60, 80, 50, 30]

    Returns:
        Total forecast rainfall.
    """

    if not forecast_rainfall_mm:
        raise ValueError("forecast_rainfall_mm cannot be empty")

    if any(value < 0 for value in forecast_rainfall_mm):
        raise ValueError(
            "Forecast rainfall values cannot be negative"
        )

    total = sum(forecast_rainfall_mm)

    return round(float(total), 2)


# ------------------------------------------------------------
# PROJECTED TRIGGER
# ------------------------------------------------------------

def calculate_projected_trigger(
    current_data,
    forecast_rainfall_mm
):
    """
    Estimate future triggering conditions using
    current conditions plus forecast rainfall.

    The existing trigger engine is retained.
    Forecast rainfall updates the rainfall components.
    """

    if not forecast_rainfall_mm:
        raise ValueError(
            "At least one forecast rainfall value is required"
        )

    data = deepcopy(current_data)

    # Forecast accumulation
    forecast_total = calculate_forecast_rainfall(
        forecast_rainfall_mm
    )

    # --------------------------------------------------------
    # Forecast rainfall windows
    # --------------------------------------------------------

    # Next forecast period
    forecast_1d = float(
        forecast_rainfall_mm[0]
    )

    # Sum available forecast values for 3-day window
    forecast_3d = float(
        sum(forecast_rainfall_mm[:3])
    )

    # Sum available forecast values for 7-day window
    forecast_7d = float(
        sum(forecast_rainfall_mm[:7])
    )

    # Maximum rainfall expected in the forecast period
    forecast_max = float(
        max(forecast_rainfall_mm)
    )

    # --------------------------------------------------------
    # Combine current + forecast rainfall
    # --------------------------------------------------------

    projected_1d = max(
        data["rainfall_1d_mm"],
        forecast_1d
    )

    projected_3d = (
        data["rainfall_3d_mm"]
        + forecast_3d
    )

    projected_7d = (
        data["rainfall_7d_mm"]
        + forecast_7d
    )

    projected_max_7d = max(
        data["max_rainfall_7d_mm"],
        forecast_max
    )

    # --------------------------------------------------------
    # Update projected rainfall values
    # --------------------------------------------------------

    data["rainfall_1d_mm"] = projected_1d
    data["rainfall_3d_mm"] = projected_3d
    data["rainfall_7d_mm"] = projected_7d
    data["max_rainfall_7d_mm"] = projected_max_7d

    projected_trigger = calculate_trigger(data)

    return {
        "forecast_total_rainfall_mm": round(
            forecast_total,
            2
        ),

        "projected_rainfall_1d_mm": round(
            projected_1d,
            2
        ),

        "projected_rainfall_3d_mm": round(
            projected_3d,
            2
        ),

        "projected_rainfall_7d_mm": round(
            projected_7d,
            2
        ),

        "projected_max_rainfall_7d_mm": round(
            projected_max_7d,
            2
        ),

        "projected_trigger_score": round(
            projected_trigger,
            4
        ),

        "projected_trigger_level":
            get_trigger_level(projected_trigger),

        "_projected_data": data
    }


# ------------------------------------------------------------
# PROJECTED RISK
# ------------------------------------------------------------

def calculate_forecast_risk(
    current_data,
    ml_probability,
    forecast_rainfall_mm
):
    """
    Calculate projected risk using forecast rainfall.

    ML probability remains the current model signal.
    Forecast rainfall modifies the future trigger condition.
    Susceptibility and exposure remain unchanged.
    """

    forecast_result = calculate_projected_trigger(
        current_data,
        forecast_rainfall_mm
    )

    projected_data = forecast_result["_projected_data"]

    susceptibility = calculate_susceptibility(
        projected_data
    )

    exposure = calculate_exposure(
        projected_data
    )

    projected_trigger = forecast_result[
        "projected_trigger_score"
    ]

    # --------------------------------------------------------
    # Final projected risk
    # --------------------------------------------------------

    final_score = (
        0.50 * ml_probability
        + 0.20 * susceptibility
        + 0.20 * projected_trigger
        + 0.10 * exposure
    )

    final_score = max(
        0.0,
        min(1.0, float(final_score))
    )

    risk_level = get_risk_level(
        final_score
    )

    # --------------------------------------------------------
    # Warning generation
    # --------------------------------------------------------

    if risk_level == "CRITICAL":
        warning = (
            "CRITICAL FORECAST: "
            "HIGH LANDSLIDE RISK EXPECTED"
        )

    elif risk_level == "HIGH":
        warning = (
            "EARLY WARNING: "
            "ELEVATED LANDSLIDE RISK EXPECTED"
        )

    elif risk_level == "MODERATE":
        warning = (
            "WATCH: "
            "LANDSLIDE RISK MAY INCREASE"
        )

    else:
        warning = (
            "LOW FORECAST RISK: "
            "NO SIGNIFICANT INCREASE EXPECTED"
        )

    # Remove internal data before API response
    forecast_result.pop(
        "_projected_data",
        None
    )

    return {
        "success": True,

        "ml_probability": round(
            float(ml_probability),
            4
        ),

        "current_risk_note":
            "ML probability represents the current-condition model signal.",

        **forecast_result,

        "projected_susceptibility_score": round(
            susceptibility,
            4
        ),

        "projected_susceptibility_level":
            get_risk_level(susceptibility),

        "projected_exposure_score": round(
            exposure,
            4
        ),

        "projected_exposure_level":
            get_risk_level(exposure),

        "projected_risk_score": round(
            final_score,
            4
        ),

        "projected_risk_level":
            risk_level,

        "early_warning": risk_level in [
            "HIGH",
            "CRITICAL"
        ],

        "warning": warning
    }