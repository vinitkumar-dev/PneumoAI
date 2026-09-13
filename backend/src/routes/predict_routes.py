import os
import gc
import torch
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from config.config import Config
from src.pipeline.predict_pipeline import PredictionPipeline
from src.services.file_service import save_upload
from src.services.prediction_service import save_prediction
from src.utils.response_builder import build_response
from src.logger import logging

predict_bp = Blueprint("predict", __name__)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@predict_bp.route("/predict", methods=["POST"])
@jwt_required()
def predict():
    return process_prediction()


def process_prediction():
    pipeline = None
    try:
        user_id = int(get_jwt_identity())

        file_key = "image" if "image" in request.files else "file" if "file" in request.files else None
        if not file_key:
            return jsonify({"status": "error", "message": "No file uploaded."}), 400

        file = request.files[file_key]
        if file.filename == "":
            return jsonify({"status": "error", "message": "Empty filename."}), 400

        raw_age = request.form.get("patient_age")
        patient_age = int(raw_age) if raw_age and raw_age.isdigit() else None

        patient_data = {
            "patient_name": request.form.get("patient_name") or "Unknown",
            "patient_age": patient_age,
            "patient_gender": request.form.get("patient_gender") or "Other",
            "clinical_notes": request.form.get("clinical_notes") or ""
        }

        logging.info("Saving upload...")
        filename, image_path = save_upload(file, UPLOAD_FOLDER)
        logging.info("Upload saved.")

        # Instantiate the classifier per-request to avoid keeping the
        # PyTorch model resident in RAM permanently (Render free tier
        # is memory constrained).
        logging.info("Initializing PredictionPipeline...")
        pipeline = PredictionPipeline()

        logging.info("Running predict() inside torch.no_grad()...")

        # Disable gradient computation to save ~60% RAM during inference
        with torch.no_grad():
            result = pipeline.predict(image_path)

        logging.info("Prediction finished.")

        # Prefer an explicit BASE_URL env var (useful when behind a proxy/CDN
        # or when the public URL differs from the internal request host),
        # otherwise fall back to the current request's own host. This makes
        # image URLs correct in local dev, staging, AND production without
        # any code changes.
        base_url = Config.BASE_URL or request.host_url.rstrip("/")

        response = build_response(
            prediction_result=result,
            filename=filename,
            base_url=base_url
        )

        saved_prediction = save_prediction(
            user_id=user_id,
            result=response,
            image_path=image_path,
            patient_data=patient_data
        )

        response["id"] = saved_prediction.id
        response["patient_name"] = saved_prediction.patient_name
        response["patient_age"] = saved_prediction.patient_age
        response["patient_gender"] = saved_prediction.patient_gender
        response["clinical_notes"] = saved_prediction.clinical_notes
        response["created_at"] = (
            saved_prediction.created_at.isoformat()
            if saved_prediction.created_at
            else None
        )

        return jsonify(response), 200

    except Exception as e:
        logging.exception(e)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    finally:
        # Aggressive memory cleanup after every execution (success or failure)
        del pipeline
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        gc.collect()
