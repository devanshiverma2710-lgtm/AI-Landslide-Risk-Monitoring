import shap
import pandas as pd

from app.predictor import model, FEATURES


# ============================================================
# PS26001 — SHAP EXPLAINABILITY
# ============================================================

# Create SHAP TreeExplainer for Random Forest
explainer = shap.TreeExplainer(model)


def explain_prediction(input_data: dict, top_n: int = 5):
    """
    Generate a local SHAP explanation for one prediction.

    Returns the top factors contributing to the
    landslide prediction.
    """

    # Keep exact training feature order
    X = pd.DataFrame(
        [input_data],
        columns=FEATURES
    )

    # Calculate SHAP values
    shap_values = explainer.shap_values(X)

    # Random Forest binary classification:
    # class 1 = landslide
    #
    # SHAP versions/models can return different shapes,
    # so handle both common formats.

    if isinstance(shap_values, list):
        values = shap_values[1][0]
    else:
        values = shap_values[0]

        if hasattr(values, "ndim") and values.ndim > 1:
            if values.shape[-1] == 2:
                values = values[:, 1]
            else:
                values = values.flatten()

    # Build explanation table
    explanation = pd.DataFrame({
        "feature": FEATURES,
        "shap_value": values,
        "feature_value": X.iloc[0].values
    })

    # Positive SHAP = pushes toward landslide
    # Negative SHAP = pushes away from landslide
    explanation["direction"] = explanation["shap_value"].apply(
        lambda x: "increases_risk" if x > 0 else "decreases_risk"
    )

    # Sort by absolute contribution
    explanation["absolute_impact"] = (
        explanation["shap_value"].abs()
    )

    explanation = explanation.sort_values(
        "absolute_impact",
        ascending=False
    ).head(top_n)

    # Convert to JSON-friendly format
    factors = []

    for _, row in explanation.iterrows():

        factors.append({
            "feature": row["feature"],
            "value": round(float(row["feature_value"]), 4),
            "shap_value": round(float(row["shap_value"]), 4),
            "direction": row["direction"]
        })

    return factors