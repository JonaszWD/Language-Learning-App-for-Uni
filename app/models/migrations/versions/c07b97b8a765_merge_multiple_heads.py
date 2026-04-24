"""merge multiple heads

Revision ID: c07b97b8a765
Revises: 6594d2b02dc6, b7e9f1a23c45
Create Date: 2026-04-20 12:15:04.970223

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c07b97b8a765'
down_revision: Union[str, Sequence[str], None] = ('6594d2b02dc6', 'b7e9f1a23c45')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
