from models import db
from datetime import datetime

class SensorHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    current = db.Column(db.Float)
    motor_status = db.Column(db.Boolean)
    laser_status = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)