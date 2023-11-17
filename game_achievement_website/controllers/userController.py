from MySQLdb.cursors import Cursor

from game_achievement_website.classes.user import User
from game_achievement_website.sql.sql_queries import get_table_data

users = []
table_name = 'user'
user_logged_in = None


def init_user_data(cursor: Cursor):
    user_data = get_table_data(cursor, table_name)
    users.clear()
    for _user in user_data:
        users.append(User(_user[0], _user[1], _user[2], _user[3], _user[4]))


def append_users(user: User):
    users.append(user)


def set_logged_in_user(user: User):
    global user_logged_in
    if user is not None:
        user_logged_in = user


def get_logged_in_user():
    return user_logged_in


def get_user(username: str, password: str):
    for user in users:
        if user.username == username and user.password == password:
            return user
