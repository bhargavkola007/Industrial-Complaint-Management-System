from functools import wraps
from flask import abort, current_app
from flask_login import current_user
from werkzeug.utils import secure_filename
from pathlib import Path
import uuid

def role_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if current_user.role not in roles:
                abort(403)
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def operator_department_required(complaint):
    if current_user.role == "ADMIN":
        return
    if current_user.role != "OPERATOR" or current_user.department != complaint.department:
        abort(403)

def allowed_file(filename, allowed_set):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_set

def save_upload(file, kind):
    if not file or file.filename == "":
        return None

    cfg = current_app.config
    if kind == "image":
        allowed = cfg["ALLOWED_IMAGE_EXTENSIONS"]
        folder = Path(cfg["IMAGE_UPLOAD_FOLDER"])
    else:
        allowed = cfg["ALLOWED_AUDIO_EXTENSIONS"]
        folder = Path(cfg["AUDIO_UPLOAD_FOLDER"])

    if not allowed_file(file.filename, allowed):
        raise ValueError(f"Invalid {kind} file type")

    folder.mkdir(parents=True, exist_ok=True)
    safe_name = secure_filename(file.filename)
    unique_name = f"{uuid.uuid4().hex}_{safe_name}"
    file.save(folder / unique_name)

    if kind == "image":
        return f"uploads/images/{unique_name}"
    return f"uploads/audio/{unique_name}"

def format_seconds(seconds):
    if seconds is None:
        return "-"
    seconds = int(seconds)
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"
