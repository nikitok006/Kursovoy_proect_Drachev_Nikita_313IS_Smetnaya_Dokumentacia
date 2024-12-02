from PySide6.QtGui import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QMessageBox


class SelectEstimateDialog(QDialog):
    def __init__(self, estimate_controller, session):
        super().__init__()
        self.setWindowTitle("Выберите смету для отчета")
        self.setMinimumSize(600, 400)
        self.estimate_controller = estimate_controller
        self.session = session

        # Основной макет
        layout = QVBoxLayout(self)

        # Таблица смет
        self.estimate_table = QTableWidget()
        self.estimate_table.setColumnCount(3)
        self.estimate_table.setHorizontalHeaderLabels(["Номер сметы", "Общая стоимость", "Комментарий"])
        layout.addWidget(self.estimate_table)

        # Кнопки "Выбрать" и "Отмена"
        button_layout = QHBoxLayout()
        self.select_button = QPushButton("Выбрать")
        self.select_button.clicked.connect(self.select_estimate)
        button_layout.addWidget(self.select_button)

        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

        # Загрузка данных
        self.populate_estimates()

    def populate_estimates(self):
        """
        Заполняет таблицу смет данными из контроллера.
        """
        current_project_id = self.session.get_current_project()
        if current_project_id is  not None:
            estimates = self.estimate_controller.get_all_estimates(current_project_id)
            self.estimate_table.setRowCount(len(estimates))
            for row, estimate in enumerate(estimates):
                id_item = QTableWidgetItem()
                id_item.setData(Qt.UserRole, estimate["id"])  # Сохраняем ID сметы
                id_item.setText(str(estimate["estimate_number"]))  # Отображаем номер сметы
                self.estimate_table.setItem(row, 0, id_item)
                self.estimate_table.setItem(row, 1, QTableWidgetItem(str(estimate["total_cost"])))
                self.estimate_table.setItem(row, 2, QTableWidgetItem(estimate["comment"]))

        else:
            QMessageBox.warning(self, "Ошибка", "Проект не выбран.")
            self.reject()

    def select_estimate(self):
        """
        Обрабатывает выбор сметы.
        """
        current_row = self.estimate_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите смету.")
            return

        self.selected_estimate = {
            "id": self.estimate_table.item(current_row, 0).data(Qt.UserRole),  # ID сметы
            "estimate_number": self.estimate_table.item(current_row, 0).text(),
            "total_cost": self.estimate_table.item(current_row, 1).text(),
            "comment": self.estimate_table.item(current_row, 2).text(),
        }
        self.accept()
