import sqlite3

from models.user_model import UserModel
from app_controllers.session import Session


class ProjectModel:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path

    def get_all_projects(self, username):
        """
        Получает все проекты из базы данных.
        :return: Список проектов в формате [{"id": 1, "name": "Проект 1"}, ...]
        """

        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT id, name FROM Projects WHERE id_estimator = ? OR id_project_manager = ?", (username, username) )  # Таблица с проектами
        rows = cursor.fetchall()
        connection.close()

        return [{"id": row[0], "name": row[1]} for row in rows]