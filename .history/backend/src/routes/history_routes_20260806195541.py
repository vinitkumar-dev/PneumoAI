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

    base_url = request.host_url.rstrip("/")

    return jsonify({

        # =====================================================
        # CORE
        # =====================================================
        "id": prediction.id,
        "created_at": prediction.created_at.isoformat(),

        # =====================================================
        # PATIENT INFORMATION
        # =====================================================
        "patient_name": prediction.patient_name,
        "patient_age": prediction.patient_age,
        "patient_gender": prediction.patient_gender,
        "clinical_notes": prediction.clinical_notes,

        # =====================================================
        # PREDICTION
        # =====================================================
        "prediction": prediction.prediction,
        "confidence": prediction.confidence,
        "model": prediction.model,
        "explanation": prediction.explanation,
        "inference_time": prediction.inference_time,

        # =====================================================
        # IMAGES
        # =====================================================
        "original_image": (
            f"{base_url}/{prediction.image_path}"
            if prediction.image_path else None
        ),

        "gradcam_image": (
            prediction.gradcam_path
            if prediction.gradcam_path and prediction.gradcam_path.startswith("http")
            else (
                f"{base_url}/{prediction.gradcam_path}"
                if prediction.gradcam_path else None
            )
        ),

        "yolo_image": (
            prediction.yolo_path
            if prediction.yolo_path and prediction.yolo_path.startswith("http")
            else (
                f"{base_url}/{prediction.yolo_path}"
                if prediction.yolo_path else None
            )
        ),

        # =====================================================
        # METRICS
        # =====================================================
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