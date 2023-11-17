def is_valid_exclusive(exclusive: chr):
    if exclusive.lower() != 'y' and exclusive.lower() != 'n':
        return False
    return True


def is_valid_price(price: float):
    if price < 0:
        return False
    return True


class Game:
    def __init__(self, game_id: str, name: str, game_type: str, developer: str, release_date: str, price: float,
                 console_id: str, exclusive: chr):

        self.exclusive = exclusive
        self.console_id = console_id
        self.price = price
        self.release_date = release_date
        self.developer = developer
        self.game_type = game_type
        self.name = name
        self.game_id = game_id
        self.exclusive = exclusive
