from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from backend.database.connection import Base


class Maintenance(Base):
    __tablename__ = "maintenance"

    maintenance_id = Column(Integer, primary_key=True, autoincrement=True)

    robot_id = Column(
        Integer,
        ForeignKey("robot_arms.robot_id"),
        nullable=False
    )

    maintenance_type = Column(String(100), nullable=False)

    technician_name = Column(String(100), nullable=False)

    maintenance_date = Column(Date)

    next_due_date = Column(Date)

    remarks = Column(String(300))

    robot = relationship(
        "RobotArm",
        back_populates="maintenance_records"
    )