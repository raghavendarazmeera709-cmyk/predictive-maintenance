from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from backend.database.connection import Base


class Notification(Base):
    __tablename__ = "notifications"

    notification_id = Column(Integer, primary_key=True, autoincrement=True)

    robot_id = Column(
        Integer,
        ForeignKey("robot_arms.robot_id"),
        nullable=False
    )

    alert_type = Column(String(100), nullable=False)

    message = Column(String(300), nullable=False)

    priority = Column(String(30), nullable=False)

    status = Column(String(30), default="Unread")

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    robot = relationship(
        "RobotArm",
        back_populates="notifications"
    )
    