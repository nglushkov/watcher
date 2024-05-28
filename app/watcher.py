import inquirer
from database_manager import DatabaseManager
from tabulate import tabulate
from datetime import datetime


def rating_validator(_, x):
    try:
        rating = int(x)
        if 1 <= rating <= 5:
            return True
        else:
            raise ValueError("Rating must be between 1 and 5.")
    except ValueError:
        raise ValueError("Please enter a valid rating between 1 and 5.")


def date_validator(_, x):
    try:
        datetime.strptime(x, "%d.%m.%Y")
        return True
    except ValueError:
        raise ValueError("Date must be in format DD.MM.YYYY.")


class WatcherApp:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.is_running = True

    def add_watched_movie(self):
        pass

    def last_watched_movies(self):
        choices = [
            'Last 30 days',
            'Best rewatched',
            'All'
        ]
        questions = [
            inquirer.List('filter',
                message="Choose filter option",
                choices=choices,
            ),
        ]
        answer = inquirer.prompt(questions)
        filter_option = answer['filter']

        if filter_option == 'Last 30 days':
            watched_movies = self.db_manager.get_last_30_days_watched_movies()
        elif filter_option == 'Best rewatched':
            watched_movies = self.db_manager.get_best_rewatched_movies()
        else:
            watched_movies = self.db_manager.get_all_watched_movies()

        if not watched_movies:
            print("No movies found.")
            return

        headers = ["ID", "Title", "Date", "Genres", "Rating", "Rewatch"]
        rows = [[idx + 1, movie["title"] + " (" + str(movie["year"]) + ")", movie["date"], movie["genres"], movie["rate"],
             "true" if movie["is_rewatch"] else ""] for idx, movie in enumerate(watched_movies)]

        print(tabulate(rows, headers=headers, tablefmt="grid"))

    def find_a_movie(self):
        questions = [inquirer.Text("title", message="Enter the title")]
        title = inquirer.prompt(questions).get("title")
        result = self.db_manager.find_movies(title)
        self.print_movies(result)

    def print_movies(self, movies: list) -> None:
        if not movies:
            confirm_question = [
                inquirer.Confirm(
                    "find_another",
                    message="Movie not found. Find another movies?",
                    default=True,
                )
            ]
            answer = inquirer.prompt(confirm_question)
            if answer["find_another"]:
                self.find_a_movie()
            return
    
        movies_questions = [
            inquirer.List(
                "selected_movie",
                message="Choose movie",
                choices=[(f"{movie['title']} ({movie['year']})", movie) for movie in movies]
            )
        ]
        movie = inquirer.prompt(movies_questions).get("selected_movie")
        movie_name = f"{movie['title']} ({movie['year']})"

        movie_details = [
            ["Title", movie["title"]],
            ["Original Title", movie["title_original"]],
            ["Release Date", movie["release_date"].strftime("%d.%m.%Y") if movie["release_date"] else "N/A"],
            ["Genres", movie["genres"]],
            ["Rating", str(movie["rating"])],
        ]
        print(tabulate(movie_details, tablefmt="grid"))
        print("Description:\n" + movie["description"])

        questions = [
            inquirer.Confirm("add_to_watched", message=f"Add to watched movies \"{movie_name}\"?"),
        ]

        if inquirer.prompt(questions).get("add_to_watched"):
            while True:
                try:
                    rating_question = [
                        inquirer.Text("rating", message="Rate the movie (from 1 to 5)", validate=rating_validator)
                    ]
                    rating_input = inquirer.prompt(rating_question)
                    rating = int(rating_input.get("rating"))
                    break
                except Exception as e:
                    print("Error:", e)
                    print("Please enter a valid rating.")

            rewatch_question = [
                inquirer.Confirm("rewatch", message=f"Will you rewatch \"{movie_name}\"?")
            ]
            rewatch_answer = inquirer.prompt(rewatch_question).get("rewatch")

            date_confirm_question = [
                inquirer.Confirm("set_date", message=f"Do you want to set the watch date for \"{movie_name}\"?")
            ]
            date_confirm_answer = inquirer.prompt(date_confirm_question).get("set_date")

            if date_confirm_answer:
                while True:
                    try:
                        date_question = [
                            inquirer.Text("date", message="Enter the watch date (DD.MM.YYYY)", validate=date_validator)
                        ]
                        date_input = inquirer.prompt(date_question)
                        watch_date = datetime.strptime(date_input.get("date"), "%d.%m.%Y").date()
                        break
                    except Exception as e:
                        print("Error:", e)
                        print("Please enter a valid date in format DD.MM.YYYY.")
            else:
                watch_date = datetime.now().date()

            self.db_manager.add_watched_movie(movie["id"], rating, rewatch_answer, watch_date)
            print(f"Movie {movie_name} has been added to watched movies.")

    def exit_program(self):
        self.is_running = False
        print("Exiting the program...")

    def main_menu(self):
        action_functions = {
            "Find a movie": self.find_a_movie,
            "Add watched movie": self.add_watched_movie,
            "Last watched movies": self.last_watched_movies,
            "Exit": self.exit_program
        }

        while self.is_running:
            questions = [
                inquirer.List(
                    "action",
                    message="Choose an action",
                    choices=list(action_functions.keys())
                )
            ]
            answers = inquirer.prompt(questions)
            action = answers["action"]
            action_functions[action]()

if __name__ == "__main__":
    app = WatcherApp()
    app.main_menu()
