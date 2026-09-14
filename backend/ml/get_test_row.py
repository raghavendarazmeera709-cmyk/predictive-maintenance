import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR / "data" / "dataset_clean.xlsx"

df = pd.read_excel(DATA_PATH)

df.columns = df.columns.str.strip()

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

row = df.iloc[19]

print("\n========== ROW 19 ==========")
print("Actual Protective Stop:", row["Robot_ProtectiveStop"])

print("\nFeature values:")

for feature in features:
    print(f"{feature}: {row[feature]}")