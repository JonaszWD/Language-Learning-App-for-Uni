import os
import sys
from pathlib import Path

# Make `import app...` work when pytest is run from the repo root, and give the
# DB layer an in-memory SQLite URL so importing it never needs a real database.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
