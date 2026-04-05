from sqlalchemy.orm import Session

from app.models.post import Post


class PostRepository:
    """
    All direct database operations for the Post model live here.
    Receives a db session from the service so the service
    controls the transaction boundary.
    """

    def __init__(self, db: Session):
        self.db = db

    # ── Read ──────────────────────────────────────────────────────────────────

    def search_by_title(self, query: str, user_id: int) -> list[type[Post]]:
        """Case-insensitive title search scoped to one user."""
        return (
            self.db.query(Post)
            .filter(Post.user_id == user_id)
            .filter(Post.title.ilike(f"%{query}%"))
            .order_by(Post.created_at.desc())
            .limit(20)
            .all()
        )
    def search_by_id(self, user_id: int) -> list[type[Post]]:
        """Case-insensitive title search scoped to one user."""
        return (
            self.db.query(Post)
            .filter(Post.user_id == user_id)
            .order_by(Post.created_at.desc())
            .limit(20)
            .all()
        )

    def get_all_for_user(self, user_id: int) -> list[type[Post]]:
        """Return every post belonging to a user, newest first."""
        return (
            self.db.query(Post)
            .filter(Post.user_id == user_id)
            .order_by(Post.created_at.desc())
            .all()
        )

    def get_by_id(self, post_id: int, user_id: int) -> Post | None:
        """
        Fetch a single post by id.
        user_id is always included so a user can never fetch
        another user's post by guessing an id.
        """
        return (
            self.db.query(Post)
            .filter(Post.id == post_id)
            .filter(Post.user_id == user_id)
            .first()
        )

    def get_by_title(self, title: str, user_id: int) -> Post | None:
        """Exact title match scoped to one user."""
        return (
            self.db.query(Post)
            .filter(Post.user_id == user_id)
            .filter(Post.title == title)
            .first()
        )

    # ── Write ─────────────────────────────────────────────────────────────────

    def save(self, post: Post) -> Post:
        """
        Insert a new post or update an existing one.
        Works for both — SQLAlchemy detects whether the object
        is new (no id) or existing (has id).
        """
        self.db.add(post)
        self.db.flush()    # writes to DB within the transaction but doesn't commit yet
        self.db.refresh(post)  # reloads the object so generated fields like id are populated
        return post

    # ── Delete ────────────────────────────────────────────────────────────────

    def delete(self, post_id: int, user_id: int) -> bool:
        """
        Delete a post. Returns True if deleted, False if not found.
        user_id check ensures users can only delete their own posts.
        """
        post = self.get_by_id(post_id, user_id)
        if not post:
            return False
        self.db.delete(post)
        self.db.flush()
        return True