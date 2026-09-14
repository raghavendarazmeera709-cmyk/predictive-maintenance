import random
from datetime import datetime, timedelta

from faker import Faker
import pandas as pd
from pathlib import Path

from backend.database.connection import SessionLocal

from backend.models.robot_arm import RobotArm
from backend.models.sensor import Sensor
from backend.models.telemetry import Telemetry
from backend.models.prediction import Prediction
from backend.models.maintenance import Maintenance
from backend.models.incident import Incident
from backend.models.notification import Notification
from backend.models.user import User

fake = Faker()

db = SessionLocal()

# -----------------------------
# Number of Records
# -----------------------------

ROBOT_COUNT = 50
SENSOR_COUNT = 50
TELEMETRY_COUNT = 50
PREDICTION_COUNT = 50
MAINTENANCE_COUNT = 50
INCIDENT_COUNT = 50
NOTIFICATION_COUNT = 50
USER_COUNT = 50


# -----------------------------
# Seed Robots
# -----------------------------

def seed_robots():

    if db.query(RobotArm).count() > 0:
        print("Robots already exist")
        return

    manufacturers = [
        "ABB",
        "KUKA",
        "Fanuc",
        "Yaskawa",
        "Universal Robots",
        "Siemens"
    ]

    statuses = [
        "Active",
        "Maintenance",
        "Inactive"
    ]

    for i in range(ROBOT_COUNT):

        robot = RobotArm(

            robot_name=f"Robot-{i+1}",

            manufacturer=random.choice(manufacturers),

            model=f"Model-{random.randint(100,999)}",

            serial_number=f"RB{10000+i}",

            installation_date=fake.date_between(
                start_date="-5y",
                end_date="today"
            ),

            location=f"Assembly Line {random.randint(1,10)}",

            payload_capacity=round(
                random.uniform(5,50),
                2
            ),

            reach=round(
                random.uniform(1,4),
                2
            ),

            status=random.choice(statuses)

        )

        db.add(robot)

    db.commit()

    print(f"{ROBOT_COUNT} Robots Inserted")


# -----------------------------
# Seed Sensors
# -----------------------------

def seed_sensors():

    if db.query(Sensor).count() > 0:
        print("Sensors already exist")
        return

    robots = db.query(RobotArm).all()

    sensor_types = [
        "Temperature",
        "Vibration",
        "Current",
        "Voltage",
        "Humidity"
    ]

    manufacturers = [
        "Bosch",
        "Honeywell",
        "Siemens",
        "ABB",
        "Omron"
    ]

    units = {

        "Temperature":"°C",

        "Vibration":"mm/s",

        "Current":"A",

        "Voltage":"V",

        "Humidity":"%"

    }

    for i in range(SENSOR_COUNT):

        sensor_type = random.choice(sensor_types)

        sensor = Sensor(

            robot_id=random.choice(
                robots
            ).robot_id,

            sensor_name=f"{sensor_type} Sensor {i+1}",

            sensor_type=sensor_type,

            manufacturer=random.choice(
                manufacturers
            ),

            status="Active",

            unit=units[sensor_type]

        )

        db.add(sensor)

    db.commit()

    print(f"{SENSOR_COUNT} Sensors Inserted")

# -----------------------------
# Seed Telemetry
# -----------------------------

