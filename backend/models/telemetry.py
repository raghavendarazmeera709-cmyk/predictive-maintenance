from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from backend.database.connection import Base


class Telemetry(Base):
    __tablename__ = "telemetry"

    telemetry_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    robot_id = Column(
        Integer,
        ForeignKey("robot_arms.robot_id"),
        nullable=False
    )

    # -----------------------------------
    # ML Robot Telemetry Features
    # -----------------------------------

    Current_J0 = Column(Float)
    Temperature_T0 = Column(Float)

    Current_J1 = Column(Float)
    Temperature_J1 = Column(Float)

    Current_J2 = Column(Float)
    Temperature_J2 = Column(Float)

    Current_J3 = Column(Float)
    Temperature_J3 = Column(Float)

    Current_J4 = Column(Float)
    Temperature_J4 = Column(Float)

    Current_J5 = Column(Float)
    Temperature_J5 = Column(Float)

    Speed_J0 = Column(Float)
    Speed_J1 = Column(Float)
    Speed_J2 = Column(Float)
    Speed_J3 = Column(Float)
    Speed_J4 = Column(Float)
    Speed_J5 = Column(Float)

    Tool_current = Column(Float)

    cycle = Column(Float)

    # -----------------------------------
    # Timestamp
    # -----------------------------------

    timestamp = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    # -----------------------------------
    # Relationship
    # -----------------------------------

    robot = relationship(
        "RobotArm",
        back_populates="telemetry_records"
    )