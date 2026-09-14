from sqlalchemy.orm import Session

from backend.models.user import User
from backend.schemas.user import (
    UserCreate,
    UserUpdate,
)


def create_user(db: Session, user: UserCreate):
    db_user = User(**user.model_dump())

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_all_users(db: Session):
    return db.query(User).all()


def get_user_by_id(db: Session, user_id: int):
    return (
        db.query(User)
        .filter(User.user_id == user_id)
        .first()
    )


def update_user(
    db: Session,
    user_id: int,
    user: UserUpdate,
):
    db_user = get_user_by_id(db, user_id)

    if not db_user:
        return None

    update_data = user.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)

    return db_user


def delete_user(
    db: Session,
    user_id: int,
):
    db_user = get_user_by_id(db, user_id)

    if not db_user:
        return False

    db.delete(db_user)
    db.commit()

    return True