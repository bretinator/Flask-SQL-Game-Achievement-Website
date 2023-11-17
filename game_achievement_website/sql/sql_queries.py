from MySQLdb.cursors import Cursor


def get_column_data(cursor: Cursor, column: str, table: str):
    query = f"SELECT {column} from {table}"
    try:
        cursor.execute(query)
    except Exception as e:
        print(f"ErrorL {e}")
    return cursor.fetchall()


def get_table_data(cursor: Cursor, table: str):
    query = f"SELECT * FROM {table}"
    try:
        cursor.execute(query)
    except Exception as e:
        print(f"ErrorL {e}")
    return cursor.fetchall()


def get_achievement_display_data(cursor: Cursor, game_id, platform, difficulty):
    query = (f"SELECT game.name, system.console, achievement.difficulty, achievement.time_required, achievement.name, "
             f"achievement.description FROM achievement JOIN game ON achievement.game_id = game.game_id "
             f"JOIN `system` ON game.console_id = system.console_id WHERE achievement.game_id = %s AND game.console_id "
             f"= %s AND achievement.difficulty = %s")

    try:
        cursor.execute(query, (game_id, platform, difficulty))
    except Exception as e:
        print(f"ErrorL {e}")
    return cursor.fetchall()


def get_top_ten_achievements(cursor: Cursor):
    query = f"SELECT * from achievement ORDER BY percentage ASC"
    try:
        cursor.execute(query)
    except Exception as e:
        print(f"ErrorL {e}")
    return cursor.fetchall()


def get_top_ten_longest_achievements(cursor: Cursor):
    query = f"SELECT * from achievement ORDER BY time_required DESC"
    try:
        cursor.execute(query)
    except Exception as e:
        print(f"ErrorL {e}")
    return cursor.fetchall()


def check_if_value_exists(cursor: Cursor, table, column, value):
    query = f"SELECT * FROM {table} WHERE {column} = %s"
    try:
        cursor.execute(query, (value,))

        if cursor.rowcount > 0:
            return True
        return False
    except Exception as e:
        print(f"Error: {e}")


def check_if_values_exists(cursor: Cursor, table, column1, column2, value1, value2):
    query = f"SELECT * FROM {table} WHERE {column1} = %s AND {column2} = %s"
    try:
        cursor.execute(query, (value1, value2))

        if cursor.rowcount > 0:
            return True
        return False
    except Exception as e:
        print(f"Error: {e}")


def insert_achievement(cursor: Cursor, game_id, name, difficulty, time_required, percentage, description):
    query = ("INSERT INTO achievement (game_id, name, difficulty, time_required, percentage, description) VALUES (%s, "
             "%s, %s, %s, %s, %s)")
    data_to_insert = (game_id, name, difficulty, time_required, percentage, description)
    cursor.execute(query, data_to_insert)
    cursor.connection.commit()


def insert_game(cursor: Cursor, name, game_type, developer, release_date, price, console_id, exclusive):
    query = ("INSERT INTO game (name, game_type, developer, release_date, price, console_id, exclusive) VALUES (%s, "
             "%s, %s, %s, %s, %s, %s)")
    data_to_insert = (name, game_type, developer, release_date, price, console_id, exclusive)
    cursor.execute(query, data_to_insert)
    cursor.connection.commit()


def insert_user(cursor: Cursor, name, username, password, console_id):
    query = "INSERT INTO user (name, username, password, console_id) VALUES (%s, %s, %s, %s)"
    data_to_insert = (name, username, password, console_id)
    cursor.execute(query, data_to_insert)
    cursor.connection.commit()


def insert_console(cursor: Cursor, console_name):
    query = "INSERT INTO `system` (console) VALUES (%s)"
    data_to_insert = (console_name,)
    cursor.execute(query, data_to_insert)
    cursor.connection.commit()


def create_system_table(cursor: Cursor):
    query = (f"CREATE TABLE IF NOT EXISTS `System` ("
             f"console_id INT PRIMARY KEY AUTO_INCREMENT, "
             f"console VARCHAR(11) "
             f")")
    cursor.execute(query)


def create_game_table(cursor: Cursor):
    query = (f"CREATE TABLE IF NOT EXISTS Game ("
             f"game_id INT PRIMARY KEY AUTO_INCREMENT, "
             f"name VARCHAR(50), "
             f"game_type VARCHAR(50), "
             f"developer VARCHAR(50), "
             f"release_date DATE, "
             f"price DECIMAL(4, 2), "
             f"console_id INT, "
             f"FOREIGN KEY (console_id) REFERENCES `System`(console_id), "
             f"exclusive CHAR(1)"
             f")")
    cursor.execute(query)


def create_achievement_table(cursor: Cursor):
    query = (f"CREATE TABLE IF NOT EXISTS Achievement ("
             f"achievement_id INT PRIMARY KEY AUTO_INCREMENT, "
             f"game_id INT, "
             f"FOREIGN KEY (game_id) REFERENCES Game(game_id), "
             f"name VARCHAR(50), "
             f"difficulty VARCHAR(14), "
             f"time_required VARCHAR(5), "
             f"percentage DECIMAL(3, 2), "
             f"description VARCHAR(100)"
             f")")
    cursor.execute(query)


def create_user_table(cursor: Cursor):
    query = (f"CREATE TABLE IF NOT EXISTS User ("
             f"account_id INT PRIMARY KEY AUTO_INCREMENT, "
             f"name VARCHAR(50), "
             f"username VARCHAR(50), "
             f"password VARCHAR(50), "
             f"console_id INT, "
             f"FOREIGN KEY (console_id) REFERENCES `system`(console_id)"
             f")")
    cursor.execute(query)
