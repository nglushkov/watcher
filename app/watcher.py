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
    result = db_manager.find_movie_by_title(title)
    print_movies(result)

def print_movies(movies):
    table = PrettyTable()
    table.field_names = ["Title", "Release Year"]
    for movie in movies:
        table.add_row(movie)
    print(table)

action_functions = {
    "Add watched movie": add_watched_movie,
    "Last watched movies": last_watched_movies,
    "Find a movie": find_a_movie,
}

questions = [
    inquirer.List(
        "action",
        message="What do you want?",
        choices=list(action_functions.keys()),
    ),
]

answers = inquirer.prompt(questions)
print(answers)

selected_action = answers["action"]

if selected_action in action_functions:
    action_functions[selected_action]()
else:
    print("Неизвестное действие")
