from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
import bcrypt

# from extensions import db
from database.db import db

from models.user import User

auth_bp = Blueprint("auth", __name__)


# ==========================
# GET CURRENT USER
# ==========================
@auth_bp.route("/auth/me", methods=["GET"])
@jwt_required()
def get_me():

    user_id = int(get_jwt_identity())

    user = db.session.get(User, user_id)

    if user is None:
        return jsonify({
            "status": "error",
            "message": "User not found"
        }), 404

    return jsonify({
        "status": "success",
        "user": {
    "id": user.id,
    "name": user.name,
    "email": user.email
}
    }), 200


# ==========================
# REGISTER
# ==========================
@auth_bp.route("/auth/register", methods=["POST"])
def register():

    data = request.get_json()
    # print('result is ',data)
    # print(User.__table__.columns.keys())

    username = data.get("username") or data.get("name")
    email = data.get("email")
    password = data.get("password")
    # print(username)

    if not username or not email or not password:
        return jsonify({
            "status": "error",
            "message": "All fields are required"
        }), 400

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({
            "status": "error",
            "message": "Email already exists"
        }), 409

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    user = User(
        name=username,
        email=email,
        password_hash=hashed_password
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "User registered successfully"
    }), 201


# ==========================
# LOGIN
# ==========================
@auth_bp.route("/auth/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "status": "error",
            "message": "Email and password are required"
        }), 400

    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({
            "status": "error",
            "message": "Invalid email or password"
        }), 401

    if not bcrypt.checkpw(
        password.encode("utf-8"),
        user.password_hash.encode("utf-8")
    ):
        return jsonify({
            "status": "error",
            "message": "Invalid email or password"
        }), 401

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
    "email": user.email,
    "name": user.name
}
    )

    return jsonify({
        "status": "success",
        "message": "Login successful",
        "access_token": access_token,
       "user": {
    "id": user.id,
    "name": user.name,
    "email": user.email
}
    }), 200