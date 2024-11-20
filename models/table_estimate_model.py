import sqlite3


class ProjectModel:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path

    def get_all_projects(self):
        """
        Получает все проекты из базы данных.
        :return: Список проектов в формате [{"id": 1, "name": "Проект 1"}, ...]
        """
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT id, name FROM Projects")  # Таблица с проектами
        rows = cursor.fetchall()
        connection.close()

        return [{"id": row[0], "name": row[1]} for row in rows]