from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMessageBox, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, \
    QWidget, QHBoxLayout, QStatusBar, QMenuBar, QMenu, QDialog
from PySide6.QtCore import QSize, Qt

from views.comment_window import CommentCreationWindow
from views.Selected_estimate import SelectEstimateDialog
from views.edit_estimate_dialog import EditEstimateDialog
from views.project_select_window import ProjectSelectionView

class CommentWindow(QMainWindow):
    def __init__(self, project_controller, estimate_controller, report_controller, session):
        super().__init__()
        self.session = session
        self.project_controller = project_controller
        self.estimate_controller = estimate_controller
        self.report_controller = report_controller

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

        self.estimate_list_button = QPushButton("Выбрать проект")
        self.estimate_list_button.clicked.connect(self.open_project_selection)
        action_layout.addWidget(self.estimate_list_button)

        self.create_report_button = QPushButton("Создать отчет")
        self.create_report_button.clicked.connect(self.open_select_estimate_dialog)
        action_layout.addWidget(self.create_report_button)

        main_layout.addLayout(action_layout)

        # Таблица смет
        self.estimate_table = QTableWidget()
        self.estimate_table.setColumnCount(4)  # Устанавливаем количество столбцов
        self.estimate_table.setHorizontalHeaderLabels(
            ["Номер сметы", "Итоговая сумма", "Дата составления", "Комментарий"])
        self.estimate_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.estimate_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.estimate_table.customContextMenuRequested.connect(self.show_context_menu)
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
        self.comment = CommentCreationWindow(self.estimate_controller, self.update_estimates_table)
        self.comment.show()


    def open_project_selection(self):
        """Открывает окно выбора проекта."""
        dialog = ProjectSelectionView(
            self.project_controller,
            self.session,
            self.update_estimates_table  # Передаём метод как колбэк
        )
        dialog.exec()

    def open_select_estimate_dialog(self):
        """
        Открывает диалоговое окно выбора сметы для отчета.
        """
        if self.session.get_current_project() is not None:
            dialog = SelectEstimateDialog(self.estimate_controller, self.session)
            if dialog.exec() == QDialog.Accepted:
                selected_estimate = dialog.selected_estimate
                if selected_estimate:
                    print(f"Выбранная смета: {selected_estimate}")
                    self.report_controller.create_report_for_estimate(selected_estimate)
        else:
            QMessageBox.warning(self, "Ошибка", "Не выбран проект.")

    def show_context_menu(self, position):
        """Отображает контекстное меню при клике правой кнопкой."""
        menu = QMenu()
        edit_action = menu.addAction("Показать")
        action = menu.exec(self.estimate_table.viewport().mapToGlobal(position))
        if action == edit_action:
            selected_row = self.estimate_table.currentRow()
            if selected_row >= 0:
                estimate_number = self.estimate_table.item(selected_row, 0).text()
                self.open_edit_estimate_dialog(estimate_number)

    def open_edit_estimate_dialog(self, estimate_number):
        """Открывает диалог для редактирования выбранной сметы."""
        dialog = EditEstimateDialog(self.estimate_controller, estimate_number)
        dialog.exec_()
        self.update_estimates_table()  # Обновляем таблицу после редактирования