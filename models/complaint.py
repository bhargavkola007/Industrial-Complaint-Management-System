from datetime import datetime
from . import db

class Complaint(db.Model):
    __tablename__ = "complaints"

    id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.String(40), unique=True, nullable=False, index=True)

    employee_name = db.Column(db.String(120), nullable=False)
    employee_id = db.Column(db.String(60), nullable=False)
    employee_phone = db.Column(db.String(20), nullable=False)

    department = db.Column(db.String(50), nullable=False)
    machine_name = db.Column(db.String(120), nullable=False)
    machine_id = db.Column(db.String(80), nullable=False, index=True)
    location = db.Column(db.String(150), nullable=False)

    problem_type = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), nullable=False, default="Medium")
    communication_preference = db.Column(db.String(30), nullable=False, default="Message only")

    photo_path = db.Column(db.String(255), nullable=True)
    audio_path = db.Column(db.String(255), nullable=True)

    status = db.Column(db.String(30), nullable=False, default="Pending")
    power_status = db.Column(db.String(20), nullable=False, default="LOW")
    fault_status = db.Column(db.String(30), nullable=False, default="Fault Detected")

    accepted_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    accepted_at = db.Column(db.DateTime, nullable=True)
    resolved_at = db.Column(db.DateTime, nullable=True)

    admin_remarks = db.Column(db.Text, nullable=True)
    operator_remarks = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    accepted_user = db.relationship("User", foreign_keys=[accepted_by])

    def waiting_seconds(self):
        if self.accepted_at:
            return int((self.accepted_at - self.created_at).total_seconds())
        return None

    def resolving_seconds(self):
        if self.accepted_at and self.resolved_at:
            return int((self.resolved_at - self.accepted_at).total_seconds())
        return None

    def total_seconds(self):
        if self.resolved_at:
            return int((self.resolved_at - self.created_at).total_seconds())
        return None
