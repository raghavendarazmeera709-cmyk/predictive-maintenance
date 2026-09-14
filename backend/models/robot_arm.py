from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import relationship
from backend.database.connection import Base


class RobotArm(Base):
    __tablename__ = "robot_arms"

    robot_id = Column(Integer, primary_key=True, autoincrement=True)

    robot_name = Column(String(100), nullable=False)

    manufacturer = Column(String(100), nullable=False)

    model = Column(String(100), nullable=False)

    serial_number = Column(String(100), unique=True, nullable=False)

    installation_date = Column(Date)

    location = Column(String(150))

    payload_capacity = Column(Float)

    reach = Column(Float)

    status = Column(String(30), default="Active")

    sensors = relationship(
        "Sensor",
        back_populates="robot",
        cascade="all, delete-orphan"
    )

    telemetry_records = relationship(
        "Telemetry",
        back_populates="robot",
        cascade="all, delete-orphan"
    )

    predictions = relationship(
        "Prediction",
        back_populates="robot",
        cascade="all, delete-orphan"
    )

    maintenance_records = relationship(
        "Maintenance",
        back_populates="robot",
        cascade="all, delete-orphan"
    )

    incidents = relationship(
        "Incident",
        back_populates="robot",
        cascade="all, delete-orphan"
    )

    notifications = relationship(
        "Notification",
        back_populates="robot",
        cascade="all, delete-orphan"
    )