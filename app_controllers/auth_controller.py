from views.login_view import LoginView
from models.user_model import UserModel
from views.main_view import EstimatorWindow
from views.main_view_manager import CommentWindow

class AuthController:
    def __init__(self):
        self.login_view = LoginView()
        self.user_model = UserModel()

        # Подключаем сигнал авторизации к методу проверки
        self.login_view.login_signal.connect(self.check_credentials)

    def show_login(self):
        """Отображение окна авторизации."""
        self.login_view.show()

    def check_credentials(self, username, password):
        """Проверка учетных данных."""
        if self.user_model.login_user(username, password):
            self.login_view.close()
            print(self.user_model.role(username))
            if self.user_model.role(username) == 1:
                self.main_view = EstimatorWindow()
                self.main_view.show()
            else:
                self.main_view = CommentWindow()
                self.main_view.show()
        else:
            self.login_view.show_error("Неверный логин или пароль")
