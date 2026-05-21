from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from datetime import datetime

from models import db
from models.complaint import Complaint
from models.forward_history import ForwardHistory
from models.machine import Machine
from .utils import role_required, operator_department_required

operator_bp = Blueprint("operator", __name__, url_prefix="/operator")

@operator_bp.route("/dashboard")
@login_required
@role_required("OPERATOR")
def dashboard():
    complaints = Complaint.query.filter_by(department=current_user.department).order_by(Complaint.created_at.desc()).all()
    return render_template("operator_dashboard.html", complaints=complaints, is_admin_list=False)

@operator_bp.route("/complaints")
@login_required
@role_required("OPERATOR")
def complaints():
    return redirect(url_for("operator.dashboard"))

@operator_bp.route("/complaint/<int:id>")
@login_required
@role_required("OPERATOR")
def complaint_detail(id):
    complaint = Complaint.query.get_or_404(id)
    operator_department_required(complaint)
    machine = Machine.query.filter_by(machine_id=complaint.machine_id).first()
    return render_template("complaint_detail.html", complaint=complaint, machine=machine)

@operator_bp.route("/complaint/<int:id>/accept", methods=["POST"])
@login_required
@role_required("OPERATOR")
def accept(id):
    complaint = Complaint.query.get_or_404(id)
    operator_department_required(complaint)
    if complaint.status not in ["Pending", "Forwarded"]:
        flash("Only pending/forwarded complaints can be accepted.", "warning")
    else:
        complaint.status = "Accepted"
        complaint.accepted_by = current_user.id
        complaint.accepted_at = datetime.utcnow()
        flash("Complaint accepted.", "success")
    db.session.commit()
    return redirect(url_for("operator.complaint_detail", id=id))

@operator_bp.route("/complaint/<int:id>/start", methods=["POST"])
@login_required
@role_required("OPERATOR")
def start(id):
    complaint = Complaint.query.get_or_404(id)
    operator_department_required(complaint)
    complaint.status = "In Progress"
    complaint.fault_status = "Under Repair"
    machine = Machine.query.filter_by(machine_id=complaint.machine_id).first()
    if machine:
        machine.fault_status = "Under Repair"
    db.session.commit()
    flash("Work started.", "success")
    return redirect(url_for("operator.complaint_detail", id=id))

@operator_bp.route("/complaint/<int:id>/verify-machine", methods=["POST"])
@login_required
@role_required("OPERATOR")
def verify_machine(id):
    complaint = Complaint.query.get_or_404(id)
    operator_department_required(complaint)

    power_status = request.form.get("power_status")
    fault_status = request.form.get("fault_status")

    complaint.power_status = power_status
    complaint.fault_status = fault_status

    machine = Machine.query.filter_by(machine_id=complaint.machine_id).first()
    if machine:
        machine.power_status = power_status
        machine.fault_status = fault_status

    if power_status == "ON" and fault_status == "Resolved":
        flash("Machine verified successfully. Complaint can be resolved.", "success")
    else:
        complaint.status = "In Progress"
        flash("Machine is not fully restored. Complaint remains In Progress.", "warning")

    db.session.commit()
    return redirect(url_for("operator.complaint_detail", id=id))

@operator_bp.route("/complaint/<int:id>/resolve", methods=["POST"])
@login_required
@role_required("OPERATOR")
def resolve(id):
    complaint = Complaint.query.get_or_404(id)
    operator_department_required(complaint)
    complaint.operator_remarks = request.form.get("operator_remarks")

    if complaint.power_status == "ON" and complaint.fault_status == "Resolved":
        complaint.status = "Resolved"
        complaint.resolved_at = datetime.utcnow()
        machine = Machine.query.filter_by(machine_id=complaint.machine_id).first()
        if machine:
            machine.power_status = "ON"
            machine.fault_status = "Resolved"
        flash("Complaint resolved and closed.", "success")
    else:
        complaint.status = "In Progress"
        flash("Cannot close complaint until machine status is ON and fault status is Resolved.", "danger")

    db.session.commit()
    return redirect(url_for("operator.complaint_detail", id=id))

@operator_bp.route("/complaint/<int:id>/forward", methods=["POST"])
@login_required
@role_required("OPERATOR")
def forward(id):
    complaint = Complaint.query.get_or_404(id)
    operator_department_required(complaint)
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
    complaint.status = "Forwarded"
    complaint.accepted_by = None
    complaint.accepted_at = None

    machine = Machine.query.filter_by(machine_id=complaint.machine_id).first()
    if machine:
        machine.department = to_department

    db.session.add(history)
    db.session.commit()
    flash("Complaint forwarded to correct department.", "success")
    return redirect(url_for("operator.dashboard"))
