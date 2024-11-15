import sys
from PySide6.QtWidgets import QApplication
from app_controllers.auth_controller import AuthController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open("resourses/style.qss", "r") as style_file:
        app.setStyleSheet(style_file.read())
    # Создаем и показываем окно авторизации через контроллер
    auth_controller = AuthController()
    auth_controller.show_login()

    sys.exit(app.exec())