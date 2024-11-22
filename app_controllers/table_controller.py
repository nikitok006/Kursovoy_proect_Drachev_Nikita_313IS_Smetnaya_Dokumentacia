from views.project_select_window import ProjectSelectionView



class ProjectController:
    def __init__(self, model, session):
        self.session = session
        self.model = model
        self.view = ProjectSelectionView(self)

    def show_project_selection_window(self):
        """
        Отображает окно выбора проекта.
        """
        print(self.session.get_current_user())
        projects = self.model.get_all_projects(self.session.get_current_user())
        self.view.populate_projects(projects)
        self.view.show()

    def handle_project_selection(self, project_id):
        """
        Обрабатывает выбор проекта.
        :param project_id: ID выбранного проекта.
        """
        return project_id
        # Здесь можно добавить логику для перехода на другое окно
