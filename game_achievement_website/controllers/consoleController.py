from MySQLdb.cursors import Cursor

from game_achievement_website.classes.console import Console
from game_achievement_website.sql.sql_queries import get_table_data

consoles = []
table_name = '`system`'


def init_console_data(cursor: Cursor):
    console_data = get_table_data(cursor, table_name)
    consoles.clear()
    for _console in console_data:
        consoles.append(Console(_console[0], _console[1]))


def append_consoles(console: Console):
    consoles.append(console)
