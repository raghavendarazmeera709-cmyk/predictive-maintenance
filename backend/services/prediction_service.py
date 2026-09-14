from sqlalchemy.orm import Session
from backend.models.prediction import Prediction
from backend.models.telemetry import Telemetry
from backend.schemas.prediction import (
    PredictionCreate,
    PredictionUpdate,
)
from backend.ml.predict import predict_protective_stop


def create_prediction(db: Session, prediction: PredictionCreate):
    db_prediction = Prediction(**prediction.model_dump())

    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)

    return db_prediction

def get_all_predictions(db: Session):
    return db.query(Prediction).all()


def get_prediction_by_id(db: Session, prediction_id: int):
    return (
        db.query(Prediction)
        .filter(Prediction.prediction_id == prediction_id)
        .first()
    )


def update_prediction(
    db: Session,
    prediction_id: int,
    prediction: PredictionUpdate,
):
    db_prediction = get_prediction_by_id(db, prediction_id)

    if not db_prediction:
        return None

    update_data = prediction.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_prediction, key, value)

    db.commit()
    db.refresh(db_prediction)

    return db_prediction


def delete_prediction(db: Session, prediction_id: int):
    db_prediction = get_prediction_by_id(db, prediction_id)

    if not db_prediction:
        return False

    db.delete(db_prediction)
    db.commit()

    return True

def predict_for_robot(db: Session, robot_id: int):

    # -----------------------------------
    # 1. Get latest telemetry for robot
    # -----------------------------------

    telemetry = (
        db.query(Telemetry)
        .filter(Telemetry.robot_id == robot_id)
        .order_by(Telemetry.telemetry_id.desc())
        .first()
    )

    if not telemetry:
        return None

    # -----------------------------------
    # 2. Extract the 20 ML features
    # -----------------------------------

    data = {
        "Current_J0": telemetry.Current_J0,
        "Temperature_T0": telemetry.Temperature_T0,

        "Current_J1": telemetry.Current_J1,
        "Temperature_J1": telemetry.Temperature_J1,

        "Current_J2": telemetry.Current_J2,
        "Temperature_J2": telemetry.Temperature_J2,

        "Current_J3": telemetry.Current_J3,
        "Temperature_J3": telemetry.Temperature_J3,

        "Current_J4": telemetry.Current_J4,
        "Temperature_J4": telemetry.Temperature_J4,

        "Current_J5": telemetry.Current_J5,
        "Temperature_J5": telemetry.Temperature_J5,

        "Speed_J0": telemetry.Speed_J0,
        "Speed_J1": telemetry.Speed_J1,
        "Speed_J2": telemetry.Speed_J2,
        "Speed_J3": telemetry.Speed_J3,
        "Speed_J4": telemetry.Speed_J4,
        "Speed_J5": telemetry.Speed_J5,

        "Tool_current": telemetry.Tool_current,
        "cycle": telemetry.cycle,
    }

    # -----------------------------------
    # 3. Run ML prediction
    # -----------------------------------

    result = predict_protective_stop(data)

    # -----------------------------------
    # 4. Convert prediction into text
    # -----------------------------------

    if result["prediction"] == 1:
        predicted_fault = "Robot Protective Stop"
        recommendation = "Inspect robot telemetry and joint conditions."
    else:
        predicted_fault = "Normal"
        recommendation = "No immediate action required."

    # -----------------------------------
    # 5. Save prediction
    # -----------------------------------

    prediction = Prediction(
        robot_id=robot_id,
        failure_probability=result["probability"],
        predicted_fault=predicted_fault,
        recommendation=recommendation,
    )

    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    return prediction