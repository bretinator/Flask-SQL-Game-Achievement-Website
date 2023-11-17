import re

from game_achievement_website.classes.achievement import Achievement
from game_achievement_website.classes.console import Console
from game_achievement_website.classes.game import Game
from game_achievement_website.classes.user import User
from game_achievement_website.controllers import gameController, consoleController, userController, achievementController
from game_achievement_website.controllers.achievementController import append_achievements, achieve_displays, \
    init_achievement_display_data, achieve_top_ten, get_top_ten_time, time_pattern
from game_achievement_website.controllers.consoleController import append_consoles, consoles
from game_achievement_website.controllers.gameController import append_games, games
from game_achievement_website.controllers.userController import append_users, set_logged_in_user, get_user
from sql.connect_to_database import sql_connect
from sql.sql_queries import *
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

host = '127.0.0.1'
user = 'root'
password = 'password'
database = 'game_acheivements'
cursor = sql_connect(host, user, password, database).cursor()


def main():
    # Create tables if they don't exist
    create_system_table(cursor)
    create_game_table(cursor)
    create_achievement_table(cursor)
    create_user_table(cursor)

    # Initialize data from sql db
    gameController.init_game_data(cursor)
    consoleController.init_console_data(cursor)
    achievementController.init_achievement_data(cursor)
    achievementController.init_totals_data(cursor)
    userController.init_user_data(cursor)

    app.run()


def validate_time_format(value):
    match = re.match(time_pattern, value)
    if match:
        group1 = match.group(1)
        group2 = match.group(2)
        if int(group1) >= 0 and (float(group2) % 30 == 0):
            return True
    return False


def validate_empty_input(value):
    if not value:
        return True
    return False


def process_game_input():
    err_msg = 'All fields are required'
    game_name = request.form['gameName']
    game_type = request.form['gameType']
    game_developer = request.form['gameDeveloper']
    game_release_date = request.form['gameReleaseDate']
    game_price = request.form['gamePrice']
    game_console = request.form['gameConsole']
    game_exclusive = request.form['gameExclusive']

    if validate_empty_input(game_name):
        return err_msg
    elif validate_empty_input(game_type):
        return err_msg
    elif validate_empty_input(game_developer):
        return err_msg
    elif validate_empty_input(game_release_date):
        return err_msg
    elif validate_empty_input(game_price):
        return err_msg
    elif validate_empty_input(game_console):
        return err_msg

    insert_game(cursor, game_name, game_type, game_developer, game_release_date, game_price, game_console,
                game_exclusive)
    game_ids = get_column_data(cursor, 'game_id', 'game')
    append_games(Game(game_ids[len(game_ids) - 1], game_name, game_type, game_developer, game_release_date,
                      float(game_price), game_console, game_exclusive))
    return ''


def process_console_input():
    err_msg = 'All fields are required'
    console_name = request.form['consoleName']
    if validate_empty_input(console_name):
        return err_msg
    insert_console(cursor, console_name)
    console_ids = get_column_data(cursor, 'console_id', '`system`')
    append_consoles(Console(console_ids[len(console_ids) - 1], console_name))
    return ''


def process_achievement_input():
    err_msg = 'All fields are required'
    game_id = request.form['gameID']
    achievement_name = request.form['achievementName']
    achievement_difficulty = request.form['difficulty']
    achievement_time = request.form['achievementTime']
    achievement_percentage = request.form['achievementPercentage']
    achievement_description = request.form['achievementDescription']

    if validate_empty_input(game_id):
        return err_msg
    elif validate_empty_input(achievement_name):
        return err_msg
    elif validate_empty_input(achievement_time):
        return err_msg
    elif not validate_time_format(achievement_time):
        err_msg = "Time must be in the following format: 00:00 | 30 minute increments"
        return err_msg
    elif validate_empty_input(achievement_percentage):
        return err_msg
    elif validate_empty_input(achievement_description):
        return err_msg

    insert_achievement(cursor, game_id, achievement_name, achievement_difficulty, achievement_time,
                       achievement_percentage, achievement_description)
    achievement_ids = get_column_data(cursor, 'achievement_id', 'achievement')
    append_achievements(Achievement(achievement_ids[len(achievement_ids) - 1], game_id, achievement_name,
                                    achievement_difficulty, achievement_time, float(achievement_percentage),
                                    achievement_description))
    return ''


