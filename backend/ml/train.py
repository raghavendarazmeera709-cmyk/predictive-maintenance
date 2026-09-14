import pandas as pd
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)


# -----------------------------------
# 1. Load dataset
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR / "data" / "dataset_clean.xlsx"

df = pd.read_excel(DATA_PATH)

print(df.shape)
print(df.columns.tolist())


# -----------------------------------
# 2. Clean column names
# -----------------------------------

df.columns = df.columns.str.strip()


# -----------------------------------
# 3. Select features
# -----------------------------------

features = [
    "Current_J0",
    "Temperature_T0",
    "Current_J1",
    "Temperature_J1",
    "Current_J2",
    "Temperature_J2",
    "Current_J3",
    "Temperature_J3",
    "Current_J4",
    "Temperature_J4",
    "Current_J5",
    "Temperature_J5",
    "Speed_J0",
    "Speed_J1",
    "Speed_J2",
    "Speed_J3",
    "Speed_J4",
    "Speed_J5",
    "Tool_current",
    "cycle"
]

target = "Robot_ProtectiveStop"


# -----------------------------------
# 4. Create X and y
# -----------------------------------

X = df[features]
y = df[target]


# -----------------------------------
# 5. Remove rows where target is missing
# -----------------------------------

valid_rows = y.notna()

X = X[valid_rows]
y = y[valid_rows]


# -----------------------------------
# 6. Convert target to integer
# -----------------------------------

y = y.astype(int)


print("\nTarget distribution:")
print(y.value_counts())


# -----------------------------------
# 7. Train/Test split
# -----------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# -----------------------------------
# 8. Handle missing feature values
# -----------------------------------

imputer = SimpleImputer(strategy="median")


# IMPORTANT:
# Fit imputer ONLY on training data

X_train = imputer.fit_transform(X_train)

# Use the already fitted imputer on test data

X_test = imputer.transform(X_test)


# -----------------------------------
# 9. Create Random Forest
# -----------------------------------

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)


# -----------------------------------
# 10. Train model
# -----------------------------------

model.fit(X_train, y_train)


# -----------------------------------
# 11. Make predictions
# -----------------------------------

y_pred = model.predict(X_test)


# -----------------------------------
# 12. Evaluate model
# -----------------------------------

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)


print("\n========== MODEL RESULTS ==========")

print("Accuracy :", accuracy)
print("Precision:", precision)
print("Recall   :", recall)
print("F1 Score :", f1)


print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)


print("\nConfusion Matrix:")

print(
    confusion_matrix(
        y_test,
        y_pred
    )
)


# -----------------------------------
# 13. Feature importance
# -----------------------------------

importance = pd.DataFrame({
    "feature": features,
    "importance": model.feature_importances_
})

importance = importance.sort_values(
    by="importance",
    ascending=False
)


print("\nFeature Importance:")

print(importance)


# -----------------------------------
# 14. Save model + preprocessing
# -----------------------------------

MODEL_PATH = BASE_DIR / "model.pkl"


model_data = {
    "model": model,
    "imputer": imputer,
    "features": features,
    "threshold": 0.50
}


joblib.dump(
    model_data,
    MODEL_PATH
)


print(f"\nModel saved to: {MODEL_PATH}")