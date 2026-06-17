from functools import wraps
from flask import abort, current_app
from flask_login import current_user
from werkzeug.utils import secure_filename
import cloudinary
import cloudinary.uploader
import uuid


def normalize_dept(value):
    return (value or "").strip().lower()


def role_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)

            user_role = (current_user.role or "").strip().upper()

            if user_role not in roles:
                abort(403)

            return fn(*args, **kwargs)
        return wrapper
    return decorator


def operator_department_required(complaint):
    user_role = (current_user.role or "").strip().upper()

    if user_role == "ADMIN":
        return

    if user_role != "OPERATOR":
        abort(403)

    user_dept = normalize_dept(current_user.department)
    complaint_dept = normalize_dept(complaint.department)

    if user_dept != complaint_dept:
        abort(403)


def allowed_file(filename, allowed_set):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_set


def save_upload(file, kind):
    if not file or file.filename == "":
        return None

    cfg = current_app.config

    if kind == "image":
        allowed = cfg["ALLOWED_IMAGE_EXTENSIONS"]
        resource_type = "image"
        folder = "industrial_complaints/images"
    else:
        allowed = cfg["ALLOWED_AUDIO_EXTENSIONS"]
        resource_type = "video"
        folder = "industrial_complaints/audio"

    if not allowed_file(file.filename, allowed):
        raise ValueError(f"Invalid {kind} file type")

    cloudinary.config(
        cloud_name=cfg["CLOUDINARY_CLOUD_NAME"],
        api_key=cfg["CLOUDINARY_API_KEY"],
        api_secret=cfg["CLOUDINARY_API_SECRET"],
        secure=True
    )

    safe_name = secure_filename(file.filename)
    public_id = f"{uuid.uuid4().hex}_{safe_name.rsplit('.', 1)[0]}"

    result = cloudinary.uploader.upload(
        file,
        folder=folder,
        public_id=public_id,
        resource_type=resource_type
    )

    return result.get("secure_url")


def format_seconds(seconds):
    if seconds is None:
        return "-"

    seconds = int(seconds)
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60

    return f"{h:02d}:{m:02d}:{s:02d}"