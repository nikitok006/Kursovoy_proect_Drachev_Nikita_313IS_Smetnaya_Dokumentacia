from app_controllers import estimate_controller
from views.login_view import LoginView
from models.user_model import UserModel
from views.main_view_manager import CommentWindow
from views.main_view import EstimatorWindow
from views.project_select_window import ProjectSelectionView


class AuthController:
    def __init__(self, controller, estimate_controller, report_controller, session):

        self.login_view = LoginView()
        self.user_model = UserModel()
        self.controller = controller
        self.estimate_controller = estimate_controller
        self.session = session
        # self.project_selection_window = ProjectSelectionView(self, self.session)
        self.report_controller = report_controller

        # Подключаем сигнал авторизации к методу проверки
        self.login_view.login_signal.connect(self.check_credentials)

    def show_login(self):
        """Отображение окна авторизации."""
        self.login_view.show()

    def check_credentials(self, username, password):
        """Проверка учетных данных."""
        if self.user_model.login_user(username, password):
            self.session.set_current_user(username)
            self.login_view.close()
            if self.user_model.role(username) == 1:
                self.main_view = EstimatorWindow(self.controller, self.estimate_controller, self.report_controller, self.session)
                self.main_view.show()
            else:
                self.main_view = CommentWindow(self.controller, self.estimate_controller, self.report_controller, self.session)
                self.main_view.show()
        else:
            self.login_view.show_error("Неверный логин или пароль")

