# Сессия для хранения текущего пользователя
class Session:
    def __init__(self):
        self.current_user = None
        self.current_project = 1

    def set_current_user(self, username):
        self.current_user = username

    def get_current_user(self):
        return self.current_user

    def set_current_project(self, project_id):
        self.current_project = project_id

    def get_current_project(self):
        return self.current_project
