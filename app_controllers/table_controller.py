from views.project_select_window import ProjectSelectionView
from views.main_view import EstimatorWindow


class ProjectController:
    def __init__(self, model, estimate_controller, report_controller, session):
        self.session = session
        self.model = model
        self.main = EstimatorWindow(self, estimate_controller, report_controller, session)


    def get_all_projects(self):
        """
        Отображает окно выбора проекта.
        """
        print(self.session.get_current_user())
        return self.model.get_all_projects(self.session.get_current_user())


    def estimates_table(self):
        """
        Обновляет таблицу смет в главном окне для указанного проекта.
        """
        print("обновляем")
        return  self.main.update_estimates_table()






