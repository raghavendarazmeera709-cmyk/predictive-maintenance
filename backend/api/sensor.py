from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.schemas.sensor import (
    SensorCreate,
    SensorUpdate,
    SensorResponse,
)
from backend.services.sensor_service import (
    create_sensor,
    get_all_sensors,
    get_sensor_by_id,
    update_sensor,
    delete_sensor,
)

router = APIRouter(
    prefix="/sensors",
    tags=["Sensors"]
)


@router.post(
    "/",
    response_model=SensorResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new sensor",
    description="Creates a new sensor record.",
    responses={
        201: {
            "description": "Sensor created successfully"
        },
        400: {
            "description": "Invalid request data"
        }
    }
)
def add_sensor(sensor: SensorCreate, db: Session = Depends(get_db)):
    return create_sensor(db, sensor)


@router.get(
    "/",
    response_model=list[SensorResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all sensors",
    description="Retrieves all sensor records.",
    responses={
        200: {
            "description": "Sensors retrieved successfully"
        }
    }
)
def fetch_all_sensors(db: Session = Depends(get_db)):
    return get_all_sensors(db)


@router.get(
    "/{sensor_id}",
    response_model=SensorResponse,
    status_code=status.HTTP_200_OK,
    summary="Get sensor by ID",
    description="Retrieves a specific sensor record by its ID.",
    responses={
        200: {
            "description": "Sensor retrieved successfully"
        },
        404: {
            "description": "Sensor not found"
        }
    }
)
def fetch_sensor(sensor_id: int, db: Session = Depends(get_db)):
    sensor = get_sensor_by_id(db, sensor_id)

    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")

    return sensor


@router.put(
    "/{sensor_id}",
    response_model=SensorResponse,
    status_code=status.HTTP_200_OK,
    summary="Update sensor",
    description="Updates an existing sensor.",
    responses={
        200: {
            "description": "Sensor updated successfully"
        },
        404: {
            "description": "Sensor not found"
        }
    }
)
def edit_sensor(
    sensor_id: int,
    sensor: SensorUpdate,
    db: Session = Depends(get_db),
):
    updated_sensor = update_sensor(db, sensor_id, sensor)

    if not updated_sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")

    return updated_sensor


@router.delete(
    "/{sensor_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete sensor",
    description="Deletes a sensor.",
    responses={
        200: {"description": "Sensor deleted successfully"},
        404: {"description": "Sensor not found"}
    }
)
def remove_sensor(sensor_id: int, db: Session = Depends(get_db)):
    deleted = delete_sensor(db, sensor_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Sensor not found")

    return {"message": "Sensor deleted successfully"}