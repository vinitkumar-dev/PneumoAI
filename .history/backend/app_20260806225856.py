import os
from werkzeug.middleware.proxy_fix import ProxyFix

# =========================================================
# MEMORY & CONFIG OPTIMIZATION (CRITICAL FOR RENDER 512MB RAM)
# =========================================================
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["YOLO_CONFIG_DIR"] = "/tmp/Ultralytics"

import torch
torch.set_num_threads(1)

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from config.config import Config
from database.db import db

from src.routes.predict_routes import predict_bp
from src.routes.health_routes import health_bp
from src.routes.report_routes import report_bp
from src.routes.auth_routes import auth_bp
from src.routes.file_routes import file_bp
from src.routes.dashboard_routes import dashboard_bp
from src.routes.history_routes import history_bp
from src.routes.chat_routes import chat_bp

from src.logger import logging


def create_app():
    app = Flask(__name__)

    # =========================================================
    # RENDER REVERSE PROXY FIX (FOR HTTPS URL GENERATION)
    # =========================================================
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    app.config.from_object(Config)

    db.init_app(app)

    app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
    jwt = JWTManager(app)

    migrate = Migrate(app, db)

    # =========================
    # FLASK-CORS CONFIGURATION
    # =========================
    CORS(
    app,
    resources={
        r"/*": {
            "origins": [
                "https://pneumo-ai-app.onrender.com",
                "http://localhost:5173"
            ]
        }
    },
    supports_credentials=True,
    allow_headers=[
        "Content-Type",
        "Authorization"
    ],
    methods=[
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "OPTIONS"
    ]
)

    # Force CORS headers on ALL responses (including 40x and 50x error states)
    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With, Accept"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        return response

    # =========================
    # REGISTER BLUEPRINTS
    # =========================
    app.register_blueprint(health_bp)
    app.register_blueprint(file_bp)
    app.register_blueprint(predict_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(chat_bp)

    # =========================
    # ROOT & HEALTH ENDPOINT
    # =========================
    @app.route("/", methods=["GET"])
    def home():
        return jsonify({"status": "online", "message": "PneumoAI API is running"}), 200

    logging.info("Flask App Initialized Successfully")
    with app.app_context():
        db.create_all()

    return app


# Expose app for WSGI servers like Gunicorn
app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)