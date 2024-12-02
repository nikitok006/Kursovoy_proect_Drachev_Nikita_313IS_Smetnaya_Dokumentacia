from PySide6.QtWidgets import QDialog, QVBoxLayout, QComboBox, QLabel, QPushButton, QMessageBox


class ProjectSelectionView(QDialog):
    def __init__(self, project_controller, session, update_table_callback):
        super().__init__()
        self.project_controller = project_controller
        self.session = session
        self.update_table_callback = update_table_callback

        self.setWindowTitle("Выбор проекта")
        self.setGeometry(300, 300, 400, 200)

        # Основной макет
        layout = QVBoxLayout(self)

        # Выпадающий список проектов
        self.project_combobox = QComboBox(self)
        self.select_button = QPushButton("Выбрать проект")
        self.select_button.clicked.connect(self.select_project)

        layout.addWidget(QLabel("Выберите проект:"))
        layout.addWidget(self.project_combobox)
        layout.addWidget(self.select_button)

        self.populate_projects()

    def populate_projects(self):
        #Заполняет выпадающий список проектами.
        projects = self.project_controller.get_all_projects()
        print(projects)
        for project in projects:
            self.project_combobox.addItem(project["name"], project["id"])

    def select_project(self):
        """Обрабатывает выбор проекта."""
        selected_project_id = self.project_combobox.currentData()
        if selected_project_id:
            self.session.set_current_project(selected_project_id)  # Сохраняем текущий проект в сессии
            self.update_table_callback()  # Вызываем колбэк для обновления таблицы
            self.accept()  # Закрываем диалог
        else:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите проект.")
