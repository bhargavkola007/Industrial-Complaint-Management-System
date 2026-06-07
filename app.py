from fileinput import filename

from flask import Flask, send_from_directory
from flask_login import LoginManager
from pathlib import Path
from routes.buzzer_routes import buzzer_bp
from config import Config
from models import db
from models.user import User

from routes.public_routes import public_bp
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.operator_routes import operator_bp
from routes.utils import format_seconds

try:
    from routes.sensor_routes import sensor_bp
except ImportError:
    sensor_bp = None


login_manager = LoginManager()
login_manager.login_view = "auth.login"


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.config.setdefault("ALLOWED_IMAGE_EXTENSIONS", {"png", "jpg", "jpeg", "gif", "webp"})
    app.config.setdefault("ALLOWED_AUDIO_EXTENSIONS", {"mp3", "wav", "m4a", "ogg", "aac", "webm"})

    Path(app.config["IMAGE_UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)
    Path(app.config["AUDIO_UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)
    Path("instance").mkdir(exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(operator_bp)
    app.register_blueprint(buzzer_bp)

    if sensor_bp:
        app.register_blueprint(sensor_bp)

    app.jinja_env.filters["duration"] = format_seconds

    @app.route("/uploads/<path:filename>")
    def uploaded_file(filename):
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

    @app.after_request
    def add_no_cache_headers(response):
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

    with app.app_context():
        db.create_all()
        seed_users()

    return app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def seed_users():
    users = [
        ("Admin", "admin@company.com", "admin123", "ADMIN", None),
        ("Electrical Operator", "electrical@company.com", "electrical123", "OPERATOR", "Electrical"),
        ("Mechanical Operator", "mechanical@company.com", "mechanical123", "OPERATOR", "Mechanical"),
        ("Supervisor Operator", "supervisor@company.com", "supervisor123", "OPERATOR", "Supervisor"),
    ]

    for name, email, password, role, department in users:
        existing = User.query.filter_by(email=email).first()
        if not existing:
            user = User(name=name, email=email, role=role, department=department)
            user.set_password(password)
            db.session.add(user)

    db.session.commit()


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)