import unittest

from game_achievement_website.controllers import userController
from game_achievement_website.controllers.achievementController import init_achievement_data, achievements, \
    get_achievements_for_user_console
from game_achievement_website.controllers.consoleController import consoles, init_console_data
from game_achievement_website.controllers.gameController import init_game_data, games, get_games_for_console
from game_achievement_website.controllers.userController import init_user_data, set_logged_in_user
from game_achievement_website.sql.connect_to_database import sql_connect
from game_achievement_website.sql.sql_queries import get_top_ten_longest_achievements

host = '127.0.0.1'
user = 'root'
password = 'password'
database = 'game_acheivements'
cursor = sql_connect(host, user, password, database).cursor()


class TestQueries(unittest.TestCase):
    def test_get_top_ten_longest_achievements(self):
        init_achievement_data(cursor)
        achievement_data = get_top_ten_longest_achievements(cursor)
        if len(achievements) < 10:
            if len(achievement_data) == len(achievements):
                self.assertEqual(len(achievement_data), len(achievements))
        elif len(achievements) >= 10:
            self.assertEqual(len(achievement_data), 10)

    def test_get_achievements_for_user_console(self):
        init_achievement_data(cursor)
        init_game_data(cursor)
        init_user_data(cursor)
        set_logged_in_user(userController.users[0])
        ctr = 0
        for achievement in achievements:
            for game in games:
                if userController.user_logged_in.console_id == game.console_id:
                    if achievement.game_id == game.game_id:
                        ctr += 1

        self.assertEqual(len(get_achievements_for_user_console()), ctr)

    def test_get_games_for_consoles(self):
        init_game_data(cursor)
        init_console_data(cursor)

        query = f"SELECT * from game WHERE console_id = {consoles[0].console_id}"
        cursor.execute(query)
        data = cursor.fetchall()

        self.assertEqual(len(get_games_for_console(consoles[0].console_id)), len(data))





