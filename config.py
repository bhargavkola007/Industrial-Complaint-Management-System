# import os
# from pathlib import Path

# BASE_DIR = Path(__file__).resolve().parent

# class Config:
#     SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-this")
#     SQLALCHEMY_DATABASE_URI = os.environ.get(
#         "DATABASE_URL",
#         "sqlite:///" + str(BASE_DIR / "instance" / "database.db")
#     )
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

#     UPLOAD_FOLDER = str(BASE_DIR / "static" / "uploads")
#     IMAGE_UPLOAD_FOLDER = str(BASE_DIR / "static" / "uploads" / "images")
#     AUDIO_UPLOAD_FOLDER = str(BASE_DIR / "static" / "uploads" / "audio")

#     MAX_CONTENT_LENGTH = 12 * 1024 * 1024  # 12 MB
#     ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
#     ALLOWED_AUDIO_EXTENSIONS = {"mp3", "wav", "m4a", "ogg", "aac", "webm"}
# import os
# from pathlib import Path

# BASE_DIR = Path(__file__).resolve().parent

# class Config:
#     SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-this")

#     SQLALCHEMY_DATABASE_URI = os.environ.get(
#         "DATABASE_URL",
#         "mysql+pymysql://root:Amma%4001430@localhost:3306/industrial_complaint_db"
#     )

#     SQLALCHEMY_TRACK_MODIFICATIONS = False

#     UPLOAD_FOLDER = str(BASE_DIR / "static" / "uploads")
#     IMAGE_UPLOAD_FOLDER = str(BASE_DIR / "static" / "uploads" / "images")
#     AUDIO_UPLOAD_FOLDER = str(BASE_DIR / "static" / "uploads" / "audio")

#     MAX_CONTENT_LENGTH = 12 * 1024 * 1024
#     ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
#     ALLOWED_AUDIO_EXTENSIONS = {"mp3", "wav", "m4a", "ogg", "aac", "webm"}
    
    import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-this")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = str(BASE_DIR / "static" / "uploads")
    IMAGE_UPLOAD_FOLDER = str(BASE_DIR / "static" / "uploads" / "images")
    AUDIO_UPLOAD_FOLDER = str(BASE_DIR / "static" / "uploads" / "audio")

    MAX_CONTENT_LENGTH = 12 * 1024 * 1024