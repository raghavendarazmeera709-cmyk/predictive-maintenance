from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.schemas.prediction import (
    PredictionCreate,
    PredictionUpdate,
    PredictionResponse,
    MLPredictionRequest
)

from backend.ml.predict import predict_protective_stop

from backend.services.prediction_service import (
    create_prediction,
    get_all_predictions,
    get_prediction_by_id,
    update_prediction,
    delete_prediction,
    predict_for_robot,
    
)

router = APIRouter(
    prefix="/predictions",
    tags=["Predictions"]
)


@router.post(
    "/",
    response_model=PredictionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new prediction",
    description="Creates a new prediction record.",
    responses={
        201: {
            "description": "Prediction created successfully"
        },
        400: {
            "description": "Invalid request data"
        }
    }
)
def add_prediction(
    prediction: PredictionCreate,
    db: Session = Depends(get_db)
):
    return create_prediction(db, prediction)

@router.post(
    "/ml",
    response_model=PredictionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate ML prediction",
    description="Uses the trained Random Forest model to predict a robot protective stop."
)
def generate_ml_prediction(
    data: MLPredictionRequest,
    db: Session = Depends(get_db)
):

    # Convert request data to dictionary
    sensor_data = data.model_dump()

    # robot_id is not an ML feature
    robot_id = sensor_data.pop("robot_id")

    # Run Random Forest
    result = predict_protective_stop(sensor_data)

    # Determine predicted fault
    if result["prediction"] == 1:
        predicted_fault = "Robot Protective Stop"
        recommendation = (
            "Inspect robot operating conditions and joint parameters."
        )
    else:
        predicted_fault = "No Protective Stop"
        recommendation = (
            "Robot operating conditions appear normal."
        )

    # Create prediction object
    prediction = PredictionCreate(
        robot_id=robot_id,
        failure_probability=result["probability"],
        predicted_fault=predicted_fault,
        recommendation=recommendation
    )

    # Save to database
    return create_prediction(db, prediction)

@router.post(
    "/robot/{robot_id}",
    response_model=PredictionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate prediction for a robot",
    description="Gets the latest telemetry for a robot and generates an ML prediction."
)
def generate_robot_prediction(
    robot_id: int,
    db: Session = Depends(get_db)
):
    prediction = predict_for_robot(db, robot_id)

    if not prediction:
        raise HTTPException(
            status_code=404,
            detail="No telemetry found for this robot"
        )

    return prediction


@router.get(
    "/",
    response_model=list[PredictionResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all predictions",
    description="Retrieves all prediction records.",
    responses={
        200: {
            "description": "Predictions retrieved successfully"
        }
    }
)
def fetch_all_predictions(db: Session = Depends(get_db)):
    return get_all_predictions(db)


@router.get(
    "/{prediction_id}",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Get prediction by ID",
    description="Retrieves a specific prediction by its ID.",
    responses={
        200: {
            "description": "Prediction retrieved successfully"
        },
        404: {
            "description": "Prediction not found"
        }
    }
)
def fetch_prediction(
    prediction_id: int,
    db: Session = Depends(get_db)
):
    prediction = get_prediction_by_id(db, prediction_id)

    if not prediction:
        raise HTTPException(
            status_code=404,
            detail="Prediction not found"
        )

    return prediction


@router.put(
    "/{prediction_id}",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Update prediction",
    description="Updates a specific prediction by its ID.",
    responses={
        200: {
            "description": "Prediction updated successfully"
        },
        400: {
            "description": "Invalid request data"
        },
        404: {
            "description": "Prediction not found"
        }
    }
)
def edit_prediction(
    prediction_id: int,
    prediction: PredictionUpdate,
    db: Session = Depends(get_db)
):
    updated = update_prediction(
        db,
        prediction_id,
        prediction
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Prediction not found"
        )

    return updated


@router.delete(
    "/{prediction_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete prediction",
    description="Deletes a specific prediction by its ID.",
    responses={
        200: {"description": "Prediction deleted successfully"},
        404: {"description": "Prediction not found"}
    }
)
def remove_prediction(
    prediction_id: int,
    db: Session = Depends(get_db)
):
    deleted = delete_prediction(db, prediction_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Prediction not found"
        )

    return {
        "message": "Prediction deleted successfully"
    }