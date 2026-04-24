"""merge multiple heads

Revision ID: 6b254c46668b
Revises: c07b97b8a765, c3d4e5f6a7b8
Create Date: 2026-04-20 22:32:18.944655

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b254c46668b'
down_revision: Union[str, Sequence[str], None] = ('c07b97b8a765', 'c3d4e5f6a7b8')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
