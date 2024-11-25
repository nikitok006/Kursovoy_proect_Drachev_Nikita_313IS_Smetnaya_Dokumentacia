from views.project_select_window import ProjectSelectionView
from views.main_view import EstimatorWindow


class ProjectController:
    def __init__(self, model, estimate_controller, report_controller, session):
        self.session = session
        self.model = model
        self.view = ProjectSelectionView(self, session)
        self.main = EstimatorWindow(self, estimate_controller, report_controller, session)


    def show_project_selection_window(self):
        """
        Отображает окно выбора проекта.
        """
        print(self.session.get_current_user())
        projects = self.model.get_all_projects(self.session.get_current_user())
        self.view.populate_projects(projects)
        self.view.show()

    def estimates_table(self):
        """
        Обновляет таблицу смет в главном окне для указанного проекта.
        """
        self.main.update_estimates_table()






