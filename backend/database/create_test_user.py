from backend.database.connection import SessionLocal
from backend.models.user import User
from backend.core.security import hash_password


def create_test_user():

    db = SessionLocal()

    try:
        existing_user = (
            db.query(User)
            .filter(User.email == "admin@test.com")
            .first()
        )

        if existing_user:
            print("Test user already exists.")
            return

        user = User(
            full_name="Admin User",
            email="admin@test.com",
            password_hash=hash_password("Admin@123"),
            role="admin",
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        print("Test user created successfully!")
        print("Email: admin@test.com")
        print("Password: Admin@123")

    finally:
        db.close()


if __name__ == "__main__":
    create_test_user()