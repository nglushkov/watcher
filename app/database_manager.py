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
            query = "SELECT id, external_id, title, YEAR(release_date) year FROM movies WHERE LOWER(title) LIKE LOWER(%s) ORDER BY release_date DESC"
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

    def get_last_watched_movie(self):
        with self.connect() as conn:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT wm.movie_id, wm.date, wm.rate, m.title, YEAR(m.release_date) year, wm.is_rewatch
                FROM watched_movies wm
                LEFT JOIN movies m ON wm.movie_id = m.id
                ORDER BY wm.date DESC, wm.id DESC
            """
            cursor.execute(query)
            movies = cursor.fetchall()
            return movies
