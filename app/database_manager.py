from mysql import connector
from dotenv import dotenv_values
from config import Config

class DatabaseManager:
    connection_params: dict
    
    def __init__(self):
        self.connection_params = Config.get_db_connection_params()

    def connect(self):
        return connector.connect(**self.connection_params)

    def create_tables(self, drop_table):
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                if drop_table:
                    cursor.execute("DROP TABLE IF EXISTS movie_genres;")
                    print("Table movie_genres has been dropped")
                    cursor.execute("DROP TABLE IF EXISTS movies;")
                    print("Table movies has been dropped")
                    cursor.execute("DROP TABLE IF EXISTS genres;")
                    print("Table genres has been dropped")

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS movies (
                        id BIGINT AUTO_INCREMENT PRIMARY KEY,
                        external_id BIGINT UNIQUE,
                        title VARCHAR(255),
                        title_original VARCHAR(255),
                        release_date DATE,
                        rating DECIMAL(5, 3),
                        popularity DECIMAL(9, 3),
                        original_language VARCHAR(255),
                        description TEXT,
                        INDEX idx_external_id (external_id),
                        INDEX idx_title (title)
                    ) DEFAULT CHARSET=utf8;
                """)

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS genres (
                        id INT UNIQUE,
                        name VARCHAR(255) UNIQUE
                    ) DEFAULT CHARSET=utf8;
                """)

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS movie_genres (
                        movie_id BIGINT,
                        genre_id INT,
                        FOREIGN KEY (movie_id) REFERENCES movies(external_id),
                        FOREIGN KEY (genre_id) REFERENCES genres(id),
                        PRIMARY KEY (movie_id, genre_id)
                    );
                """)
            print("Tables movies, genres, and movie_genres have been created")
        except connector.Error as err:
            print(f"Error while creating tables: {err}")

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

    def get_genres(self):
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM genres")
                genres = cursor.fetchall()
                return [genre[0] for genre in genres]
        except connector.Error as err:
            print(f"Error while getting genres: {err}")
            return []

    def find_movie_by_title(self, title):
        with self.connect() as conn:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT title, YEAR(release_date) year FROM movies WHERE LOWER(title) LIKE LOWER(%s);"
            like_value = f"%{title}%"
            cursor.execute(query, (like_value,))
            movies = cursor.fetchall()
            return [(movie["title"], movie["year"]) for movie in movies]

