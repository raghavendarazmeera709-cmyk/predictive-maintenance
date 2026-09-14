import joblib
import pandas as pd

from pathlib import Path

from sklearn.model_selection import train_test_split

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)


# -----------------------------------
# 1. Paths
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR / "data" / "dataset_clean.xlsx"
MODEL_PATH = BASE_DIR / "model.pkl"


# -----------------------------------
# 2. Load model
# -----------------------------------

model_data = joblib.load(MODEL_PATH)

model = model_data["model"]
imputer = model_data["imputer"]
features = model_data["features"]
threshold = model_data["threshold"]


# -----------------------------------
# 3. Load dataset
# -----------------------------------

df = pd.read_excel(DATA_PATH)

df.columns = df.columns.str.strip()


# -----------------------------------
# 4. Create X and y
# -----------------------------------

X = df[features]
y = df["Robot_ProtectiveStop"]


# Remove missing target values
valid_rows = y.notna()

X = X[valid_rows]
y = y[valid_rows].astype(int)


# -----------------------------------
# 5. SAME train/test split
# -----------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# -----------------------------------
# 6. Apply saved imputer
# -----------------------------------

X_test = imputer.transform(X_test)


# -----------------------------------
# 7. Get probabilities
# -----------------------------------

probabilities = model.predict_proba(X_test)[:, 1]


# -----------------------------------
# 8. Apply saved threshold
# -----------------------------------

y_pred = (
    probabilities >= threshold
).astype(int)


# -----------------------------------
# 9. Evaluate
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


print("\n========================================")
print("       SAVED MODEL VERIFICATION")
print("========================================")

print("Threshold:", threshold)

print("\nAccuracy :", accuracy)
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