from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from datetime import datetime

sensor_bp = Blueprint("sensor", __name__, url_prefix="/sensors")

latest_sensor_data = {
    "temperature": "--",
    "humidity": "--",
    "ir_beam": "--",
    "current": "--",
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

    latest_sensor_data["temperature"] = data.get("temperature", "--")
    latest_sensor_data["humidity"] = data.get("humidity", "--")
    latest_sensor_data["ir_beam"] = data.get("ir_beam", "--")
    latest_sensor_data["current"] = data.get("current", "--")
    latest_sensor_data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return jsonify({
        "message": "Sensor data updated successfully",
        "data": latest_sensor_data
    }), 200

@sensor_bp.route("/api/latest")
@login_required
def latest_sensor():
    return jsonify(latest_sensor_data)