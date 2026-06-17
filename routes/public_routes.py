from flask import Blueprint, render_template, request, redirect, url_for, flash
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
    "ics_compliance": "ICS Compliance",
    "ehs_observation": "EHS Observation",
    "maintenance_feedback": "Maintenance Feedback",
    "5s_compliance": "5S Compliance",
    "sensor_checklist": "Sensor Checklist",
    "startup_checklist": "Startup Checklist",
}


@public_bp.route("/")
def index():
    return render_template("index.html")


@public_bp.route("/complaint/<department>")
def complaint_form(department):
    department_key = department.lower()

    if department_key not in DEPARTMENTS:
        flash("Invalid department selected.", "danger")
        return redirect(url_for("public.index"))

    return render_template(
        "complaint_form.html",
        department=department_key
    )


@public_bp.route("/submit-complaint", methods=["POST"])
def submit_complaint():
    try:
        department_key = request.form.get("department", "").strip().lower()
        department = DEPARTMENTS.get(department_key)

        if not department:
            flash("Invalid department selected.", "danger")
            return redirect(url_for("public.index"))
        machine_id = request.form.get("machine_id", "N/A").strip() or "N/A"
        machine_name = request.form.get("machine_name", "N/A").strip() or "N/A"
        problem_type = request.form.get("problem_type", "General Report").strip() or "General Report"

        description = request.form.get("description", "").strip()
        extra_desc = request.form.get("extra_desc", "").strip()

        if extra_desc:
            description = f"{description}\n\nAdditional Details:\n{extra_desc}"
        elif not description:
            description = "No extra description"

        photo_path = save_upload(request.files.get("photo"), "image")
        audio_path = save_upload(request.files.get("audio"), "audio")

        power_status = "LOW"
        problem_lower = problem_type.lower()

        if (
            "off" in problem_lower
            or "failure" in problem_lower
            or "dead" in problem_lower
            or "not working" in problem_lower
            or "power supply" in problem_lower
        ):
            power_status = "OFF"

        complaint = Complaint(
            complaint_id="CMP-" + uuid.uuid4().hex[:8].upper(),
            employee_name=request.form.get("employee_name"),
            employee_id=request.form.get("employee_id", "N/A"),
            employee_phone=request.form.get("employee_phone"),
            department=DEPARTMENTS[department_key],
            machine_name=machine_name,
            machine_id=machine_id,
            location=request.form.get("location"),
            problem_type=problem_type,
            description=description,
            priority=request.form.get("priority", "Medium"),
            communication_preference="Buzzer Alert",
            photo_path=photo_path,
            audio_path=audio_path,
            status="Pending",
            power_status=power_status,
            fault_status="Fault Detected",
            buzzer_active=True,
        )

        machine = Machine.query.filter_by(machine_id=machine_id).first()

        if not machine:
            machine = Machine(
                machine_name=machine_name,
                machine_id=machine_id,
                department=department,
                location=complaint.location,
            )
            db.session.add(machine)

        machine.machine_name = machine_name
        machine.power_status = power_status
        machine.fault_status = "Fault Detected"
        machine.department = department
        machine.location = complaint.location

        db.session.add(complaint)
        db.session.commit()

        flash(f"Report submitted successfully. Physical buzzer activated.", "success")
        return redirect(url_for("public.success", complaint_id=complaint.complaint_id))

    except ValueError as e:
        db.session.rollback()
        flash(str(e), "danger")
        return redirect(request.referrer or url_for("public.index"))

    except Exception as e:
        db.session.rollback()
        print("SUBMIT ERROR:", e)
        flash("Complaint submission failed. Please check all fields and file sizes.", "danger")
        return redirect(request.referrer or url_for("public.index"))


@public_bp.route("/success/<complaint_id>")
def success(complaint_id):
    complaint = Complaint.query.filter_by(complaint_id=complaint_id).first_or_404()
    return render_template("success.html", complaint=complaint)