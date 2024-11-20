from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QLabel, QMenuBar,
    QStatusBar, QLineEdit)

import app_controllers.table_controller
from views.project_select_window import ProjectSelectionView
from PySide6.QtGui import QAction
from PySide6.QtCore import QSize, Qt
from views.estimate_create import CreateEstimateWindow
from  app_controllers.table_controller import ProjectController


class EstimatorWindow(QMainWindow):
    """Основное окно пользователя-сметчика."""
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        # Настройка окна
        self.setWindowTitle("Система Сметного Документооборота")
        self.setMinimumSize(QSize(800, 600))

        # Создание меню
        self.create_menu()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Основной вертикальный макет для центрального виджета
        main_layout = QVBoxLayout()

        # Панель действий (кнопки для основных функций)
        action_layout = QHBoxLayout()
        """Создает основные кнопки для действий."""
        self.create_estimate_button = QPushButton("Создать смету", self)
        self.create_estimate_button.clicked.connect(self.open_estimate_creation_window)
        action_layout.addWidget(self.create_estimate_button)

        self.estimate_list_button = QPushButton("Выбрать проект")
        self.estimate_list_button.clicked.connect(self.controller.show_project_selection_window)
        action_layout.addWidget(self.estimate_list_button)

        self.approved_estimates_button = QPushButton("Утвержденные сметы")
        self.approved_estimates_button.clicked.connect(self.show_approved_estimates)
        action_layout.addWidget(self.approved_estimates_button)

        self.create_report_button = QPushButton("Создать отчет")
        self.create_report_button.clicked.connect(self.create_report)
        action_layout.addWidget(self.create_report_button)

        main_layout.addLayout(action_layout)

        # Таблица для отображения смет
        self.estimate_table = QTableWidget()
        self.estimate_table.setColumnCount(6)
        self.estimate_table.setHorizontalHeaderLabels(["Номер сметы", "Тип", "Название", "Статус", "Бюджет", "Дата"])
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

    def open_estimate_creation_window(self):
        """Открывает окно для создания новой сметы."""
        self.status_bar.showMessage("Открытие окна создания сметы...")
        self.estimate_creation_window = CreateEstimateWindow()
        self.estimate_creation_window.show()

    # Обработчики других кнопок
    # def show_estimate_list(self):
    #     app_controllers.table_controller.ProjectController()


    def show_approved_estimates(self):
        self.status_bar.showMessage("Показ утвержденных смет")
        # Логика отображения утвержденных смет
        print("Показ утвержденных смет")

    def create_report(self):
        self.status_bar.showMessage("Создание отчета")
        # Логика создания отчета
        print("Создание отчета")


