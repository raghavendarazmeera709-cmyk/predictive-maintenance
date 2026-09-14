from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class MaintenanceBase(BaseModel):
    robot_id: int
    maintenance_type: str
    technician_name: str
    maintenance_date: date
    next_due_date: Optional[date] = None
    remarks: Optional[str] = None


class MaintenanceCreate(MaintenanceBase):
    pass


class MaintenanceUpdate(BaseModel):
    maintenance_type: Optional[str] = None
    technician_name: Optional[str] = None
    maintenance_date: Optional[date] = None
    next_due_date: Optional[date] = None
    remarks: Optional[str] = None


class MaintenanceResponse(MaintenanceBase):
    maintenance_id: int

    model_config = ConfigDict(from_attributes=True)