class EstimateController:
    def __init__(self, model):
        self.model = model
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
        return self.model.get_all_estimates()

    def get_materials(self):
        return self.model.get_all_materials()