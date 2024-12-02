import sqlite3


class ReportModel:
    def __init__(self):
        self.db_path = "database.db"

    def get_materials_for_estimate(self, estimate_id):
        """
        Возвращает список материалов для указанной сметы.
        """
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()

            # Запрос материалов для сметы
            cursor.execute("""
                SELECT 
                    m.name AS material_name,
                    er.quantity,
                    m.cost_per_unit,
                    er.quantity * m.cost_per_unit AS total_cost
                FROM Estimate_resources er
                JOIN resources m ON er.resource_id = m.id
                WHERE er.estimate_id = ?
            """, (estimate_id,))
            materials = [
                {
                    "material_name": row[0],
                    "quantity": row[1],
                    "cost_per_unit": row[2],
                    "total_cost": row[3],
                }
                for row in cursor.fetchall()
            ]
            return materials
        finally:
            conn.close()
