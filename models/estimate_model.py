import sqlite3


class EstimateModel:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path

    def get_all_materials(self):
        """
        Возвращает список всех доступных материалов.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM materials")  # Таблица материалов
        materials = cursor.fetchall()
        conn.close()
        return [{"id": row[0], "name": row[1]} for row in materials]

    def save_estimate(self, estimate_number, selected_materials):
        """
        Сохраняет новую смету в базу данных и связывает её с выбранными материалами.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Добавляем новую смету в таблицу estimates
        cursor.execute("INSERT INTO estimates (estimate_number) VALUES (?)", (estimate_number,))
        estimate_id = cursor.lastrowid  # ID добавленной сметы

        # Добавляем связь материалов с этой сметой в таблицу Estimate_resources
        for material_id in selected_materials:
            cursor.execute(
                "INSERT INTO Estimate_resources (estimate_id, material_id) VALUES (?, ?)",
                (estimate_id, material_id),
            )

        conn.commit()
        conn.close()

    def get_all_estimates(self):
        """
        Возвращает список всех смет и связанных с ними материалов.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Получаем все сметы
        cursor.execute("SELECT id, estimate_number FROM estimates")
        estimates = cursor.fetchall()

        # Получаем материалы, связанные с каждой сметой
        results = []
        for estimate_id, estimate_number in estimates:
            cursor.execute("""
                SELECT materials.name
                FROM Estimate_resources
                JOIN materials ON Estimate_resources.material_id = materials.id
                WHERE Estimate_resources.estimate_id = ?
            """, (estimate_id,))
            materials = [row[0] for row in cursor.fetchall()]
            results.append({"estimate_number": estimate_number, "materials": materials})

        conn.close()
        return results
