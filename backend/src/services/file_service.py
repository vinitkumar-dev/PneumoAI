import os
import uuid


def save_upload(file, upload_folder):
    """
    Save uploaded file and return filename + full path
    """

    os.makedirs(upload_folder, exist_ok=True)

    ext = os.path.splitext(file.filename)[1]
    if ext == "":
        ext = ".jpg"

    filename = f"{uuid.uuid4()}{ext}"

    file_path = os.path.join(upload_folder, filename)

    file.save(file_path)

    return filename, file_path