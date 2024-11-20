from views.project_select_window import ProjectSelectionView

class ProjectController:
    def __init__(self, model):
        self.model = model
        self.view = ProjectSelectionView(self)

    def show_project_selection_window(self):
        """
        Отображает окно выбора проекта.
        """
        print(23)
        projects = self.model.get_all_projects()
        self.view.populate_projects(projects)
        self.view.show()

    def handle_project_selection(self, project_id):
        """
        Обрабатывает выбор проекта.
        :param project_id: ID выбранного проекта.
        """
        print(f"Проект с ID {project_id} выбран.")
        # Здесь можно добавить логику для перехода на другое окно
