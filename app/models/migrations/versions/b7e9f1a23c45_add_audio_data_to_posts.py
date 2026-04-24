"""add audio_data to posts

Revision ID: b7e9f1a23c45
Revises: 451d41838c6a
Create Date: 2026-04-20 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'b7e9f1a23c45'
down_revision: Union[str, Sequence[str], None] = '451d41838c6a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('audio_data', sa.LargeBinary(), nullable=True))


def downgrade() -> None:
    op.drop_column('posts', 'audio_data')
