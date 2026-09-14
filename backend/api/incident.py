from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.schemas.incident import (
    IncidentCreate,
    IncidentUpdate,
    IncidentResponse,
)
from backend.services.incident_service import (
    create_incident,
    get_all_incidents,
    get_incident_by_id,
    update_incident,
    delete_incident,
)

router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"]
)


@router.post(
    "/",
    response_model=IncidentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new incident",
    description="Creates a new incident record for a robot arm.",
    responses={
        201: {
            "description": "Incident created successfully"
        },
        400: {
            "description": "Invalid request data"
        },
        404: {
            "description": "Robot not found"
        }
    }
)
def add_incident(
    incident: IncidentCreate,
    db: Session = Depends(get_db),
):
    return create_incident(db, incident)


@router.get(
    "/",
    response_model=list[IncidentResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all incidents",
    description="Retrieves all incident records.",
    responses={
        200: {
            "description": "Incidents retrieved successfully"
        }
    }
)
def fetch_all_incidents(db: Session = Depends(get_db)):
    return get_all_incidents(db)


@router.get(
    "/{incident_id}",
    response_model=IncidentResponse,
    status_code=status.HTTP_200_OK,
    summary="Get incident by ID",
    description="Retrieves a specific incident record by its ID.",
    responses={
        200: {
            "description": "Incident retrieved successfully"
        },
        404: {
            "description": "Incident not found"
        }
    }
)
def fetch_incident(
    incident_id: int,
    db: Session = Depends(get_db),
):
    incident = get_incident_by_id(db, incident_id)

    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    return incident


@router.put(
    "/{incident_id}",
    response_model=IncidentResponse,
    status_code=status.HTTP_200_OK,
    summary="Update incident",
    description="Updates an existing incident.",
    responses={
        200: {
            "description": "Incident updated successfully"
        },
        404: {
            "description": "Incident not found"
        }
    }
)
def edit_incident(
    incident_id: int,
    incident: IncidentUpdate,
    db: Session = Depends(get_db),
):
    updated = update_incident(db, incident_id, incident)

    if not updated:
        raise HTTPException(status_code=404, detail="Incident not found")

    return updated


@router.delete(
    "/{incident_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete incident",
    description="Deletes an existing incident.",
    responses={
        200: {
            "description": "Incident deleted successfully"
        },
        404: {
            "description": "Incident not found"
        }
    }
)
def remove_incident(
    incident_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_incident(db, incident_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Incident not found")

    return {
    "status": "success",
    "message": "Incident deleted successfully"
    }