from MySQLdb.cursors import Cursor

from game_achievement_website.classes.game import Game
from game_achievement_website.sql.sql_queries import get_table_data

games = []
table_name = 'game'


def init_game_data(cursor: Cursor):
    game_data = get_table_data(cursor, table_name)
    games.clear()
    for _game in game_data:
        games.append(Game(_game[0], _game[1], _game[2], _game[3], _game[4], _game[5], _game[6], _game[7]))


def append_games(game: Game):
    games.append(game)


def get_games_for_console(console_id: str):
    console_games = []
    for game in games:
        if game.console_id == console_id:
            console_games.append(game)
    return console_games


def get_games():
    return games


def get_total_spent_console_games(console_id: str):
    total = 0
    for game in games:
        if game.console_id == console_id:
            total += game.price
    return total


def get_total_spent_developer_games(developer: str):
    total = 0
    for game in games:
        if game.developer == developer:
            total += game.price
    return total


def get_total_spent_all_games():
    total = 0
    for game in games:
        total += game.price
    return total


def get_total_game_types():
    game_types = []
    for game in games:
        if game.game_type not in game_types:
            game_types.append(game.game_type)
    return game_types


def get_total_game_types_custom(game_type: str):
    game_types = []
    for game in games:
        if game.game_type == game_type:
            game_types.append(game.game_type)
    return game_types


def is_exclusive_game(compare_game: Game):
    for game in games:
        if (game.name.lower() == compare_game.name.lower() and
                compare_game.console_id != game.console_id):
            return False
    return True


def get_total_exclusives():
    exclusives = []
    for game in games:
        if is_exclusive_game(game):
            exclusives.append(game)
    return exclusives

