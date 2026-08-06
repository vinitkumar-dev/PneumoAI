from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.prediction import Prediction
from src.services.chat_service import ask_ai

chat_bp = Blueprint("chat", __name__, url_prefix="/api")


@chat_bp.route("/chat", methods=["POST"])
@jwt_required()
def chat():

    user_id = int(get_jwt_identity())

    data = request.get_json()

    prediction_id = data.get("prediction_id")
    question = data.get("question")

    prediction = Prediction.query.filter_by(
        id=prediction_id,
        user_id=user_id
    ).first()

    if prediction is None:
        return jsonify({
            "status":"error",
            "message":"Prediction not found"
        }),404

    answer = ask_ai(
        prediction,
        question
    )

    return jsonify({
        "answer":answer
    })