# Сессия для хранения текущего пользователя
class Session:
    def __init__(self):
        self.current_user = None

    def set_current_user(self, username):
        self.current_user = username

    def get_current_user(self):
        return self.current_user
