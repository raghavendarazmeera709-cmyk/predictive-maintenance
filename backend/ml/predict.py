from pathlib import Path

import joblib
import pandas as pd


# -----------------------------------
# 1. Load trained model
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "model.pkl"

model_data = joblib.load(MODEL_PATH)

model = model_data["model"]
imputer = model_data["imputer"]
features = model_data["features"]
threshold = model_data["threshold"]


# -----------------------------------
# 2. Prediction function
# -----------------------------------

def predict_protective_stop(data: dict):

    # Convert input dictionary into DataFrame
    input_data = pd.DataFrame([data])

    # Make sure features are in the same order
    input_data = input_data[features]

    # Apply the same preprocessing used during training
    input_data = imputer.transform(input_data)

    # Get probability of protective stop
    probability = model.predict_proba(input_data)[0][1]

    # Apply threshold
    prediction = int(probability >= threshold)

    return {
        "prediction": prediction,
        "protective_stop": prediction == 1,
        "probability": float(probability),
        "threshold": threshold
    }


# -----------------------------------
# 3. Test prediction
# -----------------------------------

if __name__ == "__main__":

    # -----------------------------------
    # Load real dataset
    # -----------------------------------

    DATA_PATH = BASE_DIR / "data" / "dataset_clean.xlsx"

    df = pd.read_excel(DATA_PATH)

    df.columns = df.columns.str.strip()


    # -----------------------------------
    # Select a real row
    # -----------------------------------

    row_index = df[df["Robot_ProtectiveStop"] == 1].index[0]

    row = df.iloc[row_index]


    # -----------------------------------
    # Get actual target value
    # -----------------------------------

    actual_value = int(row["Robot_ProtectiveStop"])


    # -----------------------------------
    # Get feature values
    # -----------------------------------

    sample_data = {}

    for feature in features:
        sample_data[feature] = row[feature]


    # -----------------------------------
    # Make prediction
    # -----------------------------------

    result = predict_protective_stop(sample_data)


    # -----------------------------------
    # Display results
    # -----------------------------------

    print("\n========== REAL DATASET PREDICTION ==========")

    print("Row index:", row_index)

    print("\nActual value:")
    print("Robot Protective Stop:", actual_value)

    print("\nModel prediction:")
    print("Prediction:", result["prediction"])
    print("Protective Stop:", result["protective_stop"])
    print("Probability:", result["probability"])
    print("Threshold:", result["threshold"])


    # -----------------------------------
    # Compare prediction with actual value
    # -----------------------------------

    if result["prediction"] == actual_value:
        print("\nResult: CORRECT prediction")
    else:
        print("\nResult: INCORRECT prediction")