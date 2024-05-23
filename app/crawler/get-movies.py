import sys

import requests

from config import Config
from crawler.database_manager import DatabaseManager

args = sys.argv[1:]
drop_table = "--drop-table" in args
if drop_table:
    print("Drop table")
year_start = None
year_end = None

if drop_table:
    print("Drop table")

if len(args) >= 2:
    try:
        year_start = int(args[-2])
        year_end = int(args[-1])
    except ValueError:
        print("Wrong arguments")
        sys.exit(1)

def fetch_movies(api_key, year, page):
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&primary_release_year={year}&page={page}&language=ru-RU"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        total_pages = data['total_pages']
        movies = data['results']
        return movies, total_pages
    else:
        print(f'Error fetching movies for year {year}')
        return None, 0

db_manager = DatabaseManager()

db_manager.create_tables(drop_table)

def fetch_and_insert_genres(db_manager, api_key):
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=ru-RU"
    response = requests.get(url)
    if response.status_code == 200:
        genres = response.json().get('genres', [])
        for genre in genres:
            if db_manager.genre_exists(genre['id']):
                print(f"Genre {genre['id']} is exists, skipping.")
                continue
            db_manager.add_genre(genre['id'], genre['name'])
        print("Genres inserted into the database.")
    else:
        print("Error fetching genres.")

fetch_and_insert_genres(db_manager, Config.get_api_key())

year = year_start
while year <= year_end:
    page = 1
    movies, total_pages = fetch_movies(Config.get_api_key(), year, page)

    while page <= total_pages:
        print(f"Processing page {page} of {total_pages} for year {year}")

        movies, _ = fetch_movies(Config.get_api_key(), year, page)
        for movie in movies:
            movie_id = movie.get('id')
            print(f"Movie with external_id {movie_id} (Page {page}/{total_pages} for year {year}) is processing...")

            if db_manager.movie_exists(movie_id) == False:
                db_manager.add_movie(movie)
            else:
                print(f"Movie with id:{movie_id} is existed")
                break
            
            genre_ids = movie.get('genre_ids', [])
            for genre_id in genre_ids:
                db_manager.add_movie_genre_relation(movie['id'], genre_id)

        page += 1
    year += 1
