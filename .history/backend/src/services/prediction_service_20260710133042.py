from database.db import db

from models.prediction import Prediction
from src.logger import logging

def save_prediction(user_id, result, image_path, patient_data=None):
    """
    Saves the execution run analytics and structural patient data matrices 
    to the centralized SQLAlchemy persistence layer.
    """
    try:
        classification = result.get("classification", {})
        patient_data = patient_data or {}

        prediction = Prediction(
            user_id=user_id,
            image_path=image_path,
            gradcam_path=result.get("gradcam_image"),
            yolo_path=result.get("yolo_image"),
            prediction=result.get("prediction"),
            confidence=result.get("confidence"),
            accuracy=classification.get("accuracy"),
            precision=classification.get("precision"),
            recall=classification.get("recall"),
            f1_score=classification.get("f1_score"),
            model=classification.get("model"),
            inference_time=float(result.get("inference_time", 0)),
            explanation=result.get("explanation"),
            
            # New Structural Clinical Properties Mapped from Inbound Client Form
            patient_name=patient_data.get("patient_name"),
            patient_age=int(patient_data.get("patient_age")) if patient_data.get("patient_age") else None,
            patient_gender=patient_data.get("patient_gender"),
            clinical_notes=patient_data.get("clinical_notes")
        )

        db.session.add(prediction)
        db.session.commit()

        logging.info(f"Clinical record and inference telemetry saved successfully. ID={prediction.id}, User={user_id}")
        return prediction

    except Exception as e:
        db.session.rollback()
        logging.exception(f"Transaction aborted. Database rollback executed: {str(e)}")
        raise