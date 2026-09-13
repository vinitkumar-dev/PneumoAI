import os
from werkzeug.middleware.proxy_fix import ProxyFix

# =========================================================
# MEMORY OPTIMIZATION FOR RENDER (512MB RAM LIMIT)
# =========================================================
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

import torch
torch.set_num_threads(1)

from flask import Flask, jsonify, send_from_directory
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

    # Ensure upload and artifact directories exist on container startup
    os.makedirs("static/uploads", exist_ok=True)
    os.makedirs("artifacts", exist_ok=True)

    # Disable strict trailing slash redirects (prevents 308 redirects that strip CORS headers)
    app.url_map.strict_slashes = False

    # =====================================================
    # RENDER PROXY FIX
    # =====================================================
    app.wsgi_app = ProxyFix(
        app.wsgi_app,
        x_for=1,
        x_proto=1,
        x_host=1,
        x_prefix=1
    )

    # =====================================================
    # CONFIG & DB
    # =====================================================
    app.config.from_object(Config)

    db.init_app(app)

    # =====================================================
    # JWT & MIGRATE
    # =====================================================
    app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
    jwt = JWTManager(app)
    migrate = Migrate(app, db)

    # =====================================================
    # CORS
    # =====================================================
    # Allowed origins come from the CORS_ORIGINS env var (see config.py),
    # so the same code works for local dev, staging, and production.
    CORS(
        app,
        resources={r"/*": {"origins": Config.CORS_ORIGINS}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization", "Accept"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    # =====================================================
    # SERVE AI GENERATED FILES & UPLOADS
    # =====================================================
    @app.route("/artifacts/<path:path>", methods=["GET"])
    def serve_artifacts(path):
        return send_from_directory("artifacts", path)

    @app.route("/uploads/<path:path>", methods=["GET"])
    def serve_uploads(path):
        return send_from_directory("static/uploads", path)

    @app.route("/static/uploads/<path:path>", methods=["GET"])
    def serve_static_uploads(path):
        return send_from_directory("static/uploads", path)

    # =====================================================
    # BLUEPRINTS
    # =====================================================
    app.register_blueprint(health_bp)
    app.register_blueprint(file_bp)
    app.register_blueprint(predict_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(chat_bp)

    # =====================================================
    # ROOT
    # =====================================================
    @app.route("/")
    def home():
        return jsonify({
            "status": "online",
            "message": "PneumoAI API is running"
        }), 200

    # =====================================================
    # JSON ERROR HANDLERS
    # =====================================================
    # Ensures the frontend always receives JSON (not an HTML error page),
    # which keeps Axios's error.response.data.message access safe.
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"status": "error", "message": "Resource not found."}), 404

    @app.errorhandler(413)
    def too_large(e):
        return jsonify({
            "status": "error",
            "message": "Uploaded file is too large. Maximum size is 16 MB."
        }), 413

    @app.errorhandler(500)
    def server_error(e):
        logging.exception("Unhandled server error")
        return jsonify({"status": "error", "message": "Internal server error."}), 500

    logging.info("Flask App Initialized Successfully")

    with app.app_context():
        db.create_all()

    return app


# =========================================================
# GUNICORN ENTRY
# =========================================================
app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
