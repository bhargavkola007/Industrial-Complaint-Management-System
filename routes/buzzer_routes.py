from flask import Blueprint, jsonify, request, current_app
from models.complaint import Complaint

buzzer_bp = Blueprint("buzzer", __name__, url_prefix="/api/buzzer")


def check_token():
    token = request.args.get("token")
    return token == current_app.config["BUZZER_API_TOKEN"]


@buzzer_bp.route("/state")
def buzzer_state():
    if not check_token():
        return jsonify({"error": "Unauthorized"}), 401

    electrical = Complaint.query.filter_by(
        department="Electrical",
        buzzer_active=True
    ).count() > 0

    mechanical = Complaint.query.filter_by(
        department="Mechanical",
        buzzer_active=True
    ).count() > 0

    supervisor = Complaint.query.filter_by(
        department="Supervisor",
        buzzer_active=True
    ).count() > 0

    return jsonify({
        "Electrical": electrical,
        "Mechanical": mechanical,
        "Supervisor": supervisor
    })