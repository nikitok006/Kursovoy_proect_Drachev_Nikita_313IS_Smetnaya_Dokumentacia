from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QLabel, QLineEdit, QComboBox,QMessageBox, QPushButton, QListWidget, QAbstractItemView, QWidget
)


class CreateEstimateWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Создание сметы")
        self.setGeometry(300, 300, 400, 400)

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Поле для ввода номера сметы
        self.estimate_number_input = QLineEdit()
        self.estimate_number_input.setPlaceholderText("Введите номер сметы")
        layout.addWidget(QLabel("Номер сметы:"))
        layout.addWidget(self.estimate_number_input)

        # Список доступных материалов
        self.materials_list = QListWidget()
        self.materials_list.setSelectionMode(QAbstractItemView.MultiSelection)
        layout.addWidget(QLabel("Выберите материалы:"))
        layout.addWidget(self.materials_list)

        # Кнопка для сохранения сметы
        self.save_button = QPushButton("Сохранить смету")
        self.save_button.clicked.connect(self.save_estimate)
        layout.addWidget(self.save_button)

        # Загрузка материалов
        self.populate_materials()

    def populate_materials(self):
        """
        Заполняет список материалов.
        """
        materials = self.controller.get_materials()
        for material in materials:
            self.materials_list.addItem(f"{material['id']}: {material['name']}")

    def save_estimate(self):
        """
        Сохраняет смету через контроллер.
        """
        estimate_number = self.estimate_number_input.text()
        selected_items = self.materials_list.selectedItems()
        selected_materials = [int(item.text().split(":")[0]) for item in selected_items]

        if not estimate_number:
            self.show_error("Пожалуйста, введите номер сметы.")
            return

        if not selected_materials:
            self.show_error("Пожалуйста, выберите хотя бы один материал.")
            return

        self.controller.save_estimate(estimate_number, selected_materials)
        self.close()

    def show_error(self, message):
        """
        Показывает сообщение об ошибке.
        """
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("Ошибка")
        error_dialog.setText(message)
        error_dialog.exec()
