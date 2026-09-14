from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database.connection import get_db

from backend.schemas.notification import (
    NotificationCreate,
    NotificationUpdate,
    NotificationResponse,
)

from backend.services.notification_service import (
    create_notification,
    get_all_notifications,
    get_notification_by_id,
    update_notification,
    delete_notification,
)

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


@router.post(
    "/",
    response_model=NotificationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create notification",
    description="Creates a new notification.",
    responses={
        201: {
            "description": "Notification created successfully"
        },
        400: {
            "description": "Invalid request data"
        }
    }
)
def add_notification(
    notification: NotificationCreate,
    db: Session = Depends(get_db),
):
    return create_notification(db, notification)


@router.get(
    "/",
    response_model=list[NotificationResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all notifications",
    description="Retrieves all notifications.",
    responses={
        200: {
            "description": "Notifications retrieved successfully"
        }
    }
)
def fetch_notifications(
    db: Session = Depends(get_db),
):
    return get_all_notifications(db)


@router.get(
    "/{notification_id}",
    response_model=NotificationResponse,
    status_code=status.HTTP_200_OK,
    summary="Get notification by ID",
    description="Retrieves a specific notification by its ID.",
    responses={
        200: {
            "description": "Notification retrieved successfully"
        },
        404: {
            "description": "Notification not found"
        }
    }
)
def fetch_notification(
    notification_id: int,
    db: Session = Depends(get_db),
):
    notification = get_notification_by_id(
        db,
        notification_id,
    )

    if not notification:
        raise HTTPException(
            status_code=404,
            detail="Notification not found",
        )

    return notification


@router.put(
    "/{notification_id}",
    response_model=NotificationResponse,
    status_code=status.HTTP_200_OK,
    summary="Update notification",
    description="Updates a specific notification by its ID.",
    responses={
        200: {
            "description": "Notification updated successfully"
        },
        400: {
            "description": "Invalid request data"
        },
        404: {
            "description": "Notification not found"
        }
    }
)
def edit_notification(
    notification_id: int,
    notification: NotificationUpdate,
    db: Session = Depends(get_db),
):
    updated = update_notification(
        db,
        notification_id,
        notification,
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Notification not found",
        )

    return updated


@router.delete(
    "/{notification_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete notification",
    description="Deletes a specific notification by its ID.",
    responses={
        200: {"description": "Notification deleted successfully"},
        404: {"description": "Notification not found"}
    }
)
def remove_notification(
    notification_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_notification(
        db,
        notification_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Notification not found",
        )

    return {
        "message": "Notification deleted successfully"
    }