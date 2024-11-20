from PySide6.QtWidgets import QApplication
from views.login_view import LoginView
from views.main_view import EstimateCreationWindow

class NavigationController:
    def __init__(self):
        self.auth_window = None
        self.estimate_window = None

    def show_login(self):
        if not self.auth_window:
            self.auth_window = LoginView()
        self.auth_window.show()

    def show_estimate_creation(self):
        if not self.estimate_window:
            self.estimate_window = EstimateCreationWindow()
        self.auth_window.close()  # Закрываем окно авторизации
        self.estimate_window.show()
