from datetime import datetime
from . import db

class Machine(db.Model):
    __tablename__ = "machines"

    id = db.Column(db.Integer, primary_key=True)
    machine_name = db.Column(db.String(120), nullable=False)
    machine_id = db.Column(db.String(80), unique=True, nullable=False, index=True)
    department = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    power_status = db.Column(db.String(20), nullable=False, default="ON")
    fault_status = db.Column(db.String(30), nullable=False, default="Normal")
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
