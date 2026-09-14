from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.models.telemetry import Telemetry
from backend.schemas.health import HealthRequest


def calculate_health(db: Session, data: HealthRequest):

    # Fetch the latest telemetry for the given robot
    telemetry = (
        db.query(Telemetry)
        .filter(Telemetry.robot_id == data.robot_id)
        .order_by(Telemetry.timestamp.desc())
        .first()
    )

    # If no telemetry exists
    if telemetry is None:
        raise HTTPException(
            status_code=404,
            detail="No telemetry data found for this robot."
        )

    # Start with 100% health
    health = 100

    # Safely get telemetry metrics with fallback to joint model fields
    temp = getattr(telemetry, "temperature", None)
    if temp is None:
        temp = getattr(telemetry, "Temperature_T0", 0.0) or 0.0

    vib = getattr(telemetry, "vibration", None)
    if vib is None:
        vib = 0.0

    motor_cur = getattr(telemetry, "motor_current", None)
    if motor_cur is None:
        motor_cur = getattr(telemetry, "Current_J0", 0.0) or 0.0

    torq = getattr(telemetry, "torque", None)
    if torq is None:
        torq = getattr(telemetry, "Tool_current", 0.0) or 0.0

    # Temperature
    if temp > 60:
        health -= 20

    # Vibration
    if vib > 0.5:
        health -= 30

    # Motor Current
    if motor_cur > 5:
        health -= 25

    # Torque
    if torq > 25:
        health -= 25

    # Prevent negative score
    health = max(0, health)

    # Determine health status
    if health >= 90:
        status = "Excellent"
    elif health >= 75:
        status = "Good"
    elif health >= 60:
        status = "Warning"
    elif health >= 40:
        status = "Critical"
    else:
        status = "Failure Likely"

    return {
        "robot_id": telemetry.robot_id,
        "temperature": float(temp),
        "vibration": float(vib),
        "motor_current": float(motor_cur),
        "torque": float(torq),
        "health_score": float(health),
        "health_status": status
    }