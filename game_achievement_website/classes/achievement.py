import re

time_pattern = r'^(\d{2}):(\d{2})$'


def is_increment_of_30(hours, minutes):
    total_minutes = int(hours) * 60 + int(minutes)
    return total_minutes % 30 == 0


def is_valid_difficulty(difficulty: str):
    if (difficulty.lower() != 'easy' and difficulty.lower() != 'medium' and difficulty.lower() != 'hard' and
            difficulty.lower() != 'very hard'):
        return False
    return True


def is_valid_time(time_required: str):
    match = re.match(time_pattern, time_required)
    if not match:
        return False
    return True


def is_valid_percentage(percentage: float):
    if percentage > 1 or percentage < 0:
        return False
    return True


class Achievement:
    def __init__(self, achievement_id: str, game_id: str, name: str, difficulty: str, time_required: str,
                 percentage: float, description: str):
        if not is_valid_difficulty(difficulty):
            return
        if not is_valid_time(time_required):
            print(time_required)
            return
        if not is_valid_percentage(percentage):
            return

        self.description = description
        self.percentage = percentage
        self.time_required = time_required
        self.difficulty = difficulty
        self.name = name
        self.game_id = game_id
        self.achievement_id = achievement_id
