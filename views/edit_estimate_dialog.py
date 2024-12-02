from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel, QHBoxLayout


class EditEstimateDialog(QDialog):
    def __init__(self, estimate_controller, estimate_number):
        super().__init__()
        self.estimate_controller = estimate_controller
        self.estimate_number = estimate_number
        self.setWindowTitle(f"Редактирование сметы № {estimate_number}")
        self.setMinimumSize(600, 400)

        # Основной макет
        layout = QVBoxLayout(self)

        # Таблица материалов
        self.materials_table = QTableWidget()
        self.materials_table.setColumnCount(3)
        self.materials_table.setHorizontalHeaderLabels(["Материал", "Количество", "Цена за единицу"])
        layout.addWidget(self.materials_table)

        # Кнопки
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Сохранить изменения")
        self.save_button.clicked.connect(self.save_changes)
        button_layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

        self.populate_materials()

    def populate_materials(self):
        """Заполняет таблицу материалами (включая те, которые ещё не добавлены в смету)."""
        materials = self.estimate_controller.get_materials_for_editing(self.estimate_number)
        self.materials_table.setRowCount(len(materials))

        for row, material in enumerate(materials):
            # Наименование материала
            self.materials_table.setItem(row, 0, QTableWidgetItem(material["name"]))

            # Количество (редактируемое поле)
            quantity_item = QTableWidgetItem(str(material["quantity"]))
            self.materials_table.setItem(row, 1, quantity_item)

            # Цена за единицу (не редактируется)
            cost_item = QTableWidgetItem(str(material["cost_per_unit"]))
            cost_item.setFlags(cost_item.flags() ^ Qt.ItemIsEditable)
            self.materials_table.setItem(row, 2, cost_item)

    def save_changes(self):
        """Сохраняет изменения в смете."""
        updated_materials = []
        for row in range(self.materials_table.rowCount()):
            name = self.materials_table.item(row, 0).text()
            quantity = float(self.materials_table.item(row, 1).text())
            cost_per_unit = float(self.materials_table.item(row, 2).text())
            updated_materials.append({"name": name, "quantity": quantity, "cost_per_unit": cost_per_unit})

        self.estimate_controller.update_estimate(self.estimate_number, updated_materials)
        self.accept()

