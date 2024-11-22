from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QMenuBar,
    QStatusBar, QTableWidgetItem)

from PySide6.QtGui import QAction
from PySide6.QtCore import QSize
from views.estimate_create import CreateEstimateWindow




class EstimatorWindow(QMainWindow):
    def __init__(self, project_controller, estimate_controller):
        super().__init__()
        self.project_controller = project_controller
        self.estimate_controller = estimate_controller

        # Настройка окна
        self.setWindowTitle("Система Сметного Документооборота")
        self.setMinimumSize(QSize(800, 600))

        # Создание меню
        self.create_menu()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Основной макет
        main_layout = QVBoxLayout()

        # Панель действий
        action_layout = QHBoxLayout()
        self.create_estimate_button = QPushButton("Создать смету", self)
        self.create_estimate_button.clicked.connect(self.open_estimate_creation_window)
        action_layout.addWidget(self.create_estimate_button)

        self.estimate_list_button = QPushButton("Выбрать проект")
        self.estimate_list_button.clicked.connect(project_controller.show_project_selection_window)
        action_layout.addWidget(self.estimate_list_button)

        self.approved_estimates_button = QPushButton("Утвержденные сметы")
        action_layout.addWidget(self.approved_estimates_button)

        self.create_report_button = QPushButton("Создать отчет")
        action_layout.addWidget(self.create_report_button)

        main_layout.addLayout(action_layout)

        # Таблица смет
        self.estimate_table = QTableWidget()
        self.estimate_table.setColumnCount(6)
        self.estimate_table.setHorizontalHeaderLabels(["Номер сметы", "Тип", "Название", "Статус", "Бюджет", "Дата"])
        main_layout.addWidget(self.estimate_table)

        # Строка состояния
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        central_widget.setLayout(main_layout)

        # Установка колбэка
        # self.estimate_controller.set_update_table_callback(self.update_estimates_table)
        self.update_estimates_table()

    def update_estimates_table(self):
        pass
        # estimates = self.estimate_controller.get_all_estimates()
        # self.estimate_table.setRowCount(len(estimates))
        # for row, estimate in enumerate(estimates):
        #     self.estimate_table.setItem(row, 0, QTableWidgetItem(str(estimate["estimate_number"])))
        #     self.estimate_table.setItem(row, 1, QTableWidgetItem(estimate["type"]))
        #     self.estimate_table.setItem(row, 2, QTableWidgetItem(estimate["name"]))
        #     self.estimate_table.setItem(row, 3, QTableWidgetItem(estimate["status"]))
        #     self.estimate_table.setItem(row, 4, QTableWidgetItem(str(estimate["budget"])))
        #     self.estimate_table.setItem(row, 5, QTableWidgetItem(estimate["date"]))

    def create_menu(self):
        menu_bar = QMenuBar(self)
        file_menu = menu_bar.addMenu("Файл")
        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        self.setMenuBar(menu_bar)

    def open_estimate_creation_window(self):
        """Открывает окно для создания новой сметы."""
        self.status_bar.showMessage("Открытие окна создания сметы...")
        self.estimate_creation_window = CreateEstimateWindow(self.estimate_controller)
        self.estimate_creation_window.show()

