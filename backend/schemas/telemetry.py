from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TelemetryBase(BaseModel):
    robot_id: int

    Current_J0: Optional[float] = None
    Temperature_T0: Optional[float] = None

    Current_J1: Optional[float] = None
    Temperature_J1: Optional[float] = None

    Current_J2: Optional[float] = None
    Temperature_J2: Optional[float] = None

    Current_J3: Optional[float] = None
    Temperature_J3: Optional[float] = None

    Current_J4: Optional[float] = None
    Temperature_J4: Optional[float] = None

    Current_J5: Optional[float] = None
    Temperature_J5: Optional[float] = None

    Speed_J0: Optional[float] = None
    Speed_J1: Optional[float] = None
    Speed_J2: Optional[float] = None
    Speed_J3: Optional[float] = None
    Speed_J4: Optional[float] = None
    Speed_J5: Optional[float] = None

    Tool_current: Optional[float] = None

    cycle: Optional[float] = None


class TelemetryCreate(TelemetryBase):
    pass


class TelemetryUpdate(BaseModel):
    Current_J0: Optional[float] = None
    Temperature_T0: Optional[float] = None

    Current_J1: Optional[float] = None
    Temperature_J1: Optional[float] = None

    Current_J2: Optional[float] = None
    Temperature_J2: Optional[float] = None

    Current_J3: Optional[float] = None
    Temperature_J3: Optional[float] = None

    Current_J4: Optional[float] = None
    Temperature_J4: Optional[float] = None

    Current_J5: Optional[float] = None
    Temperature_J5: Optional[float] = None

    Speed_J0: Optional[float] = None
    Speed_J1: Optional[float] = None
    Speed_J2: Optional[float] = None
    Speed_J3: Optional[float] = None
    Speed_J4: Optional[float] = None
    Speed_J5: Optional[float] = None

    Tool_current: Optional[float] = None

    cycle: Optional[float] = None


class TelemetryResponse(TelemetryBase):
    telemetry_id: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)