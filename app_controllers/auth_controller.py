from views.login_view import LoginView
from models.user_model import UserModel
import views.main_view
from views.main_view import EstimatorWindow


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
        if self.user_model.verify_user(username, password):
            self.login_view.close()
            self.main_view = EstimatorWindow()
            self.main_view.show()
        else:
            self.login_view.show_error("Неверный логин или пароль")