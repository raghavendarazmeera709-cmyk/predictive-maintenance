from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from backend.core.config import settings

# Database URL
DATABASE_URL = settings.DATABASE_URL

# Create database engine
engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False}
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all models
Base = declarative_base()


def get_db():
    """
    FastAPI dependency that provides
    a database session for each request.
    """
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
        
        