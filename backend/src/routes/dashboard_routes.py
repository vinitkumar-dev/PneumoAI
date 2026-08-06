from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.services.dashboard_service import get_dashboard_summary

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/api/dashboard"
)


@dashboard_bp.route("/summary", methods=["GET"])
@jwt_required()
def dashboard_summary():

    user_id = get_jwt_identity()

    data = get_dashboard_summary(user_id)

    return jsonify(data), 200