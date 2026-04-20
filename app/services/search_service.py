from typing import Any

from app.repositories.post_repository import PostRepository
from app.models.post import Post
from app.utils.db import get_db


class SearchService:

    @staticmethod
    def search_by_title(query: str, user_id: int) -> list[Any] | list[type[Post]]:
        """
        Search posts by title for a specific user.
        """
        if not query or not query.strip():
            return []

        with get_db() as db:
            repo = PostRepository(db)
            posts = repo.search_by_title(query.strip(), user_id)
            for post in posts:
                db.expunge(post)
            return posts

    @staticmethod
    def search_by_id(user_id: int) -> list[Any] | list[type[Post]]:
        """
        Search posts by title for a specific user.
        """
        with get_db() as db:
            repo = PostRepository(db)
            posts = repo.search_by_id(user_id)
            for post in posts:
                db.expunge(post)
            return posts

    @staticmethod
    def get_by_id(post_id: int, user_id: int) -> Post:
        """
        Fetch a single post by ID, scoped to the user.
        user_id is always checked so user can only load their own posts.
        """
        with get_db() as db:
            repo = PostRepository(db)
            post = repo.get_by_id(post_id, user_id)
            db.expunge(post)
            return post

    @staticmethod
    def all_for_user(user_id: int) -> list[type[Post]]:
        """
        Return all posts for a user, used to refresh the list after saving.
        """
        with get_db() as db:
            repo = PostRepository(db)
            return repo.get_all_for_user(user_id)

    @staticmethod
    def save_audio(post_id: int, user_id: int, audio_data: bytes) -> bool:
        with get_db() as db:
            repo = PostRepository(db)
            return repo.update_audio(post_id, user_id, audio_data)

    @staticmethod
    def get_audio(post_id: int, user_id: int) -> bytes | None:
        with get_db() as db:
            repo = PostRepository(db)
            post = repo.get_by_id(post_id, user_id)
            if post is None:
                return None
            audio = post.audio_data
            db.expunge(post)
            return audio

    @staticmethod
    def save(title: str, content: str, user_id: int) -> int:
        """
        Validates and saves a new post.
        """
        if not title.strip():
            raise ValueError("Title cannot be empty.")

        with get_db() as db:
            repo = PostRepository(db)
            post = Post(
                title=title.strip(),
                content=content,
                user_id=user_id
            )
            saved = repo.save(post)
            return saved.id