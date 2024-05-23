import inquirer
from database_manager import DatabaseManager

class WatcherApp:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.is_running = True

    def add_watched_movie(self):
        pass

    def last_watched_movies(self):
        pass

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
                "choosed_movie",
                message="Choose movie",
                choices=[(f"{movie['title']} ({movie['year']})", movie["external_id"]) for movie in movies]
            )
        ]
        answers = inquirer.prompt(movies_questions)
        print(answers)
    
    def exit_program(self):
        self.is_running = False
        print("Exiting the program...")

    def main_menu(self):
        action_functions = {
            "Add watched movie": self.add_watched_movie,
            "Last watched movies": self.last_watched_movies,
            "Find a movie": self.find_a_movie,
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
