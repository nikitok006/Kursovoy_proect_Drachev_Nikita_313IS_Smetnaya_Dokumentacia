from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QComboBox, QLabel, QPushButton, QWidget, QMessageBox
from PySide6.QtCore import Qt, Signal

from views.main_view import EstimatorWindow


class ProjectSelectionView(QMainWindow):

    def __init__(self, controller, session):
        super().__init__()
        self.controller = controller
        self.session = session
        self.setWindowTitle("Выбор проекта")
        self.setGeometry(300, 300, 400, 200)

        # Основной виджет
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Основной макет
        self.layout = QVBoxLayout(self.central_widget)

        # Надпись
        self.label = QLabel("Выберите проект:", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        # Выпадающий список
        self.project_combobox = QComboBox(self)
        self.layout.addWidget(self.project_combobox)

        # Кнопка подтверждения выбора
        self.select_button = QPushButton("Выбрать проект", self)
        self.select_button.clicked.connect(self.select_project)
        self.layout.addWidget(self.select_button)

    def populate_projects(self, projects):
        """
        Заполняет выпадающий список проектами из базы данных.
        :param projects: Список проектов (каждый проект - словарь с id и названием).
        """
        self.project_combobox.clear()
        for project in projects:
            self.project_combobox.addItem(project["name"], project["id"])

    def select_project(self):
        """
        Обработчик выбора проекта.
        """
        selected_id = self.project_combobox.currentData()
        if selected_id is not None:
            self.session.set_current_project(selected_id)  # Устанавливаем текущий проект
            self.controller.estimates_table()  # Вызываем обновление таблицы
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Не выбран проект.")
