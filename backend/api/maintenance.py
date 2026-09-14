from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.schemas.maintenance import (
    MaintenanceCreate,
    MaintenanceUpdate,
    MaintenanceResponse,
)
from backend.services.maintenance_service import (
    create_maintenance,
    get_all_maintenance,
    get_maintenance_by_id,
    update_maintenance,
    delete_maintenance,
)

router = APIRouter(
    prefix="/maintenance",
    tags=["Maintenance"]
)


@router.post(
    "/",
    response_model=MaintenanceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create maintenance record",
    description="Creates a new maintenance record.",
    responses={
        201: {
            "description": "Maintenance record created successfully"
        },
        400: {
            "description": "Invalid request data"
        }
    }
)
def add_maintenance(
    maintenance: MaintenanceCreate,
    db: Session = Depends(get_db),
):
    return create_maintenance(db, maintenance)


@router.get(
    "/",
    response_model=list[MaintenanceResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all maintenance records",
    description="Retrieves all maintenance records.",
    responses={
        200: {
            "description": "Maintenance records retrieved successfully"
        }
    }
)
def fetch_all_maintenance(db: Session = Depends(get_db)):
    return get_all_maintenance(db)


@router.get(
    "/{maintenance_id}",
    response_model=MaintenanceResponse,
    status_code=status.HTTP_200_OK,
    summary="Get maintenance record by ID",
    description="Retrieves a specific maintenance record by its ID.",
    responses={
        200: {
            "description": "Maintenance record retrieved successfully"
        },
        404: {
            "description": "Maintenance record not found"
        }
    }
)
def fetch_maintenance(
    maintenance_id: int,
    db: Session = Depends(get_db),
):
    maintenance = get_maintenance_by_id(db, maintenance_id)

    if not maintenance:
        raise HTTPException(status_code=404, detail="Maintenance record not found")

    return maintenance


@router.put(
    "/{maintenance_id}",
    response_model=MaintenanceResponse,
    status_code=status.HTTP_200_OK,
    summary="Update maintenance record",
    description="Updates a specific maintenance record by its ID.",
    responses={
        200: {
            "description": "Maintenance record updated successfully"
        },
        400: {
            "description": "Invalid request data"
        },
        404: {
            "description": "Maintenance record not found"
        }
    }
)
def edit_maintenance(
    maintenance_id: int,
    maintenance: MaintenanceUpdate,
    db: Session = Depends(get_db),
):
    updated = update_maintenance(db, maintenance_id, maintenance)

    if not updated:
        raise HTTPException(status_code=404, detail="Maintenance record not found")

    return updated


@router.delete(
    "/{maintenance_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete maintenance record",
    description="Deletes a specific maintenance record by its ID.",
    responses={
        200: {"description": "Maintenance record deleted successfully"},
        404: {"description": "Maintenance record not found"}
    }
)
def remove_maintenance(
    maintenance_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_maintenance(db, maintenance_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Maintenance record not found")

    return {"message": "Maintenance record deleted successfully"}