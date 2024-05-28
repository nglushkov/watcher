from datetime import datetime, timedelta

from mysql import connector

from app.config import Config


class DatabaseManager:
    connection_params: dict
    
    def __init__(self):
        self.connection_params = Config.get_db_connection_params()

    def connect(self):
        return connector.connect(**self.connection_params)

    def find_movies(self, title) -> list:
        with self.connect() as conn:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT
                    m.id,
                    m.external_id,
                    m.title,
                    YEAR(m.release_date) AS year,
                    m.title_original,
                    m.release_date,
                    m.rating,
                    m.description,
                    GROUP_CONCAT(g.name ORDER BY g.name SEPARATOR ', ') AS genres
                FROM movies m
                LEFT JOIN movie_genres mg ON m.external_id = mg.movie_id
                LEFT JOIN genres g ON mg.genre_id = g.id
                WHERE LOWER(m.title) LIKE LOWER(%s)
                GROUP BY
                    m.id,
                    m.external_id,
                    m.title,
                    m.title_original,
                    m.release_date,
                    m.rating,
                    m.description
                ORDER BY m.release_date DESC;

            """
            like_value = f"%{title}%"
            cursor.execute(query, (like_value,))
            movies = cursor.fetchall()
            return movies

    def add_watched_movie(self, movie_id, rate, is_rewatch, watch_date) -> None:
        with self.connect() as conn:
            cursor = conn.cursor(dictionary=True)
            query = "INSERT INTO watched_movies (movie_id, date, rate, is_rewatch) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (movie_id, watch_date, rate, is_rewatch))
            conn.commit()
            cursor.close()

    def get_all_watched_movies(self):
        with self.connect() as conn:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT wm.movie_id, wm.date, wm.rate, m.title, YEAR(m.release_date) AS year, wm.is_rewatch,
                       GROUP_CONCAT(g.name ORDER BY g.name SEPARATOR ', ') AS genres
                FROM watched_movies wm
                LEFT JOIN movies m ON wm.movie_id = m.id
                LEFT JOIN movie_genres mg ON m.external_id = mg.movie_id
                LEFT JOIN genres g ON mg.genre_id = g.id
                GROUP BY wm.movie_id, wm.date, wm.rate, m.title, YEAR(m.release_date), wm.is_rewatch, wm.id
                ORDER BY wm.date DESC, wm.id DESC;
            """
            cursor.execute(query)
            movies = cursor.fetchall()
            return movies

    def get_last_30_days_watched_movies(self):
        with self.connect() as conn:
            cursor = conn.cursor(dictionary=True)
            thirty_days_ago = datetime.now() - timedelta(days=30)
            query = """
                SELECT wm.movie_id, wm.date, wm.rate, m.title, YEAR(m.release_date) AS year, wm.is_rewatch,
                       GROUP_CONCAT(g.name ORDER BY g.name SEPARATOR ', ') AS genres
                FROM watched_movies wm
                LEFT JOIN movies m ON wm.movie_id = m.id
                LEFT JOIN movie_genres mg ON m.external_id = mg.movie_id
                LEFT JOIN genres g ON mg.genre_id = g.id
                WHERE wm.date >= %s
                GROUP BY wm.movie_id, wm.date, wm.rate, m.title, YEAR(m.release_date), wm.is_rewatch, wm.id
                ORDER BY wm.date DESC, wm.id DESC;
            """
            cursor.execute(query, (thirty_days_ago,))
            movies = cursor.fetchall()
            return movies

    def get_best_rewatched_movies(self):
        with self.connect() as conn:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT wm.movie_id, wm.date, wm.rate, m.title, YEAR(m.release_date) AS year, wm.is_rewatch,
                       GROUP_CONCAT(g.name ORDER BY g.name SEPARATOR ', ') AS genres
                FROM watched_movies wm
                LEFT JOIN movies m ON wm.movie_id = m.id
                LEFT JOIN movie_genres mg ON m.external_id = mg.movie_id
                LEFT JOIN genres g ON mg.genre_id = g.id
                WHERE wm.rate = 5 AND wm.is_rewatch = 1
                GROUP BY wm.movie_id, wm.date, wm.rate, m.title, YEAR(m.release_date), wm.is_rewatch, wm.id
                ORDER BY wm.date DESC, wm.id DESC;
            """
            cursor.execute(query)
            movies = cursor.fetchall()
            return movies