def seed_telemetry():

    if db.query(Telemetry).count() > 0:
        print("Telemetry already exists")
        return

    # Path to the real ML dataset
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_PATH = BASE_DIR / "ml" / "data" / "dataset_clean.xlsx"

    # Load dataset
    df = pd.read_excel(DATA_PATH)

    # Clean column names
    df.columns = df.columns.str.strip()

    # The exact 20 features used by the ML model
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

    # Make sure all required columns exist
    missing_columns = [
        column for column in features
        if column not in df.columns
    ]

    if missing_columns:
        print("Missing columns from dataset:")
        print(missing_columns)
        return

    robots = db.query(RobotArm).all()

    if not robots:
        print("No robots found. Seed robots first.")
        return

    telemetry_records = []

    # -----------------------------------
    # Insert dataset rows
    # -----------------------------------

    for index, row in df.iterrows():

        # Distribute dataset records across robots
        robot = robots[index % len(robots)]

        telemetry = Telemetry(
            robot_id=robot.robot_id,

            Current_J0=float(row["Current_J0"]),
            Temperature_T0=float(row["Temperature_T0"]),

            Current_J1=float(row["Current_J1"]),
            Temperature_J1=float(row["Temperature_J1"]),

            Current_J2=float(row["Current_J2"]),
            Temperature_J2=float(row["Temperature_J2"]),

            Current_J3=float(row["Current_J3"]),
            Temperature_J3=float(row["Temperature_J3"]),

            Current_J4=float(row["Current_J4"]),
            Temperature_J4=float(row["Temperature_J4"]),

            Current_J5=float(row["Current_J5"]),
            Temperature_J5=float(row["Temperature_J5"]),

            Speed_J0=float(row["Speed_J0"]),
            Speed_J1=float(row["Speed_J1"]),
            Speed_J2=float(row["Speed_J2"]),
            Speed_J3=float(row["Speed_J3"]),
            Speed_J4=float(row["Speed_J4"]),
            Speed_J5=float(row["Speed_J5"]),

            Tool_current=float(row["Tool_current"]),
            cycle=float(row["cycle"]),

            timestamp=datetime.now()
        )

        telemetry_records.append(telemetry)

    # Insert all records
    db.add_all(telemetry_records)
    db.commit()

    print(
        f"{len(telemetry_records)} real ML telemetry records inserted"
    )   
    
# -----------------------------
# Seed Predictions
# -----------------------------

def seed_predictions():

    if db.query(Prediction).count() > 0:
        print("Predictions already exist")
        return

    robots = db.query(RobotArm).all()

    faults = [

        "Bearing Wear",

        "Motor Overheating",

        "Voltage Fluctuation",

        "Excessive Vibration",

        "Gearbox Failure",

        "Normal Operation"

    ]

    recommendations = [

        "Replace Bearing",

        "Lubricate Gearbox",

        "Check Motor",

        "Inspect Wiring",

        "Monitor Robot",

        "No Action Required"

    ]

    for _ in range(PREDICTION_COUNT):

        prediction = Prediction(

            robot_id=random.choice(
                robots
            ).robot_id,

            failure_probability=round(
                random.uniform(0.01, 0.99),
                2
            ),

            predicted_fault=random.choice(
                faults
            ),

            confidence=round(
                random.uniform(0.70, 0.99),
                2
            ),

            recommendation=random.choice(
                recommendations
            ),

            prediction_time=fake.date_time_between(
                start_date="-30d",
                end_date="now"
            )

        )

        db.add(prediction)

    db.commit()

    print(f"{PREDICTION_COUNT} Predictions Inserted")
    
# -----------------------------
# Seed Maintenance
# -----------------------------

def seed_maintenance():

    if db.query(Maintenance).count() > 0:
        print("Maintenance already exists")
        return

    robots = db.query(RobotArm).all()

    maintenance_types = [
        "Preventive",
        "Corrective",
        "Inspection",
        "Calibration",
        "Emergency"
    ]

    technicians = [
        "Rahul Sharma",
        "Amit Verma",
        "Priya Singh",
        "Neha Gupta",
        "Rohit Kumar"
    ]

    remarks = [
        "Routine servicing completed",
        "Bearing replaced",
        "Motor cleaned",
        "Calibration successful",
        "Lubrication completed",
        "Inspection completed"
    ]

    for _ in range(MAINTENANCE_COUNT):

        maintenance = Maintenance(

            robot_id=random.choice(robots).robot_id,

            maintenance_type=random.choice(
                maintenance_types
            ),

            technician_name=random.choice(
                technicians
            ),

            maintenance_date=fake.date_between(
                start_date="-180d",
                end_date="today"
            ),

            next_due_date=fake.date_between(
                start_date="today",
                end_date="+180d"
            ),

            remarks=random.choice(remarks)

        )

        db.add(maintenance)

    db.commit()

    print(f"{MAINTENANCE_COUNT} Maintenance Records Inserted")
    
