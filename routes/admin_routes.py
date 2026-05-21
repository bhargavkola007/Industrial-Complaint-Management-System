from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import func
from datetime import datetime

from models import db
from models.complaint import Complaint
from models.forward_history import ForwardHistory
from models.machine import Machine
from .utils import role_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/dashboard")
@login_required
@role_required("ADMIN")
def dashboard():
    total = Complaint.query.count()
    counts = {
        "pending": Complaint.query.filter_by(status="Pending").count(),
        "accepted": Complaint.query.filter_by(status="Accepted").count(),
        "in_progress": Complaint.query.filter_by(status="In Progress").count(),
        "resolved": Complaint.query.filter_by(status="Resolved").count(),
        "rejected": Complaint.query.filter_by(status="Rejected").count(),
        "high_critical": Complaint.query.filter(Complaint.priority.in_(["High", "Critical"])).count(),
    }
    dept_rows = db.session.query(Complaint.department, func.count(Complaint.id)).group_by(Complaint.department).all()
    dept_counts = dict(dept_rows)
    resolved = Complaint.query.filter(Complaint.resolved_at.isnot(None)).all()
    avg_seconds = None
    if resolved:
        avg_seconds = sum([(c.resolved_at - c.created_at).total_seconds() for c in resolved]) / len(resolved)
    latest = Complaint.query.order_by(Complaint.created_at.desc()).limit(8).all()
    return render_template("admin_dashboard.html", total=total, counts=counts, dept_counts=dept_counts, avg_seconds=avg_seconds, complaints=latest)

@admin_bp.route("/complaints")
@login_required
@role_required("ADMIN")
def complaints():
    department = request.args.get("department")
    status = request.args.get("status")
    priority = request.args.get("priority")
    query = Complaint.query
    if department:
        query = query.filter_by(department=department)
    if status:
        query = query.filter_by(status=status)
    if priority:
        query = query.filter_by(priority=priority)
    complaints = query.order_by(Complaint.created_at.desc()).all()
    return render_template("operator_dashboard.html", complaints=complaints, is_admin_list=True)

@admin_bp.route("/complaint/<int:id>")
@login_required
@role_required("ADMIN")
def complaint_detail(id):
    complaint = Complaint.query.get_or_404(id)
    machine = Machine.query.filter_by(machine_id=complaint.machine_id).first()
    return render_template("complaint_detail.html", complaint=complaint, machine=machine)

@admin_bp.route("/complaint/<int:id>/update-status", methods=["POST"])
@login_required
@role_required("ADMIN")
def update_status(id):
    complaint = Complaint.query.get_or_404(id)
    status = request.form.get("status")
    complaint.status = status
    complaint.admin_remarks = request.form.get("admin_remarks")
    if status == "Resolved" and not complaint.resolved_at:
        complaint.resolved_at = datetime.utcnow()
        complaint.power_status = "ON"
        complaint.fault_status = "Resolved"
    db.session.commit()
    flash("Complaint updated.", "success")
    return redirect(url_for("admin.complaint_detail", id=id))

@admin_bp.route("/complaint/<int:id>/forward", methods=["POST"])
@login_required
@role_required("ADMIN")
def forward(id):
    complaint = Complaint.query.get_or_404(id)
    to_department = request.form.get("to_department")
    reason = request.form.get("reason")
    history = ForwardHistory(
        complaint_id=complaint.id,
        from_department=complaint.department,
        to_department=to_department,
        forwarded_by=current_user.id,
        reason=reason,
    )
    complaint.department = to_department
    complaint.status = "Pending"
    complaint.accepted_by = None
    complaint.accepted_at = None
    db.session.add(history)
    db.session.commit()
    flash("Complaint forwarded.", "success")
    return redirect(url_for("admin.complaint_detail", id=id))

@admin_bp.route("/complaint/<int:id>/delete", methods=["POST"])
@login_required
@role_required("ADMIN")
def delete(id):
    complaint = Complaint.query.get_or_404(id)
    db.session.delete(complaint)
    db.session.commit()
    flash("Complaint deleted.", "info")
    return redirect(url_for("admin.complaints"))
