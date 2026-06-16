import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "industrial_cms_1029384756")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://root:Amma%4001430@localhost:3306/industrial_complaint_db_itc"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAX_CONTENT_LENGTH = 12 * 1024 * 1024

    ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
    ALLOWED_AUDIO_EXTENSIONS = {"mp3", "wav", "m4a", "ogg", "aac", "webm"}

    CLOUDINARY_CLOUD_NAME = os.environ.get("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.environ.get("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.environ.get("CLOUDINARY_API_SECRET")

    BUZZER_API_TOKEN = os.environ.get("BUZZER_API_TOKEN", "industrial-buzzer-123")
    AUTO_COMPLAINT_API_TOKEN = os.environ.get(
    "AUTO_COMPLAINT_API_TOKEN",
    "auto-complaint-123"
    )