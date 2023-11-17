import math
import re

from MySQLdb.cursors import Cursor

from game_achievement_website.classes.achievement import Achievement
from game_achievement_website.controllers.gameController import games
from game_achievement_website.controllers.userController import get_logged_in_user
from game_achievement_website.sql.sql_queries import get_table_data, get_achievement_display_data, get_top_ten_achievements

achievements = []
achieve_displays = []
achieve_top_ten = []

table_name = 'achievement'
time_pattern = r'^(\d{2}):(\d{2})$'


def init_achievement_data(cursor: Cursor):
    achievement_data = get_table_data(cursor, table_name)
    achievements.clear()
    for _achievement in achievement_data:
        achievements.append(
            Achievement(_achievement[0], _achievement[1], _achievement[2], _achievement[3], _achievement[4],
                        _achievement[5], _achievement[6]))


def init_achievement_display_data(cursor: Cursor, game_id, platform, difficulty):
    achieve_displays.clear()
    for data in get_achievement_display_data(cursor, game_id, platform, difficulty):
        for display in data:
            achieve_displays.append(display)


def init_totals_data(cursor: Cursor):
    achieve_top_ten.clear()
    for achievement in get_top_ten_achievements(cursor):
        achieve_top_ten.append(Achievement(achievement[0], achievement[1], achievement[2], achievement[3],
                                           achievement[4], achievement[5], achievement[6]))


def append_achievements(achievement: Achievement):
    achievements.append(achievement)


def get_top_ten_time():
    total_minutes = 0
    total_hours = 0
    for achievement in achieve_top_ten:
        match = re.match(time_pattern, achievement.time_required)
        achievement_hours = int(match.group(1))
        achievement_minutes = int(match.group(2))
        total_hours += achievement_hours
        total_minutes += achievement_minutes
    if total_minutes >= 60:
        remainder = total_minutes % 60
        if remainder != 0:
            total_hours += math.trunc(total_minutes / 60)
            total_minutes -= (total_minutes - remainder)
        else:
            total_minutes = 0
            total_hours += remainder
    rounded_hours = round(total_hours)
    rounded_minutes = round(total_minutes)
    if rounded_hours <= 9:
        total_time = f"0{rounded_hours}:"
    else:
        total_time = f"{rounded_hours}:"
    if rounded_minutes <= 9:
        total_time += f"0{rounded_minutes}"
    else:
        total_time += f"{rounded_minutes}"
    return total_time


def get_achievements_for_user_console():
    console_achievements = []
    for achievement in achievements:
        for game in games:
            if get_logged_in_user() is not None:
                if (achievement.game_id == game.game_id) and (game.console_id == get_logged_in_user().console_id):
                    console_achievements.append(achievement)
    return console_achievements


def get_easy_achievements():
    easy_achievements = []
    for achievement in achievements:
        if achievement.difficulty == 'easy':
            easy_achievements.append(achievement)
    return easy_achievements


def get_medium_achievements():
    medium_achievements = []
    for achievement in achievements:
        if achievement.difficulty == 'medium':
            medium_achievements.append(achievement)
    return medium_achievements


def get_hard_achievements():
    hard_achievements = []
    for achievement in achievements:
        if achievement.difficulty == 'hard':
            hard_achievements.append(achievement)
    return hard_achievements


def get_very_hard_achievements():
    very_hard_achievements = []
    for achievement in achievements:
        if achievement.difficulty == 'very hard':
            very_hard_achievements.append(achievement)
    return very_hard_achievements
