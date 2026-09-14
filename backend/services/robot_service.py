from sqlalchemy.orm import Session

from backend.models.robot_arm import RobotArm
from backend.schemas.robot_arm import RobotArmCreate, RobotArmUpdate


def create_robot(db: Session, robot: RobotArmCreate):
    db_robot = RobotArm(**robot.model_dump())

    db.add(db_robot)
    db.commit()
    db.refresh(db_robot)

    return db_robot


def get_all_robots(db: Session):
    return db.query(RobotArm).all()


def get_robot_by_id(db: Session, robot_id: int):
    return db.query(RobotArm).filter(
        RobotArm.robot_id == robot_id
    ).first()


def update_robot(db: Session, robot_id: int, robot: RobotArmUpdate):

    db_robot = get_robot_by_id(db, robot_id)

    if not db_robot:
        return None

    update_data = robot.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_robot, key, value)

    db.commit()
    db.refresh(db_robot)

    return db_robot


def delete_robot(db: Session, robot_id: int):

    db_robot = get_robot_by_id(db, robot_id)

    if not db_robot:
        return False

    db.delete(db_robot)
    db.commit()

    return True