import os
import uuid


# =========================
# SAVE UPLOADED IMAGE
# =========================
def save_upload(file, upload_folder):
    """
    Saves uploaded image safely and returns filename + full path
    """

    os.makedirs(upload_folder, exist_ok=True)

    # extract extension
    ext = os.path.splitext(file.filename)[1]
    if ext == "":
        ext = ".jpg"

    # unique filename
    filename = f"{uuid.uuid4()}{ext}"

    file_path = os.path.join(upload_folder, filename)

    file.save(file_path)

    return filename, file_path


# =========================
# SAFE PATH NORMALIZER
# =========================
def to_url_path(base_url, file_path):
    """
    Converts local path → browser URL
    Fixes Windows \ issue + artifacts paths
    """

    if not file_path:
        return None

    file_path = os.path.normpath(file_path).replace("\\", "/")

    # remove project root if present
    if "static" in file_path:
        file_path = file_path[file_path.index("static"):]
    elif "artifacts" in file_path:
        file_path = file_path[file_path.index("artifacts"):]

    return f"{base_url}/{file_path}"


# =========================
# SAVE ARTIFACT (GRADCAM / YOLO)
# =========================
def save_artifact(image_array, save_path):
    """
    Used for GradCAM / YOLO output images
    """

    import cv2

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    cv2.imwrite(save_path, image_array)

    return save_path