# -----------------------------
# Seed Incidents
# -----------------------------

def seed_incidents():

    if db.query(Incident).count() > 0:
        print("Incidents already exist")
        return

    robots = db.query(RobotArm).all()

    severities = [
        "Low",
        "Medium",
        "High",
        "Critical"
    ]

    incident_types = [
        "Motor Failure",
        "Bearing Wear",
        "Power Failure",
        "Sensor Failure",
        "Overheating",
        "Communication Error"
    ]

    descriptions = [
        "Unexpected shutdown during operation.",
        "Temperature exceeded safe limit.",
        "Abnormal vibration detected.",
        "Voltage fluctuation observed.",
        "Motor current exceeded threshold.",
        "Sensor communication lost."
    ]

    for _ in range(INCIDENT_COUNT):

        incident = Incident(

            robot_id=random.choice(
                robots
            ).robot_id,

            severity=random.choice(
                severities
            ),

            incident_type=random.choice(
                incident_types
            ),

            description=random.choice(
                descriptions
            ),

            resolved=random.choice(
                [True, False]
            ),

            incident_time=fake.date_time_between(
                start_date="-90d",
                end_date="now"
            )

        )

        db.add(incident)

    db.commit()

    print(f"{INCIDENT_COUNT} Incident Records Inserted")
    
# -----------------------------
# Seed Notifications
# -----------------------------

def seed_notifications():

    if db.query(Notification).count() > 0:
        print("Notifications already exist")
        return

    robots = db.query(RobotArm).all()

    alert_types = [
        "Temperature Alert",
        "Maintenance Reminder",
        "Voltage Alert",
        "Motor Alert",
        "Sensor Failure",
        "Prediction Alert"
    ]

    priorities = [
        "Low",
        "Medium",
        "High",
        "Critical"
    ]

    messages = [
        "Temperature exceeded threshold.",
        "Scheduled maintenance due.",
        "Motor current is unusually high.",
        "Sensor stopped responding.",
        "Prediction model detected possible failure.",
        "Voltage fluctuation detected."
    ]

    statuses = [
        "Unread",
        "Read"
    ]

    for _ in range(NOTIFICATION_COUNT):

        notification = Notification(

            robot_id=random.choice(robots).robot_id,

            alert_type=random.choice(alert_types),

            message=random.choice(messages),

            priority=random.choice(priorities),

            status=random.choice(statuses),

            created_at=fake.date_time_between(
                start_date="-30d",
                end_date="now"
            )

        )

        db.add(notification)

    db.commit()

    print(f"{NOTIFICATION_COUNT} Notifications Inserted")
    
# -----------------------------
# Seed Users
# -----------------------------

def seed_users():

    if db.query(User).count() > 0:
        print("Users already exist")
        return

    roles = [
        "Admin",
        "Technician",
        "Supervisor"
    ]

    for i in range(USER_COUNT):

        user = User(

            full_name=fake.name(),

            email=f"user{i+1}@factoryops.com",

            phone=fake.phone_number(),

            role=random.choice(roles),

            password_hash="admin123"

        )

        db.add(user)

    db.commit()

    print(f"{USER_COUNT} Users Inserted")
    
# -----------------------------
# Seed Database
# -----------------------------

def seed_database():

    print("\n==============================")
    print("Starting Database Seeding...")
    print("==============================\n")

    seed_robots()
    seed_sensors()
    seed_telemetry()
    seed_predictions()
    seed_maintenance()
    seed_incidents()
    seed_notifications()
    seed_users()

    print("\n==============================")
    print("Database Seeding Completed!")
    print("==============================\n")


if __name__ == "__main__":

    try:
        seed_database()

    finally:
        db.close()