def process_sign_up_input():
    err_msg = 'All fields are required'
    name = request.form['name']
    username = request.form['username']
    _password = request.form['password']
    console_id = request.form['gameConsole']

    if validate_empty_input(name):
        return err_msg
    elif validate_empty_input(username):
        return err_msg
    elif check_if_value_exists(cursor, 'user', 'username', username):
        return 'Username already taken'
    elif validate_empty_input(_password):
        return err_msg

    insert_user(cursor, name, username, _password, console_id)
    user_ids = get_column_data(cursor, 'account_id', 'user')
    append_users(User(user_ids[len(user_ids) - 1], name, username, _password, console_id))


def process_achievement_display():
    err_msg = 'All fields are required'
    game_id = request.form['game']
    platform = request.form['console']
    difficulty = request.form['difficulty']

    if validate_empty_input(game_id):
        return err_msg
    elif validate_empty_input(platform):
        return err_msg
    elif validate_empty_input(difficulty):
        return err_msg

    init_achievement_display_data(cursor, game_id, platform, difficulty)


@app.route('/', methods=['GET', 'POST'])
def login():
    message_er = "No Error"
    if request.method == 'POST':
        if 'signUpBtn' in request.form:
            return redirect(url_for('sign_up'))
        elif 'logInBtn' in request.form:
            if check_if_values_exists(cursor, 'user', 'username', 'password', request.form['username'],
                                      request.form['password']):
                set_logged_in_user(get_user(request.form['username'], request.form['password']))
                return redirect(url_for('nav_page'))
            else:
                message_er = "Username or password not found"

    return render_template("Log_In.html", message_er=message_er)


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    message_er = "No Error"
    if request.method == 'POST':
        if 'goBackBtn' in request.form:
            return redirect(url_for('login'))
        elif 'signUpBtn' in request.form:
            message_er = process_sign_up_input()
    return render_template("Sign_Up.html", consoles=consoles, message_er=message_er)


@app.route('/nav_page', methods=['GET', 'POST'])
def nav_page():
    message_er = "No Error"
    if request.method == 'POST':
        if 'addItems' in request.form:
            return redirect(url_for('add_game'))
        elif 'displayAchievements' in request.form:
            return redirect(url_for('display_achieve'))
        elif 'displayGames' in request.form:
            return redirect(url_for('display_games'))
    return render_template("Nav_Page.html", message_er=message_er)


@app.route('/display_achieve', methods=['GET', 'POST'])
def display_achieve():
    message_er = "No Error"
    if request.method == 'POST':
        if 'goBackBtn' in request.form:
            return redirect(url_for('nav_page'))
        elif 'searchButton' in request.form:
            message_er = process_achievement_display()
    return render_template("Display_All_Achieve.html", message_er=message_er, consoles=consoles, games=games,
                           displays=achieve_displays, top_tens=achieve_top_ten, total_time_top_ten=get_top_ten_time())


@app.route('/display_games', methods=['GET', 'POST'])
def display_games():
    message_er = "No Error"
    if 'goBackBtn' in request.form:
        return redirect(url_for('nav_page'))
    return render_template("Display_Games.html", games=games, consoles=consoles, message_er=message_er)


@app.route('/add_game', methods=['GET', 'POST'])
def add_game():
    game_error = ''
    console_error = ''
    achievement_error = ''

    if request.method == 'POST':
        if 'addGameButton' in request.form:
            game_error = process_game_input()
        elif 'addConsoleButton' in request.form:
            console_error = process_console_input()
        elif 'addAchievementButton' in request.form:
            achievement_error = process_achievement_input()
        elif 'goBackBtn' in request.form:
            return redirect(url_for('nav_page'))
    return render_template("Add_Game.html", games=games, consoles=consoles, game_error=game_error,
                           achievement_error=achievement_error, console_error=console_error)


if __name__ == "__main__":
    main()
