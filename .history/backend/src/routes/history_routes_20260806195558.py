from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.services.history_service import get_history
from models.prediction import Prediction
from database.db import db


# =========================
# BLUEPRINT
# =========================
history_bp = Blueprint(
    "history",
    __name__,
    url_prefix="/api/predictions"
)

# =========================
# HISTORY LIST
# =========================
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


# =========================
# GET SINGLE PREDICTION (VIEW)
# =========================
@history_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_prediction(id):

    user_id = int(get_jwt_identity())

    prediction = Prediction.query.filter_by(
        id=id,
        user_id=user_id
    ).first()

    if not prediction:
        return jsonify({
            "status": "error",
            "message": "Prediction not found"
        }), 404

    # ==========================================================
    # ALWAYS USE PRODUCTION URL
    # ==========================================================
    base_url = "https://pneumoai-hgh9.onrender.com"

    def build_url(path):
        if not path:
            return None

        path = path.replace("\\", "/")

        if path.startswith("http://") or path.startswith("https://"):
            return path

        return f"{base_url}/{path.lstrip('/')}"

    return jsonify({

        "id": prediction.id,
        "created_at": prediction.created_at.isoformat(),

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

# =========================
# DELETE PREDICTION
# =========================
@history_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_prediction(id):

    user_id = int(get_jwt_identity())

    prediction = Prediction.query.filter_by(
        id=id,
        user_id=user_id
    ).first()

    if not prediction:
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