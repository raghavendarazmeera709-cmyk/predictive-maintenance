from sqlalchemy.orm import Session

from backend.models.user import User
from backend.core.security import (
    verify_password,
    create_access_token,
    hash_password,
)


def authenticate_user(
    db: Session,
    email: str,
    password: str,
):
    # Find user by email
    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    # User doesn't exist
    if not user:
        return None

    # Password doesn't match
    if not verify_password(
        password,
        user.password_hash
    ):
        return None

    return user


def login_user(
    db: Session,
    email: str,
    password: str,
):
    user = authenticate_user(
        db,
        email,
        password,
    )

    if not user:
        return None

    access_token = create_access_token({
        "user_id": user.user_id,
        "email": user.email,
        "role": user.role,
    })

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.user_id,
        "full_name": user.full_name,
        "email": user.email,
        "role": user.role,
    }


def register_user(
    db: Session,
    full_name: str,
    email: str,
    password: str,
    confirm_password: str,
    phone: str | None = None,
):
    # Check passwords
    if password != confirm_password:
        return None, "Passwords do not match"

    # Check if email already exists
    existing_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing_user:
        return None, "Email already registered"

    # Hash password
    password_hash = hash_password(password)

    # Create user
    new_user = User(
        full_name=full_name,
        email=email,
        phone=phone,
        role="operator",
        password_hash=password_hash,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user, None