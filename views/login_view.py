from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PySide6.QtCore import Signal

class LoginView(QDialog):
    login_signal = Signal(str, str)  # Сигнал, передающий логин и пароль

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Авторизация")
        self.setGeometry(100, 100, 300, 150)

        layout = QVBoxLayout()

        # Поле ввода логина
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Логин")
        layout.addWidget(self.username_input)

        # Поле ввода пароля
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        # Кнопка входа
        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.emit_login_signal)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def emit_login_signal(self):
        """Отправка сигнала с учетными данными."""
        username = self.username_input.text()
        password = self.password_input.text()
        self.login_signal.emit(username, password)

    def show_error(self, message):
        """Отображение сообщения об ошибке."""
        QMessageBox.warning(self, "Ошибка", message)