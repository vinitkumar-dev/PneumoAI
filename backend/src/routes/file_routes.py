import os
from flask import Blueprint, send_from_directory, abort

file_bp = Blueprint("files", __name__)

# backend folder
BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

ARTIFACTS_DIR = os.path.join(BASE_DIR, "artifacts")
UPLOADS_DIR = os.path.join(BASE_DIR, "static", "uploads")


@file_bp.route("/artifacts/<path:filename>")
def artifacts(filename):

    file_path = os.path.join(ARTIFACTS_DIR, filename)

    if not os.path.exists(file_path):
        return abort(404)

    return send_from_directory(
        ARTIFACTS_DIR,
        filename
    )


@file_bp.route("/uploads/<path:filename>")
def uploads(filename):

    file_path = os.path.join(UPLOADS_DIR, filename)

    if not os.path.exists(file_path):
        return abort(404)

    return send_from_directory(
        UPLOADS_DIR,
        filename
    )