from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class PredictionBase(BaseModel):
    robot_id: int
    failure_probability: float
    predicted_fault: str
    recommendation: Optional[str] = None

class PredictionCreate(PredictionBase):
    pass


class PredictionUpdate(BaseModel):
    failure_probability: Optional[float] = None
    predicted_fault: Optional[str] = None
    recommendation: Optional[str] = None


class PredictionResponse(PredictionBase):
    prediction_id: int
  
    prediction_time: datetime

    model_config = ConfigDict(from_attributes=True)
    
class MLPredictionRequest(BaseModel):
    robot_id: int

    Current_J0: float
    Temperature_T0: float

    Current_J1: float
    Temperature_J1: float

    Current_J2: float
    Temperature_J2: float

    Current_J3: float
    Temperature_J3: float

    Current_J4: float
    Temperature_J4: float

    Current_J5: float
    Temperature_J5: float

    Speed_J0: float
    Speed_J1: float
    Speed_J2: float
    Speed_J3: float
    Speed_J4: float
    Speed_J5: float

    Tool_current: float
    cycle: float
    