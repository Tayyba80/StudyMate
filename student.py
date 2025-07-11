import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QLabel, QVBoxLayout,
    QHBoxLayout, QStackedWidget, QSizePolicy, QTableWidget, QTableWidgetItem,
    QLineEdit, QMessageBox, QFormLayout, QTextEdit, QGridLayout, QFrame, QDateEdit
    ,QScrollArea,QGroupBox,QSpacerItem
)
from PyQt5.QtCore import QDate
from PyQt5.QtCore import Qt
from data import users, quizzes, assignments, notifications, course_contents
from PyQt5.QtGui import QFont

events = []
materials = []

class StudentDashboard(QMainWindow):
    def __init__(self, logout_callback):
        super().__init__()
        self.saved_events = []
        self.logout_callback = logout_callback
        self.setWindowTitle("Student Dashboard")
        self.resize(1000, 650)
        self.setStyleSheet("background-color: #ffffff;")

        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        sidebar = QVBoxLayout()
        sidebar.setSpacing(15)
        sidebar.setAlignment(Qt.AlignTop)

        app_name_label = QLabel("StudyMate")
        app_name_label.setFont(QFont("Georgia", 16, QFont.Bold))
        app_name_label.setStyleSheet("""
            color: #2c3e50;
            margin-bottom: 25px;
            letter-spacing: 1.5px;
            font-style: italic;
        """)
        app_name_label.setAlignment(Qt.AlignCenter)
        sidebar.addWidget(app_name_label)

        self.buttons = {}
        nav_items = {
            "Dashboard": 0,
            "View Assignments": 1,
            "Quizs": 2,
            "Notifications": 3,
            "Course Material": 4,
        }

        button_style = """
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px 15px;
                border-radius: 8px;
                font-size: 18px;
                font-weight: bold;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """

        for name, index in nav_items.items():
            btn = QPushButton(f"{name}")
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setStyleSheet(button_style)
            btn.setFont(QFont("Segoe UI", 10))
            btn.clicked.connect(lambda checked, i=index: self.pages.setCurrentIndex(i))

            sidebar.addWidget(btn)
            self.buttons[name] = btn

        logout_btn = QPushButton("Logout")
        logout_btn.setFont(QFont("Segoe UI", 10))
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 10px 15px;
                border-radius: 8px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        logout_btn.clicked.connect(self.logout)
        sidebar.addWidget(logout_btn)
        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar)
        sidebar_widget.setFixedWidth(400)
        sidebar_widget.setStyleSheet("background-color: #ecf0f1; padding: 20px;")

        self.pages = QStackedWidget()
        self.dashboard_widget = self.dashboard_page()  
        self.pages.addWidget(self.dashboard_widget)
        self.pages.addWidget(self.assignments())
        self.pages.addWidget(self.quiz())
        self.pages.addWidget(self.see_notification())
        self.pages.addWidget(self.see_course_content())

        main_layout.addWidget(sidebar_widget)
        main_layout.addWidget(self.pages)
        self.pages.setCurrentIndex(0)


    def dashboard_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(10)

        welcome_label = QLabel("Welcome to Student Dashboard 👋")
        welcome_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        welcome_label.setStyleSheet("color: #34495e;")
        welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome_label)

        card_layout = QGridLayout()
        card_layout.setSpacing(20)

        def create_card(title, value, color):
            card = QFrame()
            card.setStyleSheet(f"""
                background-color: {color};
                border-radius: 10px;
                padding: 20px;
                color: white;
            """)
            card_layout_inner = QVBoxLayout()
            title_label = QLabel(title)
            title_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
            value_label = QLabel(str(value))
            value_label.setFont(QFont("Segoe UI", 22, QFont.Bold))
            card_layout_inner.addWidget(title_label)
            card_layout_inner.addWidget(value_label)
            card.setLayout(card_layout_inner)
            return card

        total_quizzes = len(quizzes)
        total_due_assignments = len(assignments)
        notification = len(notifications)
        card_layout.addWidget(create_card("Total Quizzes", total_quizzes, "#3498db"), 0, 0)
        card_layout.addWidget(create_card("Due Assignments", total_due_assignments, "#9b59b6"), 0, 1)
        card_layout.addWidget(create_card("Notifications", notification, "#1abc9c"), 1, 0, 1, 2)  # Span across two columns
        layout.addLayout(card_layout)
        page.setLayout(layout)
        self.setLayout(layout)
        return page

    def update_dashboard_card(self, dashboard_widget, title, value, color):
        card_layout = dashboard_widget.layout().itemAt(1).layout()
        for i in range(card_layout.count()):
            card = card_layout.itemAt(i).widget()
            title_label = card.layout().itemAt(0).widget()
            value_label = card.layout().itemAt(1).widget()
            if title_label.text() == title:
                value_label.setText(str(value))
                break


    def assignments(self):
        layout = QVBoxLayout()
        header_label = QLabel("Assignments")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #4A90E2;
            margin-bottom: 20px;
        """)
        layout.addWidget(header_label)
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        today = QDate.currentDate()

        if not assignments:
            alert = QLabel("⚠️  No assignments available.")
            alert.setStyleSheet("""
                QLabel {
                    background-color: #fff3cd;
                    color: #856404;
                    border: 1px solid #ffeeba;
                    padding: 12px;
                    border-radius: 8px;
                    font-size: 16px;
                }
            """)
            alert.setAlignment(Qt.AlignCenter)
            layout.addWidget(alert)
        else:
            for assignment in assignments:
                due_date = QDate.fromString(assignment['due_date'], "yyyy-MM-dd")
                if due_date >= today:
                    group = QGroupBox(f"{assignment['title']} ({assignment['course']})")
                    group.setStyleSheet("""
                        QGroupBox {
                            background-color: #f9f9f9;
                            border: 1px solid #4A90E2;
                            border-radius: 12px;
                            padding: 10px;
                            margin-bottom: 15px;
                        }
                        QGroupBox::title {
                            color: #4A90E2;
                            font-size: 20px;
                            font-weight: bold;
                            padding: 5px;
                        }
                    """)

                    group_layout = QVBoxLayout()
                    group_layout.setContentsMargins(15, 15, 15, 15) 
                    group_layout.addWidget(QLabel(f"Description: {assignment['description']}"))
                    group_layout.addWidget(QLabel(f"Due Date: {assignment['due_date']}"))
                    group.setLayout(group_layout)
                    layout.addWidget(group)

        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        scroll = QScrollArea()
        container = QWidget()
        container.setLayout(layout)
        scroll.setWidget(container)
        scroll.setWidgetResizable(True)

        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #f1f1f1;
            }
            QScrollBar:vertical {
                border: none;
                background: #e0e0e0;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #4A90E2;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
            }
        """)
        final_layout = QVBoxLayout()
        final_layout.addWidget(scroll)

        main_widget = QWidget()
        main_widget.setLayout(final_layout)
        return main_widget


    def refresh_table(self, table):
        table.setRowCount(0)  
        for i, (user, (pw, role)) in enumerate(users.items()):
            table.insertRow(i)
            table.setItem(i, 0, QTableWidgetItem(user))
            table.setItem(i, 1, QTableWidgetItem(role))

    def quiz(self):
        layout = QVBoxLayout()
        header_label = QLabel("Quiz")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #4A90E2;
            margin-bottom: 20px;
        """)
        layout.addWidget(header_label)
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        today = QDate.currentDate()

        if not quizzes:
            alert = QLabel("⚠️  No Quiz so far YAY!.")
            alert.setStyleSheet("""
                QLabel {
                    background-color: #fff3cd;
                    color: #856404;
                    border: 1px solid #ffeeba;
                    padding: 12px;
                    border-radius: 8px;
                    font-size: 16px;
                }
            """)
            alert.setAlignment(Qt.AlignCenter)
            layout.addWidget(alert)
        else:
            for quiz in quizzes:
                due_date = QDate.fromString(quiz['due_date'], "yyyy-MM-dd")
                if due_date >= today:
                    group = QGroupBox(f"{quiz['topics']} ({quiz['course']})")
                    group.setStyleSheet("""
                        QGroupBox {
                            background-color: #f9f9f9;
                            border: 1px solid #4A90E2;
                            border-radius: 12px;
                            padding: 10px;
                            margin-bottom: 15px;
                        }
                        QGroupBox::title {
                            color: #4A90E2;
                            font-size: 20px;
                            font-weight: bold;
                            padding: 5px;
                        }
                    """)

                    group_layout = QVBoxLayout()
                    group_layout.setContentsMargins(15, 15, 15, 15)  
                    group_layout.addWidget(QLabel(f"Description: {quiz['description']}"))
                    group_layout.addWidget(QLabel(f"Due Date: {quiz['due_date']}"))
                    
                    group.setLayout(group_layout)
                    layout.addWidget(group)

        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        scroll = QScrollArea()
        container = QWidget()
        container.setLayout(layout)
        scroll.setWidget(container)
        scroll.setWidgetResizable(True)

        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #f1f1f1;
            }
            QScrollBar:vertical {
                border: none;
                background: #e0e0e0;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #4A90E2;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
            }
        """)

        final_layout = QVBoxLayout()
        final_layout.addWidget(scroll)
        main_widget = QWidget()
        main_widget.setLayout(final_layout)

        return main_widget

    def see_notification(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        header_label = QLabel("🔔 Notifications Center")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("""
            QLabel {
                font-size: 32px;
                font-weight: 800;
                color: #4A90E2;
                padding: 15px;
                border-radius: 12px;
                background-color: #e6f0fb;
                border: 2px solid #4A90E2;
            }
        """)
        layout.addWidget(header_label)
        layout.addSpacing(20)

        if not notifications:
            empty_label = QLabel("✅ No new notifications at the moment!")
            empty_label.setAlignment(Qt.AlignCenter)
            empty_label.setStyleSheet("font-size: 18px; color: #888; padding: 20px;")
            layout.addWidget(empty_label)
        else:
            for noti in notifications:
                group = QGroupBox()
                group.setStyleSheet("""
                    QGroupBox {
                        background-color: #ffffff;
                        border: 1.5px solid #4A90E2;
                        border-radius: 12px;
                        padding: 15px;
                        margin-bottom: 15px;
                        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
                    }
                """)

                title_label = QLabel(f"📢 {noti['topics']}")
                title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #4A90E2;")

                desc_label = QLabel(f"{noti['description']}")
                desc_label.setWordWrap(True)
                desc_label.setStyleSheet("font-size: 16px; color: #333; padding-top: 5px;")

                group_layout = QVBoxLayout()
                group_layout.addWidget(title_label)
                group_layout.addWidget(desc_label)
                group.setLayout(group_layout)

                layout.addWidget(group)
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        scroll = QScrollArea()
        container = QWidget()
        container.setLayout(layout)
        scroll.setWidget(container)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #f1f4f8;
            }
            QScrollBar:vertical {
                background: #e0e0e0;
                width: 10px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #4A90E2;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
            }
        """)

        final_layout = QVBoxLayout()
        final_layout.addWidget(scroll)

        main_widget = QWidget()
        main_widget.setLayout(final_layout)

        return main_widget


    def see_course_content(self):
        layout = QVBoxLayout()
        header_label = QLabel("📚 Course Contents")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #2C3E50;
            margin-bottom: 20px;
        """)
        layout.addWidget(header_label)

        layout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        if not course_contents:
            empty_label = QLabel("No course contents available yet.")
            empty_label.setAlignment(Qt.AlignCenter)
            empty_label.setStyleSheet("font-size: 18px; color: #7f8c8d;")
            layout.addWidget(empty_label)
        else:
            for course in course_contents:
                group = QGroupBox(f"📘 {course['name']}")
                group.setStyleSheet("""
                    QGroupBox {
                        background-color: #fdfdfd;
                        border: 1.5px solid #3498DB;
                        border-radius: 12px;
                        padding: 12px;
                        margin-bottom: 16px;
                    }
                    QGroupBox::title {
                        color: #3498DB;
                        font-size: 20px;
                        font-weight: bold;
                    }
                """)
                content_layout = QVBoxLayout()
                content_label = QLabel(course['content'])
                content_label.setWordWrap(True)
                content_label.setStyleSheet("font-size: 16px; color: #2c3e50;")
                content_layout.addWidget(content_label)
                group.setLayout(content_layout)
                layout.addWidget(group)
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        scroll = QScrollArea()
        container = QWidget()
        container.setLayout(layout)
        scroll.setWidget(container)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #f1f1f1;
            }
            QScrollBar:vertical {
                background: #ecf0f1;
                width: 10px;
            }
            QScrollBar::handle:vertical {
                background: #3498DB;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
            }
        """)

        final_layout = QVBoxLayout()
        final_layout.addWidget(scroll)

        main_widget = QWidget()
        main_widget.setLayout(final_layout)
        return main_widget

    
    def logout(self):
        self.logout_callback()
        self.close()


