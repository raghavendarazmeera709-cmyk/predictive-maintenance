from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from backend.database.connection import Base


class Prediction(Base):
    __tablename__ = "predictions"

    prediction_id = Column(Integer, primary_key=True, autoincrement=True)

    robot_id = Column(
        Integer,
        ForeignKey("robot_arms.robot_id"),
        nullable=False
    )

    failure_probability = Column(Float, nullable=False)
    
    predicted_fault = Column(String(150))

    confidence = Column(Float)

    recommendation = Column(String(300))

    prediction_time = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    robot = relationship(
        "RobotArm",
        back_populates="predictions"
    )