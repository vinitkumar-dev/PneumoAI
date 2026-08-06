from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)

@health_bp.route("/statistics", methods=["GET"])
def statistics():
    return jsonify({
        "total_predictions": 120,
        "pneumonia_cases": 65,
        "normal_cases": 55,
        "accuracy": 90.54
    })