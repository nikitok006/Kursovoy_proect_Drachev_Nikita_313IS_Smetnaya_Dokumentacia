from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QLabel, QMenuBar,
    QStatusBar, QLineEdit, QTextEdit, QMessageBox
)
from PySide6.QtGui import QAction
from PySide6.QtCore import QSize, Qt


class EstimateCreationWindow(QWidget):
    """Окно для создания новой сметы."""

    def __init__(self):
        super().__init__()

        # Настройка окна
        self.setWindowTitle("Создание сметы")
        self.setMinimumSize(QSize(400, 300))

        # Макет и виджеты для ввода данных сметы
        layout = QVBoxLayout()

        # Поля для ввода данных сметы
        self.estimate_number_input = QLineEdit()
        self.estimate_number_input.setPlaceholderText("Введите номер сметы")

        self.estimate_description_input = QTextEdit()
        self.estimate_description_input.setPlaceholderText("Введите описание сметы")

        # Кнопка для сохранения сметы
        self.save_button = QPushButton("Сохранить смету")
        self.save_button.clicked.connect(self.save_estimate)

        # Добавление виджетов в макет
        layout.addWidget(QLabel("Номер сметы:"))
        layout.addWidget(self.estimate_number_input)
        layout.addWidget(QLabel("Описание сметы:"))
        layout.addWidget(self.estimate_description_input)
        layout.addWidget(self.save_button)

        # Установка макета в виджет
        self.setLayout(layout)

    def save_estimate(self):
        """Обработчик для сохранения сметы."""
        estimate_number = self.estimate_number_input.text()
        estimate_description = self.estimate_description_input.toPlainText()
        print(f"Сохранена смета №{estimate_number} с описанием: {estimate_description}")
        # Дополнительная логика сохранения сметы, например, в базу данных или файл


class EstimatorWindow(QMainWindow):
    """Основное окно пользователя-сметчика."""

    def __init__(self):
        super().__init__()

        # Настройка окна
        self.setWindowTitle("Система Сметного Документооборота")
        self.setMinimumSize(QSize(800, 600))

        # Создание меню
        self.create_menu()

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Основной вертикальный макет для центрального виджета
        main_layout = QVBoxLayout()

        # Панель действий (кнопки для основных функций)
        action_layout = QHBoxLayout()
        self.create_buttons(action_layout)
        main_layout.addLayout(action_layout)

        # Таблица для отображения смет
        self.estimate_table = QTableWidget()
        self.estimate_table.setColumnCount(3)
        self.estimate_table.setHorizontalHeaderLabels(["Номер сметы", "Описание", "Статус"])
        main_layout.addWidget(self.estimate_table)

        # Добавление макета к центральному виджету
        central_widget.setLayout(main_layout)

        # Строка состояния
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def create_menu(self):
        """Создает меню приложения."""
        menu_bar = QMenuBar(self)

        # Главное меню
        file_menu = menu_bar.addMenu("Файл")
        view_menu = menu_bar.addMenu("Вид")
        help_menu = menu_bar.addMenu("Справка")

        # Пункты меню
        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Добавляем меню в окно
        self.setMenuBar(menu_bar)

    def create_buttons(self, layout):
        """Создает основные кнопки для действий."""
        self.create_estimate_button = QPushButton("Создать смету")
        self.create_estimate_button.clicked.connect(self.open_estimate_creation_window)
        layout.addWidget(self.create_estimate_button)

        self.estimate_list_button = QPushButton("Список смет")
        self.estimate_list_button.clicked.connect(self.show_estimate_list)
        layout.addWidget(self.estimate_list_button)

        self.approved_estimates_button = QPushButton("Утвержденные сметы")
        self.approved_estimates_button.clicked.connect(self.show_approved_estimates)
        layout.addWidget(self.approved_estimates_button)

        self.create_report_button = QPushButton("Создать отчет")
        self.create_report_button.clicked.connect(self.create_report)
        layout.addWidget(self.create_report_button)

    def open_estimate_creation_window(self):
        """Открывает окно для создания новой сметы."""
        self.status_bar.showMessage("Открытие окна создания сметы...")
        self.estimate_creation_window = EstimateCreationWindow()
        self.estimate_creation_window.show()

    # Обработчики других кнопок
    def show_estimate_list(self):
        self.status_bar.showMessage("Показ списка смет")
        # Логика отображения списка смет
        print("Показ списка смет")

    def show_approved_estimates(self):
        self.status_bar.showMessage("Показ утвержденных смет")
        # Логика отображения утвержденных смет
        print("Показ утвержденных смет")

    def create_report(self):
        self.status_bar.showMessage("Создание отчета")
        # Логика создания отчета
        print("Создание отчета")


