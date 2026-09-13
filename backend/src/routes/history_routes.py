from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from config.config import Config
from src.services.history_service import get_history
from models.prediction import Prediction
from database.db import db

history_bp = Blueprint(
    "history",
    __name__,
    url_prefix="/api/predictions"
)


def build_url(path):
    """
    Converts every stored (relative) path into a valid absolute URL for
    the CURRENT request's host. Falls back to the configured BASE_URL
    env var when set (useful behind a proxy/CDN), otherwise uses
    `request.host_url`, which is correct for both local development and
    production automatically.
    """
    if not path:
        return None

    path = str(path).replace("\\", "/")

    # Already an absolute URL (e.g. legacy DB rows) — leave as-is.
    if path.startswith("http://") or path.startswith("https://"):
        return path

    base_url = Config.BASE_URL or request.host_url.rstrip("/")

    return f"{base_url}/{path.lstrip('/')}"


def clamp_confidence(value):
    try:
        value = float(value or 0)
    except (TypeError, ValueError):
        return 0.0
    return max(0.0, min(100.0, value))


# ==========================================================
# HISTORY
# ==========================================================
@history_bp.route("/history", methods=["GET"])
@jwt_required()
def history():

    user_id = int(get_jwt_identity())

    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "", type=str)
    prediction_filter = request.args.get("prediction", "", type=str)

    data = get_history(
        user_id=user_id,
        page=page,
        limit=10,
        search=search,
        prediction_filter=prediction_filter
    )

    # Convert relative image paths to absolute URLs for the frontend.
    for item in data.get("items", []):
        item["image_path"] = build_url(item.get("image_path"))

    return jsonify(data), 200


# ==========================================================
# SINGLE PREDICTION
# ==========================================================
@history_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_prediction(id):

    user_id = int(get_jwt_identity())

    prediction = Prediction.query.filter_by(
        id=id,
        user_id=user_id
    ).first()

    if prediction is None:
        return jsonify({
            "status": "error",
            "message": "Prediction not found"
        }), 404

    return jsonify({

        "id": prediction.id,
        "created_at": (
            prediction.created_at.isoformat()
            if prediction.created_at
            else None
        ),

        "patient_name": prediction.patient_name,
        "patient_age": prediction.patient_age,
        "patient_gender": prediction.patient_gender,
        "clinical_notes": prediction.clinical_notes,

        "prediction": prediction.prediction,
        "confidence": clamp_confidence(prediction.confidence),
        "model": prediction.model,
        "explanation": prediction.explanation,
        "inference_time": prediction.inference_time,

        "original_image": build_url(prediction.image_path),

        "accuracy": prediction.accuracy,
        "precision": prediction.precision,
        "recall": prediction.recall,
        "f1_score": prediction.f1_score,

        "classification": {
            "accuracy": prediction.accuracy,
            "precision": prediction.precision,
            "recall": prediction.recall,
            "f1_score": prediction.f1_score,
            "model": prediction.model
        }

    }), 200


# ==========================================================
# DELETE
# ==========================================================
@history_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_prediction(id):

    user_id = int(get_jwt_identity())

    prediction = Prediction.query.filter_by(
        id=id,
        user_id=user_id
    ).first()

    if prediction is None:
        return jsonify({
            "status": "error",
            "message": "Prediction not found"
        }), 404

    db.session.delete(prediction)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Prediction deleted successfully",
        "id": id
    }), 200
