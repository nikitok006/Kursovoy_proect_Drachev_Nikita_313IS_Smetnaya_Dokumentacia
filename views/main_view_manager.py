from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHBoxLayout, QMenuBar, QMenu
from views.comment_window import CommentCreationWindow

class CommentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Система Сметного Документооборота")
        self.resize(800, 600)

        # Главное меню
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        file_menu = QMenu("Файл", self)
        view_menu = QMenu("Вид", self)
        help_menu = QMenu("Справка", self)

        self.menu_bar.addMenu(file_menu)
        self.menu_bar.addMenu(view_menu)
        self.menu_bar.addMenu(help_menu)

        # Основной виджет
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Верхняя панель кнопок
        button_layout = QHBoxLayout()

        self.comment_button = QPushButton("Оставить комментарий")
        self.list_button = QPushButton("Список смет")
        self.approved_button = QPushButton("Утвержденные сметы")
        self.report_button = QPushButton("Создать отчет")

        button_layout.addWidget(self.comment_button)
        button_layout.addWidget(self.list_button)
        button_layout.addWidget(self.approved_button)
        button_layout.addWidget(self.report_button)

        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Номер сметы", "Тип", "Название", "Статус", "Бюджет", "Дата"])

        # Основной компоновщик
        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table)

        central_widget.setLayout(main_layout)

        # Сигнал для кнопки комментариев
        self.comment_button.clicked.connect(self.leave_comment)

    def leave_comment(self):
        self.comment = CommentCreationWindow()
        self.comment.show()