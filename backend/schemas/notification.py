from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class NotificationBase(BaseModel):
    robot_id: int
    alert_type: str
    message: str
    priority: str
    status: str = "Unread"


class NotificationCreate(NotificationBase):
    pass


class NotificationUpdate(BaseModel):
    alert_type: Optional[str] = None
    message: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None


class NotificationResponse(NotificationBase):
    notification_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)