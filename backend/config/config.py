import os
from datetime import timedelta
from urllib.parse import quote_plus

from dotenv import load_dotenv

# =====================================================
# Base Directory
# =====================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

# =====================================================
# Load Environment Variables
# =====================================================

load_dotenv(
    os.path.join(BASE_DIR, ".env")
)

# =====================================================
# Database Configuration
# =====================================================

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD", ""))
DB_NAME = os.getenv("DB_NAME", "pneumo_ai")

# =====================================================
# Validate Required Environment Variables
# =====================================================

required_env = [
    "SECRET_KEY",
    "JWT_SECRET_KEY",
]

missing = [key for key in required_env if not os.getenv(key)]

if missing:
    raise RuntimeError(
        f"Missing environment variables: {', '.join(missing)}. "
        f"Copy backend/.env.example to backend/.env and fill in values "
        f"(or set them in your Render service's Environment tab)."
    )

# =====================================================
# CORS Origins
# =====================================================
# Configurable via a comma-separated CORS_ORIGINS env var so the same
# codebase works locally, on preview deployments, and in production
# without code changes. Falls back to sensible local + production
# defaults if the env var isn't set.

_default_origins = (
    "http://localhost:5173,"
    "http://127.0.0.1:5173,"
    "http://localhost:3000,"
    "https://pneumo-ai-app.onrender.com"
)

CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", _default_origins).split(",")
    if origin.strip()
]

# =====================================================
# Public Backend Base URL
# =====================================================
# Used to build absolute URLs for the original X-ray image returned by
# the API. If not set, routes fall back to Flask's `request.host_url`,
# which works correctly for both local development and Render (thanks
# to ProxyFix in app.py).

BASE_URL = os.getenv("BASE_URL", "").rstrip("/")

# =====================================================
# Configuration Class
# =====================================================

class Config:

    # -----------------------------
    # Flask
    # -----------------------------
    SECRET_KEY = os.getenv("SECRET_KEY")

    DEBUG = os.getenv("DEBUG", "True").lower() == "true"

    ENV = os.getenv("FLASK_ENV", "development")

    # -----------------------------
    # JWT
    # -----------------------------
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)

    JWT_TOKEN_LOCATION = ["headers"]

    JWT_HEADER_NAME = "Authorization"

    JWT_HEADER_TYPE = "Bearer"

    # -----------------------------
    # Database
    # -----------------------------
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://"
        f"{DB_USER}:"
        f"{DB_PASSWORD}@"
        f"{DB_HOST}:"
        f"{DB_PORT}/"
        f"{DB_NAME}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 10,
        "max_overflow": 20,
        "pool_recycle": 3600,
        "pool_pre_ping": True,
    }

    # -----------------------------
    # Upload Configuration
    # -----------------------------
    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "static",
        "uploads"
    )

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

    ALLOWED_EXTENSIONS = {
        "png",
        "jpg",
        "jpeg",
        "webp",
        "dcm",
    }

    # -----------------------------
    # CORS / Base URL
    # -----------------------------
    CORS_ORIGINS = CORS_ORIGINS

    BASE_URL = BASE_URL

    # -----------------------------
    # JSON
    # -----------------------------
    JSON_SORT_KEYS = False

    JSONIFY_PRETTYPRINT_REGULAR = False
