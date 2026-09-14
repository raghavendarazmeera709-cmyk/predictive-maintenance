from sqlalchemy.orm import Session

from backend.models.maintenance import Maintenance
from backend.schemas.maintenance import (
    MaintenanceCreate,
    MaintenanceUpdate,
)


def create_maintenance(db: Session, maintenance: MaintenanceCreate):
    db_maintenance = Maintenance(**maintenance.model_dump())

    db.add(db_maintenance)
    db.commit()
    db.refresh(db_maintenance)

    return db_maintenance


def get_all_maintenance(db: Session):
    return db.query(Maintenance).all()


def get_maintenance_by_id(db: Session, maintenance_id: int):
    return (
        db.query(Maintenance)
        .filter(Maintenance.maintenance_id == maintenance_id)
        .first()
    )


def update_maintenance(
    db: Session,
    maintenance_id: int,
    maintenance: MaintenanceUpdate,
):
    db_maintenance = get_maintenance_by_id(db, maintenance_id)

    if not db_maintenance:
        return None

    update_data = maintenance.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_maintenance, key, value)

    db.commit()
    db.refresh(db_maintenance)

    return db_maintenance


def delete_maintenance(db: Session, maintenance_id: int):
    db_maintenance = get_maintenance_by_id(db, maintenance_id)

    if not db_maintenance:
        return False

    db.delete(db_maintenance)
    db.commit()

    return True