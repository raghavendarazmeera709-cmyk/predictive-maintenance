from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class RobotArmBase(BaseModel):
    robot_name: str
    manufacturer: str
    model: str
    serial_number: str
    installation_date: Optional[date] = None
    location: Optional[str] = None
    payload_capacity: Optional[float] = None
    reach: Optional[float] = None
    status: str = "Active"


class RobotArmCreate(RobotArmBase):
    pass


class RobotArmUpdate(BaseModel):
    robot_name: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    installation_date: Optional[date] = None
    location: Optional[str] = None
    payload_capacity: Optional[float] = None
    reach: Optional[float] = None
    status: Optional[str] = None


class RobotArmResponse(RobotArmBase):
    robot_id: int

    model_config = ConfigDict(from_attributes=True)
    