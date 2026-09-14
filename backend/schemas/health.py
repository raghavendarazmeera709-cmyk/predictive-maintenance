from pydantic import BaseModel

class HealthRequest(BaseModel):
    robot_id: int


class HealthResponse(BaseModel):
    robot_id: int

    temperature: float
    vibration: float
    motor_current: float
    torque: float

    health_score: float
    health_status: str