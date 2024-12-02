import sqlite3
import bcrypt


class UserModel:
    def __init__(self):
        self.connection = sqlite3.connect("database.db")

    def hash_password(self, password):
        # Генерация хэша с солью
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)

    def verify_password(self, password, hashed_password):
        # Убедимся, что хэш в байтах
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

    def login_user(self, username, password):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Ищем пользователя в базе данных
        cursor.execute("SELECT password FROM Users WHERE login = ?", (username,))
        user = cursor.fetchone()
        cursor.execute("SELECT role FROM Users WHERE login = ?", (username,))
        if user:
            stored_hash = user[0]  # Хэш пароля из базы
            # Проверяем введённый пароль
            if self.verify_password(password, stored_hash):
                return 1
            else:
                print("Неверный пароль.")
        else:
            print("Пользователь не найден.")

        conn.close()

    def get_username(self, username):
            return username

    def role(self, username):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM Users WHERE login = ?", (username,))
        role = cursor.fetchone()
        if role == ('сметчик',):
            return 1
        else:
            return 0
