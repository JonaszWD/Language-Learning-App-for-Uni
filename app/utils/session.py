class Session:
    """
    Holds the currently logged-in user's data.
    One instance is created at app startup and passed to every
    controller that needs to know who is logged in.
    """

    def __init__(self):
        self._user_id: int | None = None
        self._username: str | None = None

    # ── Auth ──────────────────────────────────────────────────────────────────

    def login(self, user_id: int, username: str):
        """Called by AuthController after a successful DB login."""
        self._user_id = user_id
        self._username = username

    def logout(self):
        """Clear all session data."""
        self._user_id = None
        self._username = None

    # ── Accessors ─────────────────────────────────────────────────────────────

    @property
    def user_id(self) -> int | None:
        return self._user_id

    @property
    def username(self) -> str | None:
        return self._username

    @property
    def is_logged_in(self) -> bool:
        return self._user_id is not None