import sys
from PySide6.QtWidgets import QApplication
from PySide6.scripts.pyside_tool import project

from app_controllers.auth_controller import AuthController
from app_controllers.table_controller import ProjectController
from models.table_estimate_model import ProjectModel
from views.project_select_window import ProjectSelectionView
from views.main_view import EstimatorWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open("resourses/style.qss", "r") as style_file:
        app.setStyleSheet(style_file.read())
    # Создаем и показываем окно авторизации через контроллер
    model = ProjectModel()
    controller = ProjectController(model)
    auth_controller = AuthController(controller)
    auth_controller.show_login()
    main_window = EstimatorWindow(controller)
    print(main_window.estimate_list_button)
    main_window.estimate_list_button.clicked.connect(ProjectController.show_project_selection_window)
    sys.exit(app.exec())