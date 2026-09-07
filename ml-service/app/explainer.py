# ============================================================
# PS26001 — SHAP MODEL EXPLAINER
# Works with calibrated Random Forest
# ============================================================

import shap
import pandas as pd
import numpy as np

from app.predictor import model, FEATURES


# ============================================================
# CREATE SHAP EXPLAINERS
# ============================================================

def get_base_estimators():

    """
    Extract the underlying Random Forest estimators
    from CalibratedClassifierCV.

    For the final calibrated model, sklearn stores
    multiple fitted Random Forest estimators inside
    calibrated_classifiers_.
    """

    # CalibratedClassifierCV
    if hasattr(model, "calibrated_classifiers_"):

        estimators = []

        for calibrated_classifier in model.calibrated_classifiers_:

            if hasattr(calibrated_classifier, "estimator"):

                estimators.append(
                    calibrated_classifier.estimator
                )

        if len(estimators) > 0:
            return estimators

    # Normal Random Forest fallback
    return [model]


# ============================================================
# SHAP EXPLANATION
# ============================================================

def explain_prediction(input_data, top_n=5):

    """
    Generate SHAP explanations for one prediction.

    For a calibrated Random Forest, SHAP is calculated
    using the underlying Random Forest estimators.

    The SHAP values are averaged across the calibrated
    ensemble.
    """

    # --------------------------------------------------------
    # Prepare input
    # --------------------------------------------------------

    X = pd.DataFrame(
        [input_data],
        columns=FEATURES
    )

    # Make sure feature order is correct
    X = X[FEATURES]

    # --------------------------------------------------------
    # Get underlying RF estimators
    # --------------------------------------------------------

    estimators = get_base_estimators()

    all_shap_values = []

    # --------------------------------------------------------
    # Calculate SHAP for each estimator
    # --------------------------------------------------------

    for estimator in estimators:

        explainer = shap.TreeExplainer(
            estimator
        )

        shap_values = explainer.shap_values(
            X
        )

        # ----------------------------------------------------
        # SHAP output handling
        # ----------------------------------------------------

        # Older SHAP versions:
        # list[class 0 values, class 1 values]

        if isinstance(shap_values, list):

            values = shap_values[1][0]

        else:

            shap_values = np.asarray(
                shap_values
            )

            # Possible shape:
            # (1, features)
            if shap_values.ndim == 2:

                values = shap_values[0]

            # Possible shape:
            # (1, features, classes)
            elif shap_values.ndim == 3:

                values = shap_values[0, :, 1]

            else:

                values = shap_values.flatten()

        all_shap_values.append(
            np.asarray(values)
        )

    # --------------------------------------------------------
    # Average SHAP contribution across RF estimators
    # --------------------------------------------------------

    mean_shap_values = np.mean(
        all_shap_values,
        axis=0
    )

    # --------------------------------------------------------
    # Build explanation
    # --------------------------------------------------------

    explanation = []

    for feature, value, shap_value in zip(
        FEATURES,
        X.iloc[0].values,
        mean_shap_values
    ):

        if shap_value > 0:

            direction = "increases_risk"

        elif shap_value < 0:

            direction = "decreases_risk"

        else:

            direction = "neutral"

        explanation.append({
            "feature": feature,
            "value": float(value),
            "shap_value": float(shap_value),
            "direction": direction
        })

    # --------------------------------------------------------
    # Sort by absolute SHAP impact
    # --------------------------------------------------------

    explanation = sorted(
        explanation,
        key=lambda x: abs(
            x["shap_value"]
        ),
        reverse=True
    )

    # --------------------------------------------------------
    # Return top factors
    # --------------------------------------------------------

    return explanation[:top_n]