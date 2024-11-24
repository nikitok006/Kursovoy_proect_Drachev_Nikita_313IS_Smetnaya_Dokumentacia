import sqlite3
from  collections import defaultdict
from datetime import datetime
from  app_controllers.session import Session

class EstimateModel:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path

    def get_project_id(self, project_id):
        # """
        # Получает project_id для текущего пользователя.
        # """
        # conn = sqlite3.connect(self.db_path)
        # cursor = conn.cursor()
        # cursor.execute("""
        #     SELECT projects.id
        #     FROM projects
        #     JOIN Users ON projects.id_estimator = Users.login
        #     WHERE users.login = ?
        #     LIMIT 1
        # """, (project_id,))
        # print(project_id, 1431431234)
        # result = cursor.fetchone()
        # print(result, 1431431234)

        return project_id

    def get_materials(self):
        """
        Возвращает список всех доступных материалов.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, unit, cost_per_unit FROM resources")  # Таблица материалов
        materials = cursor.fetchall()
        print(materials)
        conn.close()
        return [{"id": row[0], "name": row[1], "unit": row[2], "cost_per_unit": row[3]} for row in materials]

    def save_estimate(self, estimate_number, materials_with_quantity, session):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            username = session.get_current_project()
            project_id = self.get_project_id(username)

            # Текущая дата
            current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Сохраняем смету без total_cost
            print(f"Сохраняем смету: estimate_number={estimate_number}, project_id={project_id}")
            cursor.execute("""
                INSERT INTO estimates (estimate_number, project_id, created_at)
                VALUES (?, ?, ?)
            """, (estimate_number, project_id, current_date))
            estimate_id = cursor.lastrowid

            # Рассчитываем общую стоимость (total_cost)
            total_cost = 0
            for material in materials_with_quantity:
                # Получаем стоимость материала
                cursor.execute("""
                    SELECT cost_per_unit
                    FROM resources
                    WHERE id = ?
                """, (material["id"],))
                material_cost_result = cursor.fetchone()
                if not material_cost_result:
                    raise ValueError(f"Материал с id={material['id']} не найден в таблице materials")
                cost_per_unit = material_cost_result[0]

                # Увеличиваем общую стоимость
                total_cost += material["quantity"] * cost_per_unit
                total_cost_per_material = material["quantity"] * cost_per_unit
                # Сохраняем материал в таблицу estimate_materials
                print(
                    f"Сохраняем материал: estimate_id={estimate_id}, material_id={material['id']}, quantity={material['quantity']}")
                cursor.execute("""
                    INSERT INTO estimate_resources (estimate_id, resource_id, quantity, total_cost)
                    VALUES (?, ?, ?, ?)
                """, (estimate_id, material["id"], material["quantity"],total_cost_per_material))

            # Обновляем total_cost в таблице estimates
            cursor.execute("""
                UPDATE estimates
                SET total_cost = ?
                WHERE id = ?
            """, (total_cost, estimate_id))

            # Сохраняем изменения в базе
            conn.commit()
            conn.close()
            print(f"Смета успешно сохранена с общей стоимостью: {total_cost}")
        except sqlite3.IntegrityError as e:
            print(f"Ошибка сохранения сметы: {e}")
        except ValueError as ve:
            print(f"Ошибка: {ve}")


    def get_all_estimates(self, session):
        """
        Возвращает список всех смет и связанных с ними материалов.
        """
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            username = session.get_current_project()
            project_id = self.get_project_id(username)
            print(project_id)
            # Выполняем объединённый запрос
            cursor.execute("""
                      SELECT 
                          estimates.id, 
                          estimates.estimate_number, 
                          estimates.created_at, 
                          estimates.total_cost, 
                          estimates.comment
                      FROM estimates
                      WHERE estimates.project_id = ?
                  """, (project_id,))
            rows = cursor.fetchall()

            # Группируем результаты
            results = defaultdict(lambda: {
                "materials": [],
                "estimate_number": "",
                "created_at": "",
                "total_cost": "",
                "comment": ""
            })

            for estimate_id, estimate_number, created_at, total_cost, comment in rows:
                # Преобразуем created_at в читаемый формат
                if created_at:
                    try:
                        created_at = datetime.fromtimestamp(float(created_at)).strftime('%Y-%m-%d %H:%M:%S')
                    except (ValueError, TypeError):
                        created_at = "Не указана"

                results[estimate_id].update({
                    "estimate_number": estimate_number,
                    "created_at": created_at,
                    "total_cost": total_cost if total_cost is not None else "Отсутствует",
                    "comment": comment if comment is not None else ""
                })

            # Преобразуем результаты в список
            final_results = list(results.values())

            # Отладочный вывод
            print(f"Итоговые результаты: {final_results}")
            return final_results
        finally:
            conn.close()
