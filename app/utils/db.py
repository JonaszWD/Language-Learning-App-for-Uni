import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# ── Base ──────────────────────────────────────────────────────────────────────
# All models import Base from here and use it to declare their tables.
# This ensures every model is registered under the same metadata,
# which Alembic needs to detect schema changes.
Base = declarative_base()

# ── Engine ────────────────────────────────────────────────────────────────────
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise EnvironmentError(
        "DATABASE_URL is not set. Add it to your .env file.\n"
        "Example: DATABASE_URL=postgresql://user:password@localhost:5432/mydb"
    )

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # test connections before using them — avoids stale connection errors
    echo=False,           # set to True during development to log all SQL queries
)

# ── Session factory ───────────────────────────────────────────────────────────
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,   # we commit manually so we control when data is saved
    autoflush=False,    # we flush manually to avoid premature writes
)


# ── Context manager ───────────────────────────────────────────────────────────
@contextmanager
def get_db():
    """
    Provide a models session for a single unit of work.

    Usage:
        with get_db() as db:
            results = db.query(Post).all()

    The session is automatically committed on success,
    rolled back on any exception, and always closed afterwards.
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# ── Table creation ────────────────────────────────────────────────────────────
def create_tables():
    """
    Create all tables that don't exist yet.
    Called once at startup in main.py as a safety net.
    Alembic handles migrations — this just ensures the DB is never empty
    on a first run before migrations have been applied.
    """
    Base.metadata.create_all(bind=engine)