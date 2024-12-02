from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QLineEdit, QPushButton, QComboBox, QWidget, QMessageBox
from reportlab.lib.rl_safe_eval import eval_debug


class CommentCreationWindow(QWidget):
    def __init__(self, controller, update):
        super().__init__()
        self.controller = controller
        self.update = update
        self.setWindowTitle("Добавление комментария")
        self.resize(400, 300)

        # Элементы интерфейса
        self.layout = QVBoxLayout(self)

        self.label_select_estimate = QLabel("Выберите смету:")
        self.estimate_combo_box = QComboBox(self)
        self.select_button = QPushButton("Выбрать проект")
        self.select_button.clicked.connect(self.add_comment)

        self.label_comment = QLabel("Введите комментарий:")
        self.comment_input = QLineEdit()

        self.save_button = QPushButton("Сохранить комментарий")
        self.save_button.clicked.connect(self.add_comment)
        self.cancel_button = QPushButton("Отмена")

        # Добавление виджетов на компоновку
        self.layout.addWidget(self.label_select_estimate)
        self.layout.addWidget(self.estimate_combo_box)
        self.layout.addWidget(self.label_comment)
        self.layout.addWidget(self.comment_input)
        self.layout.addWidget(self.save_button)
        self.layout.addWidget(self.cancel_button)
        self.populate_projects()

    def add_comment(self):
        """Сохраняет комментарий через контроллер."""
        comment = self.comment_input.text()
        if not comment:
            QMessageBox.warning(self, "Ошибка", "Комментарий не может быть пустым.")
            return
        estimate = self.estimate_combo_box.currentText().split()
        estimate_number = int(estimate[2])
        self.controller.add_comment(estimate_number, comment)
        self.update()
        self.close()


    def populate_projects(self):
        #Заполняет выпадающий список проектами.
        estimates = self.controller.get_estimates()
        for estimate in estimates:
            display_text = f"Номер сметы: {estimate['id']}   Дата составления: {estimate['name']}"  # Формируем текст для отображения
            self.estimate_combo_box.addItem(display_text, estimate["id"])  # Добавляем текст и сохраняем ID


