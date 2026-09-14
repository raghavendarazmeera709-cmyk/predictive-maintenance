from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database.connection import get_db

from backend.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
)

from backend.services.user_service import (
    create_user,
    get_all_users,
    get_user_by_id,
    update_user,
    delete_user,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Creates a new user record.",
    responses={
        201: {
            "description": "User created successfully"
        },
        400: {
            "description": "Invalid request data"
        }
    }
)
def add_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    return create_user(db, user)


@router.get(
    "/",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all users",
    description="Retrieves all user records.",
    responses={
        200: {
            "description": "Users retrieved successfully"
        }
    }
)
def fetch_users(
    db: Session = Depends(get_db),
):
    return get_all_users(db)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get user by ID",
    description="Retrieves a specific user by their ID.",
    responses={
        200: {
            "description": "User retrieved successfully"
        },
        404: {
            "description": "User not found"
        }
    }
)
def fetch_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Update user",
    description="Updates a specific user by their ID.",
    responses={
        200: {
            "description": "User updated successfully"
        },
        400: {
            "description": "Invalid request data"
        },
        404: {
            "description": "User not found"
        }
    }
)
def edit_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
):
    updated = update_user(
        db,
        user_id,
        user,
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return updated


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete user",
    description="Deletes a specific user by their ID.",
    responses={
        200: {"description": "User deleted successfully"},
        404: {"description": "User not found"}
    }
)
def remove_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_user(
        db,
        user_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return {
        "message": "User deleted successfully"
    }