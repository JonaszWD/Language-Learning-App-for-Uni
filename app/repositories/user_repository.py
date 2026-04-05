from sqlalchemy.orm import Session
from app.models.user import User

class UserRepository:
    """
    All direct database operations for the User model live here.
    Receives a db session from the service so the service
    controls the transaction boundary.
    """
    def __init__(self, db: Session):
        self.db = db

    # ── Verify ──────────────────────────────────────────────────────────────────

    def verify_username(self, name: str) -> bool:
        """
        Checks if a username already exists in the database.
        Returns True if the username does exist, False if it doesn't.
        """
        return self.db.query(User).filter(User.name == name).first() is not None

    def verify_password(self, name: str, password: bytes) -> bool:
        """
        Checks if a password exists in the database.
        """
        return (
                self.db.query(User)
                .filter(User.name == name, User.password == password)
                .first()
                is not None
        )

    # ── Read ──────────────────────────────────────────────────────────────────

    def get_by_name(self, name: str):
        """
        Fetches a user by its name
        """
        return (
            self.db.query(User)
            .filter(User.name == name)
            .first()
        )

    def get_by_id(self, id: int):
        """
        Fetches a user by its id
        """
        return (
            self.db.query(User)
            .filter(User.id == id)
            .first()
        )

    # ── Write ─────────────────────────────────────────────────────────────────

    def save(self, user: User) -> User:
        """
        Saves a new user to the database.
        """
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    # ── Delete ────────────────────────────────────────────────────────────────

    def delete_by_name(self, name: str):
        """
        Deletes a user by its name.
        """
        user = self.get_by_name(name)
        if user:
            self.db.delete(user)
            self.db.commit()