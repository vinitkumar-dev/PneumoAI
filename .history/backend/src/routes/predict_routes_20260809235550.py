# from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required, get_jwt_identity

# from src.pipeline.explain_pipeline import ExplainPipeline
# from src.services.file_service import save_upload
# from src.services.prediction_service import save_prediction
# from src.utils.response_builder import build_response
# from src.logger import logging

# predict_bp = Blueprint("predict", __name__)

# explainer = ExplainPipeline()
# UPLOAD_FOLDER = "static/uploads"


# @predict_bp.route("/predict", methods=["POST"])
# @jwt_required()
# def predict():
#     try:
#         user_id = int(get_jwt_identity())

#         # -------------------------
#         # Validate uploaded file
#         # -------------------------
#         file_key = None

#         if "image" in request.files:
#             file_key = "image"
#         elif "file" in request.files:
#             file_key = "file"

#         if not file_key:
#             return jsonify({
#                 "status": "error",
#                 "message": "No file uploaded."
#             }), 400

#         file = request.files[file_key]

#         if file.filename == "":
#             return jsonify({
#                 "status": "error",
#                 "message": "Empty filename."
#             }), 400

#         # -------------------------
#         # Patient Information
#         # -------------------------
#         patient_data = {
#             "patient_name": request.form.get("patient_name"),
#             "patient_age": request.form.get("patient_age"),
#             "patient_gender": request.form.get("patient_gender"),
#             "clinical_notes": request.form.get("clinical_notes")
#         }

#         # -------------------------
#         # Save uploaded image
#         # -------------------------
#         filename, image_path = save_upload(file, UPLOAD_FOLDER)

#         logging.info(f"Image saved : {image_path}")

#         # -------------------------
#         # Run AI Model
#         # -------------------------
#         result = explainer.explain(image_path)

#         base_url = request.host_url.rstrip("/")

#         response = build_response(
#             prediction_result=result,
#             filename=filename,
#             base_url=base_url
#         )

#         # -------------------------
#         # Save to Database
#         # -------------------------
#         saved_prediction = save_prediction(
#             user_id=user_id,
#             result=response,
#             image_path=image_path,
#             patient_data=patient_data
#         )

#         # ============================================================
#         # IMPORTANT: Add DB information to response
#         # ============================================================

#         response["id"] = saved_prediction.id

#         response["patient_name"] = saved_prediction.patient_name

#         response["patient_age"] = saved_prediction.patient_age

#         response["patient_gender"] = saved_prediction.patient_gender

#         response["clinical_notes"] = saved_prediction.clinical_notes

#         response["created_at"] = (
#             saved_prediction.created_at.isoformat()
#             if saved_prediction.created_at
#             else None
#         )

#         # ============================================================

#         logging.info(
#             f"Prediction saved successfully. ID={saved_prediction.id}"
#         )

#         return jsonify(response)

#     except Exception as e:
#         logging.exception(e)

#         return jsonify({
#             "status": "error",
#             "message": str(e)
#         }), 500





import os
import gc
import traceback
import torch
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.pipeline.explain_pipeline import ExplainPipeline
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
    explainer = None
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

        # Instantiate pipeline per-request to avoid keeping heavy PyTorch models in RAM permanently
        logging.info("Initializing ExplainPipeline...")
        explainer = ExplainPipeline()

        logging.info("Running explain() inside torch.no_grad()...")
        
        # Disable gradient computation to save ~60% RAM during inference
        with torch.no_grad():
            result = explainer.explain(image_path)

        logging.info("Explain finished.")

        # Force production HTTPS URL
        base_url = "https://pneumoai-hgh9.onrender.com"

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
            "error": str(e)
        }), 500

    finally:
        # Aggressive memory cleanup after every execution (success or failure)
        del explainer
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        gc.collect()