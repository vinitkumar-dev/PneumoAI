from flask import Blueprint, send_from_directory
import os

file_bp = Blueprint("files", __name__)

BASE_DIR = os.getcwd()


@file_bp.route("/artifacts/<path:filename>")
def artifacts(filename):

    return send_from_directory(
        os.path.join(BASE_DIR, "artifacts"),
        filename
    )


@file_bp.route("/uploads/<path:filename>")
def uploads(filename):

    return send_from_directory(
        os.path.join(BASE_DIR, "static", "uploads"),
        filename
    )