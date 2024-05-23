from mysql import connector

from config import Config


class DatabaseManager:
    connection_params: dict
    
    def __init__(self):
        self.connection_params = Config.get_db_connection_params()

    def connect(self):
        return connector.connect(**self.connection_params)

    def find_movies(self, title) -> list:
        with self.connect() as conn:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT external_id, title, YEAR(release_date) year FROM movies WHERE LOWER(title) LIKE LOWER(%s) ORDER BY release_date;"
            like_value = f"%{title}%"
            cursor.execute(query, (like_value,))
            movies = cursor.fetchall()
            return movies

