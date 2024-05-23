"""Create watched_movies table

Revision ID: 924315f9cde3
Revises: dd6eaec92f27
Create Date: 2024-05-23 15:41:19.444590

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '924315f9cde3'
down_revision: Union[str, None] = 'dd6eaec92f27'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE watched_movies (
            id INT AUTO_INCREMENT PRIMARY KEY,
            movie_id BIGINT,
            date DATE,
            rate INT,
            FOREIGN KEY (movie_id) REFERENCES movies(id)
        );
    """)


def downgrade() -> None:
    op.execute("""
        DROP TABLE IF EXISTS watched_movies;
    """)
