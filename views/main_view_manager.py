from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHBoxLayout,QStatusBar, QMenuBar, QMenu
from PySide6.QtCore import QSize

from views.comment_window import CommentCreationWindow

class CommentWindow(QMainWindow):
    def __init__(self, project_controller, estimate_controller, session):
        super().__init__()
        self.session = session
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
        self.create_estimate_button = QPushButton("Оставить коментарий", self)
        self.create_estimate_button.clicked.connect(self.leave_comment)
        action_layout.addWidget(self.create_estimate_button)

        self.update_button = QPushButton("Обновить таблицу")
        self.update_button.clicked.connect(self.update_estimates_table)
        action_layout.addWidget(self.update_button)

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
        self.estimate_table.setColumnCount(4)  # Устанавливаем количество столбцов
        self.estimate_table.setHorizontalHeaderLabels(
            ["Номер сметы", "Итоговая сумма", "Дата составления", "Комментарий"])
        main_layout.addWidget(self.estimate_table)

        # Строка состояния
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        central_widget.setLayout(main_layout)

        # Установка колбэка
        # self.estimate_controller.set_update_table_callback(self.update_estimates_table)
        # self.update_estimates_table()

    def update_estimates_table(self):
        # self.estimate_table.setRowCount(1)
        # self.estimate_table.setItem(0, 0, QTableWidgetItem("Тестовая смета"))
        # self.estimate_table.setItem(0, 1, QTableWidgetItem("10000"))
        # self.estimate_table.setItem(0, 2, QTableWidgetItem("2024-11-24 15:00:00"))
        # self.estimate_table.setItem(0, 3, QTableWidgetItem("Тестовый комментарий"))
        """
        # Обновляет таблицу смет для текущего проекта.
        # """
        current_project_id = self.session.get_current_project()
        if current_project_id is not None:
            estimates = self.estimate_controller.get_all_estimates()
            print(estimates)
            print(current_project_id)
            self.estimate_table.clearContents()
            self.estimate_table.setRowCount(len(estimates))  # Устанавливаем количество строк

            for row, estimate in enumerate(estimates):
                self.estimate_table.setItem(row, 0, QTableWidgetItem(str(estimate.get("estimate_number", ""))))
                self.estimate_table.setItem(row, 1, QTableWidgetItem(str(estimate.get("total_cost", ""))))
                self.estimate_table.setItem(row, 2, QTableWidgetItem(str(estimate.get("created_at", ""))))
                self.estimate_table.setItem(row, 3, QTableWidgetItem(str(estimate.get("comment", ""))))

    def create_menu(self):
        menu_bar = QMenuBar(self)
        file_menu = menu_bar.addMenu("Файл")
        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        self.setMenuBar(menu_bar)

        # Сигнал для кнопки комментариев
        # self.comment_button.clicked.connect(self.leave_comment)

    def leave_comment(self):
        self.comment = CommentCreationWindow()
        self.comment.show()