"""initial migration

Revision ID: dd6eaec92f27
Revises: 
Create Date: 2024-05-23 15:21:04.002420

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd6eaec92f27'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            external_id BIGINT UNIQUE,
            title VARCHAR(255),
            title_original VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
            release_date DATE,
            rating DECIMAL(5, 3),
            popularity DECIMAL(9, 3),
            original_language VARCHAR(255),
            description TEXT,
            INDEX idx_external_id (external_id),
            INDEX idx_title (title)
        ) CHARACTER SET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    
        CREATE TABLE IF NOT EXISTS genres (
            id INT UNIQUE,
            name VARCHAR(255) UNIQUE
        );
        
        CREATE TABLE IF NOT EXISTS movie_genres (
            movie_id BIGINT,
            genre_id INT,
            FOREIGN KEY (movie_id) REFERENCES movies(external_id),
            FOREIGN KEY (genre_id) REFERENCES genres(id),
            PRIMARY KEY (movie_id, genre_id)
        );
    """)


def downgrade() -> None:
    op.execute("""
        DROP TABLE IF EXISTS movie_genres;
        DROP TABLE IF EXISTS movies;
        DROP TABLE IF EXISTS genres;
    """)
