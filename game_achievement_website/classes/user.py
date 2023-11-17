class User:
    def __init__(self, account_id: str, name: str, username: str, password: str, console_id: str):
        self.console_id = console_id
        self.password = password
        self.username = username
        self.name = name
        self.account_id = account_id
