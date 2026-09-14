from pathlib import Path

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)


# -----------------------------------
# 1. Load dataset
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR / "data" / "dataset_clean.xlsx"

df = pd.read_excel(DATA_PATH)

df.columns = df.columns.str.strip()

print("Dataset shape:", df.shape)


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


print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))


# -----------------------------------
# 5. Fit imputer ONLY on training data
# -----------------------------------

imputer = SimpleImputer(strategy="median")

X_train = imputer.fit_transform(X_train)

X_test = imputer.transform(X_test)


# -----------------------------------
# 6. Define models
# -----------------------------------

models = {

    "Logistic Regression": LogisticRegression(
        max_iter=2000,
        class_weight="balanced",
        random_state=42
    ),

    "Decision Tree": DecisionTreeClassifier(
        max_depth=10,
        class_weight="balanced",
        random_state=42
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=200,
        class_weight="balanced",
        random_state=42
    )
}


# -----------------------------------
# 7. Train and evaluate
# -----------------------------------

results = []


for name, model in models.items():

    print(f"\nTraining {name}...")

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    y_probability = model.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, y_pred)

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

    roc_auc = roc_auc_score(
        y_test,
        y_probability
    )

    results.append({
        "Model": name,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1,
        "ROC-AUC": roc_auc
    })


# -----------------------------------
# 8. Display comparison
# -----------------------------------

results_df = pd.DataFrame(results)

print("\n========================================")
print("             MODEL COMPARISON")
print("========================================")

print(
    results_df.to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}"
    )
)