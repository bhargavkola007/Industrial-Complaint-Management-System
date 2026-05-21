from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
import uuid

from models import db
from models.complaint import Complaint
from models.machine import Machine
from .utils import save_upload

public_bp = Blueprint("public", __name__)

DEPARTMENTS = {
    "electrical": "Electrical",
    "mechanical": "Mechanical",
    "supervisor": "Supervisor",
}

@public_bp.route("/")
def index():
    return render_template("index.html")

@public_bp.route("/complaint/<department>")
def complaint_form(department):
    department_name = DEPARTMENTS.get(department.lower())
    if not department_name:
        flash("Invalid department selected.", "danger")
        return redirect(url_for("public.index"))
    return render_template("complaint_form.html", department=department_name)

@public_bp.route("/submit-complaint", methods=["POST"])
def submit_complaint():
    try:
        department = request.form.get("department")
        machine_id = request.form.get("machine_id", "").strip()
        problem_type = request.form.get("problem_type", "")

        photo_path = save_upload(request.files.get("photo"), "image")
        audio_path = save_upload(request.files.get("audio"), "audio")

        power_status = "LOW"
        if "off" in problem_type.lower() or "failure" in problem_type.lower():
            power_status = "OFF"

        complaint = Complaint(
            complaint_id="CMP-" + uuid.uuid4().hex[:8].upper(),
            employee_name=request.form.get("employee_name"),
            employee_id=request.form.get("employee_id"),
            employee_phone=request.form.get("employee_phone"),
            department=department,
            machine_name=request.form.get("machine_name"),
            machine_id=machine_id,
            location=request.form.get("location"),
            problem_type=problem_type,
            description=request.form.get("description"),
            priority=request.form.get("priority"),
            communication_preference=request.form.get("communication_preference"),
            photo_path=photo_path,
            audio_path=audio_path,
            status="Pending",
            power_status=power_status,
            fault_status="Fault Detected",
        )

        machine = Machine.query.filter_by(machine_id=machine_id).first()
        if not machine:
            machine = Machine(
                machine_name=complaint.machine_name,
                machine_id=machine_id,
                department=department,
                location=complaint.location,
            )
            db.session.add(machine)

        machine.power_status = power_status
        machine.fault_status = "Fault Detected"
        machine.department = department
        machine.location = complaint.location

        db.session.add(complaint)
        db.session.commit()

        alert = f"SMS sent to {department} Department"
        if complaint.communication_preference == "Call only":
            alert = "Call alert requested"
        elif complaint.communication_preference == "Both call and message":
            alert = f"SMS and call alert sent to Admin and {department} Department Operator"

        flash(alert, "success")
        return redirect(url_for("public.success", complaint_id=complaint.complaint_id))

    except ValueError as e:
        db.session.rollback()
        flash(str(e), "danger")
        return redirect(request.referrer or url_for("public.index"))
    except Exception as e:
        db.session.rollback()
        flash("Complaint submission failed. Please check all fields and file sizes.", "danger")
        return redirect(request.referrer or url_for("public.index"))

@public_bp.route("/success/<complaint_id>")
def success(complaint_id):
    complaint = Complaint.query.filter_by(complaint_id=complaint_id).first_or_404()
    return render_template("success.html", complaint=complaint)
