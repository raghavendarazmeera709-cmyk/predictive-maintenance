from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.schemas.health import HealthRequest, HealthResponse
from backend.services.health_service import calculate_health

router = APIRouter(
    prefix="/health",
    tags=["Health Monitoring"]
)

@router.post("/", response_model=HealthResponse)
def get_health(
    data: HealthRequest,
    db: Session = Depends(get_db)
):
    return calculate_health(db, data)