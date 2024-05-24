from app.database_manager import DatabaseManager


class CrawlerDatabaseManager(DatabaseManager):
    def __init__(self):
        super().__init__()

    def movie_exists(self, external_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM movies WHERE external_id = %s", (external_id,))
            count = cursor.fetchone()[0]
            return count > 0
        
    def add_movie(self, movie):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO movies (external_id, title, title_original, release_date, rating, popularity, original_language, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    movie.get('id'),
                    movie.get('title'),
                    movie.get('original_title'),
                    movie.get('release_date'),
                    movie.get('vote_average'),
                    movie.get('popularity'),
                    movie.get('original_language'),
                    movie.get('overview')
                )
            )
            conn.commit()

    def add_genre(self, genre_id, genre_name):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO genres (id, name) VALUES (%s, %s)", (genre_id, genre_name,))
            conn.commit()

    def genre_exists(self, id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM genres WHERE id = %s", (id,))
            count = cursor.fetchone()[0]
            return count > 0

    def add_movie_genre_relation(self, movie_id, genre_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM movie_genres WHERE movie_id=%s", (movie_id,))
            cursor.execute("INSERT INTO movie_genres (movie_id, genre_id) VALUES (%s, %s)", (movie_id, genre_id))
            conn.commit()

    def find_movies(self, title) -> list:
        with self.connect() as conn:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT external_id, title, YEAR(release_date) year FROM movies WHERE LOWER(title) LIKE LOWER(%s) ORDER BY release_date;"
            like_value = f"%{title}%"
            cursor.execute(query, (like_value,))
            movies = cursor.fetchall()
            return movies

