class EstimateController:
    def __init__(self, model, session):
        self.model = model
        self.session = session
        self.update_table_callback = None

    def set_update_table_callback(self, callback):
        """
        Устанавливает функцию для обновления таблицы.
        """
        self.update_table_callback = callback

    def get_all_estimates(self, *args):
        """
        Получает список всех смет через модель.
        """
        return self.model.get_all_estimates(self.session)

    def get_materials(self, *args):
        # print("Вызов get_materials в EstimateController")
        return self.model.get_materials()

    def save_estimate(self, estimate_number, materials_with_quantity, session):
        # Логика сохранения в БД
        for material in materials_with_quantity:
            print(f"Материал ID {material['id']}, Количество {material['quantity']}")
        print(f"Смета №{estimate_number} сохранена.")
        return self.model.save_estimate(estimate_number, materials_with_quantity, session)

    def get_materials_for_estimate(self, estimate_number):
        return self.model.get_materials_for_estimate(estimate_number)

    def update_estimate(self, estimate_number, materials):
        self.model.update_estimate(estimate_number, materials)

    def get_materials_for_editing(self, estimate_number):
        """
        Возвращает все материалы с пометкой, связаны ли они с данной сметой.
        """
        materials_in_estimate = self.model.get_materials_for_estimate(estimate_number)
        all_materials = self.model.get_materials()

        # Создаём словарь для проверки, какие материалы уже есть в смете
        materials_in_estimate_dict = {m["name"]: m for m in materials_in_estimate}

        # Объединяем данные
        for material in all_materials:
            if material["name"] in materials_in_estimate_dict:
                material["quantity"] = materials_in_estimate_dict[material["name"]]["quantity"]
                material["in_estimate"] = True
            else:
                material["quantity"] = 0  # Материал ещё не связан со сметой
                material["in_estimate"] = False

        return all_materials

    def get_estimates(self):
        return self.model.get_estimates(self.session.get_current_project())

    def add_comment(self, estimate_number, comment):
        """Добавляет или обновляет комментарий для указанной сметы."""
        self.model.add_comment(estimate_number, comment)