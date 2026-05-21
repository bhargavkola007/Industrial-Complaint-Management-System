from datetime import datetime
from . import db

class ForwardHistory(db.Model):
    __tablename__ = "forward_history"

    id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey("complaints.id"), nullable=False)
    from_department = db.Column(db.String(50), nullable=False)
    to_department = db.Column(db.String(50), nullable=False)
    forwarded_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    forwarded_at = db.Column(db.DateTime, default=datetime.utcnow)

    complaint = db.relationship("Complaint", backref="forward_history")
    forwarded_user = db.relationship("User")
