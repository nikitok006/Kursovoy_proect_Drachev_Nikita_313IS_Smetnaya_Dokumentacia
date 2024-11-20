from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QPushButton, QListWidget, QFormLayout, QSpinBox
)
from PySide6.QtGui import QAction
from PySide6.QtCore import QSize, Qt

class CreateEstimateWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Создание сметы")
        self.setGeometry(100, 100, 500, 400)

        # Центральный виджет
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Основной макет
        self.layout = QVBoxLayout()

        # Поле для названия сметы
        form_layout = QFormLayout()
        self.estimate_name_input = QLineEdit()
        form_layout.addRow("Название сметы:", self.estimate_name_input)

        # Тип сметы
        self.estimate_type_combo = QComboBox()
        self.estimate_type_combo.addItems(["Локальная", "Объектная", "Сводная"])
        form_layout.addRow("Тип сметы:", self.estimate_type_combo)

        # Бюджет сметы
        self.budget_input = QSpinBox()
        self.budget_input.setMaximum(10_000_000)
        self.budget_input.setPrefix("₽ ")
        form_layout.addRow("Бюджет:", self.budget_input)

        self.layout.addLayout(form_layout)

        # Список материалов
        self.materials_combo = QComboBox()
        self.materials_combo.addItems(["Бетон", "Арматура", "Кирпич", "Песок", "Цемент"])
        self.add_material_button = QPushButton("Добавить материал")
        self.add_material_button.clicked.connect(self.add_material)  # Подключение кнопки

        materials_layout = QHBoxLayout()
        materials_layout.addWidget(self.materials_combo)
        materials_layout.addWidget(self.add_material_button)

        self.layout.addLayout(materials_layout)

        # Выбранные материалы
        self.materials_list = QListWidget()
        self.layout.addWidget(QLabel("Выбранные материалы:"))
        self.layout.addWidget(self.materials_list)

        # Кнопка сохранения
        self.save_button = QPushButton("Сохранить смету")
        # self.save_button.clicked.connect(self.save_estimate)
        self.layout.addWidget(self.save_button, alignment=Qt.AlignmentFlag.AlignRight)

        # Установка макета
        self.central_widget.setLayout(self.layout)

    def add_material(self):
        """Добавить материал из выпадающего списка в список материалов."""
        material = self.materials_combo.currentText()
        if material not in [self.materials_list.item(i).text() for i in range(self.materials_list.count())]:
            self.materials_list.addItem(material)

        # Установка макета в виджет
        self.setLayout(self.layout)