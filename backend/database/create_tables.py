from backend.database.connection import Base, engine

# Import all models so SQLAlchemy registers them
from backend.models import (
    RobotArm,
    Sensor,
    Telemetry,
    Prediction,
    Maintenance,
    Incident,
    Notification,
    User,
)



def create_tables():
    """
    Create all database tables.
    """
    Base.metadata.create_all(bind=engine)
    print(" All database tables created successfully!")


if __name__ == "__main__":
    create_tables()
    
    