"""Change watched movies table

Revision ID: 2cf0369b5d5e
Revises: 924315f9cde3
Create Date: 2024-05-26 03:17:00.280577

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2cf0369b5d5e'
down_revision: Union[str, None] = '924315f9cde3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE watched_movies
        ADD COLUMN is_rewatch BOOLEAN
        """
    )

def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE watched_movies
        DROP COLUMN is_rewatch
        """
    )
