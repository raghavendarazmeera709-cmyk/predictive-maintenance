from sqlalchemy.orm import Session

from backend.models.telemetry import Telemetry
from backend.schemas.telemetry import (
    TelemetryCreate,
    TelemetryUpdate,
)


def create_telemetry(db: Session, telemetry: TelemetryCreate):
    db_telemetry = Telemetry(**telemetry.model_dump())

    db.add(db_telemetry)
    db.commit()
    db.refresh(db_telemetry)

    return db_telemetry


def get_all_telemetry(db: Session):
    return db.query(Telemetry).all()


def get_telemetry_by_id(db: Session, telemetry_id: int):
    return (
        db.query(Telemetry)
        .filter(Telemetry.telemetry_id == telemetry_id)
        .first()
    )


def update_telemetry(
    db: Session,
    telemetry_id: int,
    telemetry: TelemetryUpdate,
):
    db_telemetry = get_telemetry_by_id(db, telemetry_id)

    if not db_telemetry:
        return None

    update_data = telemetry.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_telemetry, key, value)

    db.commit()
    db.refresh(db_telemetry)

    return db_telemetry


def delete_telemetry(db: Session, telemetry_id: int):
    db_telemetry = get_telemetry_by_id(db, telemetry_id)

    if not db_telemetry:
        return False

    db.delete(db_telemetry)
    db.commit()

    return True

def get_latest_telemetry_by_robot(db: Session, robot_id: int):
    return (
        db.query(Telemetry)
        .filter(Telemetry.robot_id == robot_id)
        .order_by(Telemetry.telemetry_id.desc())
        .first()
    )
    
    