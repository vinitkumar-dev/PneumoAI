from models.prediction import Prediction
from database.db import db
from src.logger import logging


def get_dashboard_summary(user_id):

    logging.info("=" * 50)
    logging.info(f"Dashboard User ID: {user_id}")

    total_predictions = Prediction.query.filter_by(
        user_id=user_id
    ).count()

    logging.info(f"Total Predictions: {total_predictions}")

    avg_confidence = (
        db.session.query(db.func.avg(Prediction.confidence))
        .filter(Prediction.user_id == user_id)
        .scalar()
    ) or 0

    latest = (
        Prediction.query.filter(Prediction.user_id == user_id)
        .order_by(Prediction.created_at.desc())
        .first()
    )

    logging.info(f"Latest Prediction: {latest}")

    return {
        "total_predictions": total_predictions,
        "average_confidence": round(float(avg_confidence), 2),
        "latest_model": latest.model if latest else None,
        "models": 4
    }