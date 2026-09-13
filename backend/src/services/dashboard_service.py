from models.prediction import Prediction
from database.db import db
from src.logger import logging


def get_dashboard_summary(user_id):

    user_id = int(user_id)

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

    # Confidence is always stored as a 0-100 percentage. Clamp the
    # aggregate defensively so a stale/out-of-range row already sitting
    # in the database can never inflate the dashboard's Mean Confidence
    # Interval beyond 100% (this is what previously produced values like
    # "1639.36%").
    avg_confidence = max(0.0, min(100.0, float(avg_confidence)))

    latest = (
        Prediction.query.filter(Prediction.user_id == user_id)
        .order_by(Prediction.created_at.desc())
        .first()
    )

    logging.info(f"Latest Prediction: {latest}")

    return {
        "total_predictions": total_predictions,
        "average_confidence": round(avg_confidence, 2),
        "latest_model": latest.model if latest else None,
        "models": 1
    }
