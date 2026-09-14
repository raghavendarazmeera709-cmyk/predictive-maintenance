from pathlib import Path

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)


# -----------------------------------
# 1. Load dataset
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR / "data" / "dataset_clean.xlsx"

df = pd.read_excel(DATA_PATH)

df.columns = df.columns.str.strip()


# -----------------------------------
# 2. Features and target
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


X = df[features]
y = df[target]


# -----------------------------------
# 3. Remove missing target values
# -----------------------------------

valid_rows = y.notna()

X = X[valid_rows]
y = y[valid_rows].astype(int)


# -----------------------------------
# 4. Train/Test split
# -----------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# -----------------------------------
# 5. Imputation
# -----------------------------------

imputer = SimpleImputer(strategy="median")

X_train = imputer.fit_transform(X_train)
X_test = imputer.transform(X_test)


# -----------------------------------
# 6. Train Random Forest
# -----------------------------------

model = RandomForestClassifier(
    n_estimators=200,
    class_weight="balanced",
    random_state=42
)

model.fit(X_train, y_train)


# -----------------------------------
# 7. Get probabilities
# -----------------------------------

probabilities = model.predict_proba(X_test)[:, 1]


# -----------------------------------
# 8. Test different thresholds
# -----------------------------------

thresholds = [
    0.30,
    0.35,
    0.40,
    0.45,
    0.50,
    0.55,
    0.60,
    0.65,
    0.70
]


print("\n==============================================")
print("       RANDOM FOREST THRESHOLD TUNING")
print("==============================================")

print(
    f"{'Threshold':<12}"
    f"{'Accuracy':<12}"
    f"{'Precision':<12}"
    f"{'Recall':<12}"
    f"{'F1':<12}"
)


for threshold in thresholds:

    y_pred = (
        probabilities >= threshold
    ).astype(int)

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

    print(
        f"{threshold:<12.2f}"
        f"{accuracy:<12.4f}"
        f"{precision:<12.4f}"
        f"{recall:<12.4f}"
        f"{f1:<12.4f}"
    )


# -----------------------------------
# 9. Detailed result for 0.40
# -----------------------------------

threshold = 0.40

y_pred = (
    probabilities >= threshold
).astype(int)


print("\n==============================================")
print("         CONFUSION MATRIX @ 0.40")
print("==============================================")

print(confusion_matrix(y_test, y_pred))