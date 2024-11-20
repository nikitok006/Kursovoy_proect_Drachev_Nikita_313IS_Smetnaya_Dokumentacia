from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QLineEdit, QPushButton, QComboBox, QWidget, QMessageBox



class CommentCreationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавление комментария")
        self.resize(400, 300)

        # Элементы интерфейса
        self.layout = QVBoxLayout(self)

        self.label_select_estimate = QLabel("Выберите смету:")
        self.estimate_combo_box = QComboBox()

        self.label_comment = QLabel("Введите комментарий:")
        self.comment_input = QLineEdit()

        self.save_button = QPushButton("Сохранить комментарий")
        self.cancel_button = QPushButton("Отмена")

        # Добавление виджетов на компоновку
        self.layout.addWidget(self.label_select_estimate)
        self.layout.addWidget(self.estimate_combo_box)
        self.layout.addWidget(self.label_comment)
        self.layout.addWidget(self.comment_input)
        self.layout.addWidget(self.save_button)
        self.layout.addWidget(self.cancel_button)

        # Загрузка данных в выпадающий список
        # self.load_estimates_from_db()

        # Привязка сигналов к кнопкам
        # self.save_button.clicked.connect(self.save_comment)
        # self.cancel_button.clicked.connect(self.close)