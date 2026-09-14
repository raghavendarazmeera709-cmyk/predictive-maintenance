from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from backend.database.connection import Base


class Sensor(Base):
    __tablename__ = "sensors"

    sensor_id = Column(Integer, primary_key=True, autoincrement=True)

    robot_id = Column(
        Integer,
        ForeignKey("robot_arms.robot_id"),
        nullable=False
    )

    sensor_name = Column(String(100), nullable=False)

    sensor_type = Column(String(100), nullable=False)

    manufacturer = Column(String(100))

    status = Column(String(30), default="Active")

    unit = Column(String(30))

    robot = relationship(
        "RobotArm",
        back_populates="sensors"
    )