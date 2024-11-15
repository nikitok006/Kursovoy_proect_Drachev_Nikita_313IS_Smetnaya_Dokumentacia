import sqlite3

class UserModel:
    def __init__(self):
        self.connection = sqlite3.connect("database.db")

    def verify_user(self, username, password):
        """Проверка учетных данных в базе."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Users WHERE login=? AND password=?", (username, password))
        result = cursor.fetchone()
        return result is not None

    def add_estimate(self):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO ESTIMATE")
