from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.schemas.telemetry import (
    TelemetryCreate,
    TelemetryUpdate,
    TelemetryResponse,
)
from backend.services.telemetry_service import (
    create_telemetry,
    get_all_telemetry,
    get_telemetry_by_id,
    update_telemetry,
    delete_telemetry,
    get_latest_telemetry_by_robot,
    
)

router = APIRouter(
    prefix="/telemetry",
    tags=["Telemetry"]
)


@router.post(
    "/",
    response_model=TelemetryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new telemetry record",
    description="Creates a new telemetry record.",
    responses={
        201: {
            "description": "Telemetry created successfully"
        },
        400: {
            "description": "Invalid request data"
        }
    }
)
def add_telemetry(
    telemetry: TelemetryCreate,
    db: Session = Depends(get_db)
):
    return create_telemetry(db, telemetry)


@router.get(
    "/",
    response_model=list[TelemetryResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all telemetry records",
    description="Retrieves all telemetry records.",
    responses={
        200: {
            "description": "Telemetry records retrieved successfully"
        }
    }
)
def fetch_all_telemetry(db: Session = Depends(get_db)):
    return get_all_telemetry(db)

@router.get(
    "/robot/{robot_id}/latest",
    response_model=TelemetryResponse,
    status_code=status.HTTP_200_OK,
    summary="Get latest telemetry for a robot",
    description="Retrieves the latest telemetry record for a specific robot.",
    responses={
        200: {
            "description": "Latest telemetry retrieved successfully"
        },
        404: {
            "description": "Telemetry not found for this robot"
        }
    }
)
def fetch_latest_robot_telemetry(
    robot_id: int,
    db: Session = Depends(get_db)
):
    telemetry = get_latest_telemetry_by_robot(db, robot_id)

    if not telemetry:
        raise HTTPException(
            status_code=404,
            detail="No telemetry found for this robot"
        )

    return telemetry


@router.get(
    "/{telemetry_id}",
    response_model=TelemetryResponse,
    status_code=status.HTTP_200_OK,
    summary="Get telemetry by ID",
    description="Retrieves a specific telemetry record by its ID.",
    responses={
        200: {
            "description": "Telemetry retrieved successfully"
        },
        404: {
            "description": "Telemetry not found"
        }
    }
)
def fetch_telemetry(
    telemetry_id: int,
    db: Session = Depends(get_db)
):
    telemetry = get_telemetry_by_id(db, telemetry_id)

    if not telemetry:
        raise HTTPException(
            status_code=404,
            detail="Telemetry not found"
        )

    return telemetry


@router.put(
    "/{telemetry_id}",
    response_model=TelemetryResponse,
    status_code=status.HTTP_200_OK,
    summary="Update telemetry",
    description="Updates a specific telemetry record by its ID.",
    responses={
        200: {
            "description": "Telemetry updated successfully"
        },
        400: {
            "description": "Invalid request data"
        },
        404: {
            "description": "Telemetry not found"
        }
    }
)
def edit_telemetry(
    telemetry_id: int,
    telemetry: TelemetryUpdate,
    db: Session = Depends(get_db)
):
    updated = update_telemetry(db, telemetry_id, telemetry)

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Telemetry not found"
        )

    return updated


@router.delete(
    "/{telemetry_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete telemetry",
    description="Deletes a specific telemetry record by its ID.",
    responses={
        200: {"description": "Telemetry deleted successfully"},
        404: {"description": "Telemetry not found"}
    }
)
def remove_telemetry(
    telemetry_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_telemetry(db, telemetry_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Telemetry not found"
        )

    return {"message": "Telemetry deleted successfully"}