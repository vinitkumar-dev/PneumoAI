from database.db import db
from models.prediction import Prediction
from src.logger import logging


def to_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def to_int(value):
    try:
        if value is None or value == "":
            return None
        return int(value)
    except (TypeError, ValueError):
        return None


def clamp_confidence(value):
    """
    Confidence is always stored as a 0-100 percentage. Clamping here is
    the last line of defense before the value ever reaches the database,
    so a bad upstream value (e.g. legacy double-scaled data) can never
    corrupt aggregates like the dashboard's Mean Confidence Interval.
    """
    value = to_float(value, default=0.0)
    return max(0.0, min(100.0, value))


def save_prediction(user_id, result, image_path, patient_data=None):
    """
    Save prediction details into the database.
    """

    try:

        patient_data = patient_data or {}

        classification = result.get("classification", {})

        prediction = Prediction(

            user_id=user_id,

            # -----------------------------
            # Image Path (Relative)
            # -----------------------------
            image_path=str(image_path).replace("\\", "/"),

            # -----------------------------
            # Prediction
            # -----------------------------
            prediction=result.get("prediction"),

            confidence=clamp_confidence(
                result.get("confidence")
            ),

            model=classification.get("model"),

            accuracy=clamp_confidence(
                classification.get("accuracy")
            ),

            precision=clamp_confidence(
                classification.get("precision")
            ),

            recall=clamp_confidence(
                classification.get("recall")
            ),

            f1_score=clamp_confidence(
                classification.get("f1_score")
            ),

            inference_time=to_float(
                result.get("inference_time")
            ),

            explanation=result.get("explanation"),

            # -----------------------------
            # Patient Details
            # -----------------------------
            patient_name=patient_data.get("patient_name"),

            patient_age=to_int(
                patient_data.get("patient_age")
            ),

            patient_gender=patient_data.get("patient_gender"),

            clinical_notes=patient_data.get("clinical_notes"),
        )

        db.session.add(prediction)
        db.session.commit()

        logging.info(
            f"Prediction saved successfully. "
            f"Prediction ID={prediction.id}, "
            f"User ID={user_id}"
        )

        return prediction

    except Exception as e:

        db.session.rollback()

        logging.exception(
            "Database transaction failed while saving prediction."
        )

        raise e
