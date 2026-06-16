from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import login_required
from models.complaint import Complaint, now_india
from datetime import datetime
from models import db
import uuid
from models.sensor_history import SensorHistory

sensor_bp = Blueprint("sensor", __name__, url_prefix="/sensors")

latest_sensor_data = {
    "temperature": "--",
    "humidity": "--",
    "current": "--",
    "motor_status": "--",
    "laser_status": "--",
    "updated_at": "--"
}

@sensor_bp.route("/live")
@login_required
def live_sensors():
    return render_template("live_sensors.html")

@sensor_bp.route("/api/update", methods=["POST"])
def update_sensor_data():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data received"}), 400

    temperature = data.get("temperature")
    humidity = data.get("humidity")
    current = data.get("current")
    motor_status = data.get("motor_status")
    laser_status = data.get("laser_status")

    latest_sensor_data["temperature"] = temperature
    latest_sensor_data["humidity"] = humidity
    latest_sensor_data["current"] = current
    latest_sensor_data["motor_status"] = motor_status
    latest_sensor_data["laser_status"] = laser_status
    latest_sensor_data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    history = SensorHistory(
        temperature=temperature,
        humidity=humidity,
        current=current,
        motor_status=motor_status,
        laser_status=laser_status
    )

    db.session.add(history)
    db.session.commit()

    return jsonify({
        "message": "Sensor data updated successfully",
        "data": latest_sensor_data
    }), 200

@sensor_bp.route("/api/latest")
@login_required
def latest_sensor():
    return jsonify(latest_sensor_data)

@sensor_bp.route("/api/history")
@login_required
def sensor_history():
    records = SensorHistory.query.order_by(SensorHistory.created_at.desc()).limit(50).all()

    return jsonify([
        {
            "temperature": r.temperature,
            "humidity": r.humidity,
            "current": r.current,
            "motor_status": r.motor_status,
            "laser_status": r.laser_status,
            "created_at": r.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        for r in records
    ])

@sensor_bp.route("/api/auto-complaint", methods=["POST"])
def auto_complaint():
    token = request.args.get("token")

    if token != current_app.config["AUTO_COMPLAINT_API_TOKEN"]:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data received"}), 400

    complaint = Complaint(
        employee_name="Automatic Sensor System",
        employee_id="AUTO-ESP32",
        employee_phone="N/A",
        department="Electrical",
        machine_name=data.get("machine_name", "Industrial Motor"),
        machine_id=data.get("machine_id", "MOTOR-001"),
        location=data.get("location", "Production Unit"),
        problem_type="Motor Fault Detected",
        description=data.get(
            "description",
            "Relay is ON and laser is safe, but motor current is zero for 10 consecutive readings. Possible motor failure, wire disconnection, open circuit, or power path failure."
        ),
        complaint_id="AUTO-" + uuid.uuid4().hex[:8].upper(),
        priority="Critical",
        communication_preference="System Generated",
        status="Pending",
        power_status="ON",
        fault_status="Fault Detected",
        buzzer_active=True,
        created_at=now_india()
    )

    db.session.add(complaint)
    db.session.commit()

    return jsonify({
        "message": "Automatic complaint created successfully",
        "complaint_id": complaint.complaint_id
    }), 201