from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QLabel, QLineEdit, QTableWidget,QTableWidgetItem, QMessageBox, QPushButton, QListWidget, QAbstractItemView, QWidget
)
from PySide6.QtCore import Qt


class CreateEstimateWindow(QMainWindow):
    def __init__(self, controller, session, update_table_callback):
        super().__init__()
        self.controller = controller
        self.session = session
        self.update_table_callback = update_table_callback
        print(f"Переданный контроллер: {self.controller}")

        self.setWindowTitle("Создание сметы")
        self.setGeometry(300, 300, 600, 400)

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Поле для ввода номера сметы
        self.estimate_number_input = QLineEdit()
        self.estimate_number_input.setPlaceholderText("Введите номер сметы")
        layout.addWidget(QLabel("Номер сметы:"))
        layout.addWidget(self.estimate_number_input)

        # Таблица для отображения материалов и ввода количества
        self.materials_table = QTableWidget()
        self.materials_table.setColumnCount(4)
        self.materials_table.setHorizontalHeaderLabels([ "Материал", "Ед. изм.", "Стоимость за единицу", "Количество"])
        self.materials_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(QLabel("Материалы:"))
        layout.addWidget(self.materials_table)

        # Кнопка для сохранения сметы
        self.save_button = QPushButton("Сохранить смету")
        self.save_button.clicked.connect(self.save_estimate)
        layout.addWidget(self.save_button)

        # Загрузка материалов
        self.populate_materials()

    def populate_materials(self):
        """
        Заполняет таблицу материалов.
        """
        materials = self.controller.get_materials()
        self.materials_table.setRowCount(len(materials))


        for row, material in enumerate(materials):
            # ID материала
            id_item = material["id"]
            # id_item.setFlags(id_item.flags() ^ Qt.ItemIsEditable)  # ID нельзя редактировать
            # # self.materials_table.setItem(row, 0, id_item)

            # Название материала
            name_item = QTableWidgetItem(material['name'])
            name_item.setFlags(name_item.flags() ^ Qt.ItemIsEditable)  # Название нельзя редактировать
            self.materials_table.setItem(row, 0, name_item)

            # Единица измерения
            unit_item = QTableWidgetItem(material['unit'])
            unit_item.setFlags(unit_item.flags() ^ Qt.ItemIsEditable)  # Единица измерения тоже
            self.materials_table.setItem(row, 1, unit_item)

            cost = QTableWidgetItem(str(material['cost_per_unit']) + "0 ₽")
            cost.setFlags(cost.flags() ^ Qt.ItemIsEditable)  # Единица измерения тоже
            self.materials_table.setItem(row, 2, cost)

            # Количество
            quantity_item = QTableWidgetItem("0")
            self.materials_table.setItem(row, 3, quantity_item)

    def save_estimate(self):
        """
        Сохраняет смету через контроллер.
        """
        materials = self.controller.get_materials()
        estimate_number = self.estimate_number_input.text()
        if not estimate_number:
            self.show_error("Пожалуйста, введите номер сметы.")
            return

        materials_with_quantity = []
        for row, material in enumerate(materials):
            material_id = material["id"]
            quantity_text = self.materials_table.item(row, 3).text()


            # Проверка корректности введенного количества
            try:
                quantity = float(quantity_text)
                if quantity <= 0:
                    continue  # Пропускаем материалы с нулевым или отрицательным количеством
            except ValueError:
                # self.show_error(f"Некорректное количество для материала ID {material_id}.")
                return

            materials_with_quantity.append({"id": material_id,"quantity": quantity})

        if not materials_with_quantity:
            self.show_error("Пожалуйста, выберите хотя бы один материал с корректным количеством.")
            return

        # Сохранение через контроллер
        self.controller.save_estimate(estimate_number, materials_with_quantity, self.session)
        self.update_table_callback()
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

