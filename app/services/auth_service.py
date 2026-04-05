from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.utils.db import get_db

class AuthService:

    @staticmethod
    def find_user(username: str) -> bool:
        """
        Returns True if the username is found, False otherwise.
        """
        with get_db() as db:
            repo = UserRepository(db)
            return repo.verify_username(username)

    @staticmethod
    def get_user(username: str) -> User:
        """
        Returns account belonging to the username.
        """
        with get_db() as db:
            repo = UserRepository(db)
            user = repo.get_by_name(username)
            if user:
                db.expunge(user)
            return user

    @staticmethod
    def search(user: str, password: bytes) -> User:
        """
        Search User by username and password, used for login.
        """
        with get_db() as db:
            repo = UserRepository(db)
            return repo.get_by_name_password(user, password)

    @staticmethod
    def register(username: str, password: bytes) -> User:
        """
        Register new user with username and password.
        """
        with get_db() as db:
            repo = UserRepository(db)
            user = User(
                name = username,
                password = password,
            )
        return repo.save(user)