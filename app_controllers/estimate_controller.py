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