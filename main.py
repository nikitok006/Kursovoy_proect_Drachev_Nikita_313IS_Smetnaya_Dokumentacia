import sys
from PySide6.QtWidgets import QApplication
from app_controllers.estimate_controller import EstimateController
from app_controllers.auth_controller import AuthController
from app_controllers.table_controller import ProjectController
from models.table_projects_model import ProjectModel
from models.estimate_model import EstimateModel
from views.main_view import EstimatorWindow
from app_controllers.session import Session

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Применяем стили, если файл существует
    try:
        with open("resourses/style.qss", "r") as style_file:
            app.setStyleSheet(style_file.read())
    except FileNotFoundError:
        print("Файл стилей не найден. Используются стандартные стили.")

    # Создаём сессию
    session = Session()

    # Инициализация моделей
    project_model = ProjectModel()
    estimate_model = EstimateModel()

    # Инициализация контроллеров

    estimate_controller = EstimateController(estimate_model, session)
    project_controller = ProjectController(project_model, estimate_controller ,session)
    # Инициализация контроллера авторизации
    auth_controller = AuthController(project_controller, estimate_controller, session)

    # Создание главного окна
    main_window = EstimatorWindow(project_controller, estimate_controller, session)

    # Привязка кнопок
    main_window.estimate_list_button.clicked.connect(project_controller.show_project_selection_window)

    # Устанавливаем колбэк для обновления таблицы
    estimate_controller.set_update_table_callback(main_window.update_estimates_table)

    # Показываем окно авторизации
    auth_controller.show_login()

    # Запускаем приложение
    sys.exit(app.exec())
