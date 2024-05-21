import inquirer
from database_manager import DatabaseManager
from prettytable import PrettyTable

db_manager = DatabaseManager()

def add_watched_movie():
    print("Вы выбрали: Добавить просмотренный фильм")

def last_watched_movies():
    print("Вы выбрали: Последние просмотренные фильмы")

def find_a_movie():
    questions = [inquirer.Text("title", message="Enter the title")]
    title = inquirer.prompt(questions).get("title")
    result = db_manager.find_movies(title)
    print_movies(result)

def print_movies(movies: list) -> None:
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
            find_a_movie()
        return
    
    choices = [(f"{movie['title']} ({movie['year']})", movie["external_id"]) for movie in movies]
    movies_questions = [
        inquirer.List(
            "choosed_movie",
            message="Choose movie",
            choices=choices
        )
    ]
    answers = inquirer.prompt(movies_questions)
    print(answers)
    
def exit_program():
    global is_run
    is_run = False
    print("Exiting the program...")

def main_menu():
    global is_run
    is_run = True

    action_functions = {
        "Add watched movie": add_watched_movie,
        "Last watched movies": last_watched_movies,
        "Find a movie": find_a_movie,
        "Exit": exit_program
    }
    
    while is_run:
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
    main_menu()
