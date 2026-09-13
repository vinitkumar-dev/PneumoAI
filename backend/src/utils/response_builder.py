CLASSIFICATION_INFO = {
    "model": "EfficientNet-B0",
    "accuracy": 90.54,
    "auc_roc": 96.80,
    "f1_score": 90.34,
    "precision": 90.93,
    "recall": 90.54,
}


def clamp_percent(value, default=0.0):
    """
    Clamps any numeric value to the valid 0-100 percentage range.

    This is the safety net that stops corrupted / out-of-range confidence
    values (e.g. from legacy double-scaled data) from ever reaching the
    database or the API response.
    """
    try:
        value = float(value)
    except (TypeError, ValueError):
        return default

    if value != value:  # NaN check
        return default

    return max(0.0, min(100.0, value))


def build_response(prediction_result, filename, base_url):
    """
    Converts the raw output of PredictionPipeline.predict() into the JSON
    payload returned by /predict.

    NOTE: `prediction_result["confidence"]`, `["normal_probability"]` and
    `["pneumonia_probability"]` coming from PredictionPipeline are ALREADY
    on a 0-100 percentage scale — they must NOT be multiplied by 100 again
    here. They are also clamped defensively so a value can never exceed
    100% or drop below 0%, regardless of upstream rounding artifacts.
    """

    base_url = base_url.rstrip("/")

    original_image = f"{base_url}/uploads/{filename}"

    confidence = clamp_percent(prediction_result.get("confidence"))
    normal_probability = clamp_percent(prediction_result.get("normal_probability"))
    pneumonia_probability = clamp_percent(prediction_result.get("pneumonia_probability"))

    explanation = (
        f"The EfficientNet-B0 model classified this chest X-ray as "
        f"{prediction_result['prediction']} with "
        f"{confidence}% confidence."
    )

    return {
        "status": "success",

        "prediction": prediction_result["prediction"],

        "confidence": confidence,

        "normal_probability": normal_probability,

        "pneumonia_probability": pneumonia_probability,

        "original_image": original_image,

        "classification": CLASSIFICATION_INFO,

        "inference_time": prediction_result.get("inference_time", 0),
        "timestamp": prediction_result.get("timestamp"),
        "explanation": explanation,
    }
