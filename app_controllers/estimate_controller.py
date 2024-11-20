# from models.estimate_model import EstimateModel
# from views.main_view import EstimateCreationWindow
#
# class EstimateController:
#     def __init__(self):
#         self.model = EstimateModel()
#         self.creation = EstimateCreationWindow()
#
#     def save_estimate(self, name, estimate_type, budget, materials):
#         # Сохраняем смету и получаем её ID
#         estimate_id = self.model.save_estimate(name, estimate_type, budget)
#         # Сохраняем связанные материалы
#         self.model.save_materials(estimate_id, materials)