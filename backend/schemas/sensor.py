from typing import Optional

from pydantic import BaseModel, ConfigDict


class SensorBase(BaseModel):
    robot_id: int
    sensor_name: str
    sensor_type: str
    manufacturer: Optional[str] = None
    status: str = "Active"
    unit: Optional[str] = None


class SensorCreate(SensorBase):
    pass


class SensorUpdate(BaseModel):
    sensor_name: Optional[str] = None
    sensor_type: Optional[str] = None
    manufacturer: Optional[str] = None
    status: Optional[str] = None
    unit: Optional[str] = None


class SensorResponse(SensorBase):
    sensor_id: int

    model_config = ConfigDict(from_attributes=True)