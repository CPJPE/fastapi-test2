"""add content column to posts table

Revision ID: 00f723fe7af3
Revises: be8f5a5d055d
Create Date: 2024-04-02 14:56:19.149859

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00f723fe7af3'
down_revision: Union[str, None] = 'be8f5a5d055d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
