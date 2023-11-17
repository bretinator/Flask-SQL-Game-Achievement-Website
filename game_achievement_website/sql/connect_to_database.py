import MySQLdb


def sql_connect(host: str, user: str, password: str, database: str):
    host = host
    user = user
    password = password
    database = database
    try:
        connection = MySQLdb.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if connection:
            print("Connected to MySQL server")
            return connection

    except MySQLdb.Error as error:
        print(f"Error: {error}")
