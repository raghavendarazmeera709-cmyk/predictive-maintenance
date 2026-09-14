from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class IncidentBase(BaseModel):
    robot_id: int
    incident_type: str
    severity: str
    description: Optional[str] = None
    resolved: bool = False


class IncidentCreate(IncidentBase):
    pass


class IncidentUpdate(BaseModel):
    incident_type: Optional[str] = None
    severity: Optional[str] = None
    description: Optional[str] = None
    resolved: Optional[bool] = None


class IncidentResponse(IncidentBase):
    incident_id: int
    incident_time: datetime

    model_config = ConfigDict(from_attributes=True)