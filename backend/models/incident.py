from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from backend.database.connection import Base


class Incident(Base):
    __tablename__ = "incidents"

    incident_id = Column(Integer, primary_key=True, autoincrement=True)

    robot_id = Column(
        Integer,
        ForeignKey("robot_arms.robot_id"),
        nullable=False
    )

    severity = Column(String(30), nullable=False)

    incident_type = Column(String(100), nullable=False)

    description = Column(String(300))

    resolved = Column(Boolean, default=False)

    incident_time = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    robot = relationship(
        "RobotArm",
        back_populates="incidents"
    )