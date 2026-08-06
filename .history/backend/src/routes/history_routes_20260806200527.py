from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.services.history_service import get_history
from models.prediction import Prediction
from database.db import db

history_bp = Blueprint(
    "history",
    __name__,
    url_prefix="/api/predictions"
)

# ==========================================================
# PRODUCTION BASE URL
# ==========================================================
BASE_URL = "https://pneumoai-hgh9.onrender.com"


def build_url(path):
    """
    Converts every stored path into a valid production URL.
    Handles:
        - Windows paths
        - localhost URLs
        - relative paths
        - production URLs
    """
    if not path:
        return None

    path = str(path).replace("\\", "/")

    # Remove localhost prefix from old DB records
    path = path.replace("http://127.0.0.1:5000/", "")
    path = path.replace("https://127.0.0.1:5000/", "")

    # Already correct
    if path.startswith(BASE_URL):
        return path

    # Other external URLs
    if path.startswith("http://") or path.startswith("https://"):
        return path

    return f"{BASE_URL}/{path.lstrip('/')}"


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
        "confidence": prediction.confidence,
        "model": prediction.model,
        "explanation": prediction.explanation,
        "inference_time": prediction.inference_time,

        "original_image": build_url(prediction.image_path),
        "gradcam_image": build_url(prediction.gradcam_path),
        "yolo_image": build_url(prediction.yolo_path),

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