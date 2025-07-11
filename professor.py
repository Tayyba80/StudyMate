import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QPushButton, QLabel, QVBoxLayout,
    QHBoxLayout, QStackedWidget, QSizePolicy,
    QLineEdit, QMessageBox, QTextEdit, QGridLayout, QFrame, QDateEdit
    ,QSpacerItem
)
from PyQt5.QtCore import QDate,Qt
from data import users, quizzes, assignments, notifications,course_contents,reminders
from PyQt5.QtGui import QFont

events = []
materials = []

class ProfessorDashboard(QMainWindow):
    def __init__(self, logout_callback):
        super().__init__()
        self.saved_events = []
        self.logout_callback = logout_callback
        self.setWindowTitle("Professor Dashboard")
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
            "Create Assignments": 1,
            "Add Quizs": 2,
            "Add Important Notifications": 3,
            "Add Course Material": 4,
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
            if name == "Dashboard":
                btn.clicked.connect(self.update_dashboard_page)
            else:
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
        self.pages.addWidget(self.create_assignments())
        self.pages.addWidget(self.create_quiz())
        self.pages.addWidget(self.add_notification())
        self.pages.addWidget(self.add_course_content())

        main_layout.addWidget(sidebar_widget)
        main_layout.addWidget(self.pages)

        self.pages.setCurrentIndex(0)

    def update_dashboard_page(self):
        total_quiz = len(quizzes)
        assignmentsDue = len(assignments)
        total_Rem = len(reminders)

        self.update_dashboard_card(self.dashboard_widget, "Due Quizes", total_quiz, "#3498db")
        self.update_dashboard_card(self.dashboard_widget, "Due Assignments to take", assignmentsDue, "#9b59b6")
        self.update_dashboard_card(self.dashboard_widget, "Reminders", total_Rem, "#1abc9c")
        self.pages.removeWidget(self.dashboard_widget)
        self.dashboard_widget.deleteLater()
        self.dashboard_widget = self.dashboard_page()
        self.pages.insertWidget(0, self.dashboard_widget)
        self.pages.setCurrentIndex(0)



    def dashboard_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(10)

        welcome_label = QLabel("Welcome to Professor Dashboard 👋")
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
        rem = len(reminders)

        card_layout.addWidget(create_card("Due Quizzes", total_quizzes, "#3498db"), 0, 0)
        card_layout.addWidget(create_card("Assignments to take", total_due_assignments, "#9b59b6"), 0, 1)
        card_layout.addWidget(create_card("Reminders", rem, "#1abc9c"), 1, 0, 1, 2) 

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


    def create_assignments(self):
        widget = QWidget()
        layout = QVBoxLayout()

        title_label = QLabel("Assignment Title:")
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter the assignment title...")
        self.title_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
            }
        """)
        desc_label = QLabel("Description:")
        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Enter a brief description...")
        self.desc_input.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                min-height: 150px;
            }
        """)
        date_label = QLabel("Due Date:")
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setStyleSheet("""
            QDateEdit {
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
            }
        """)

        course_label = QLabel("Course Name:")
        self.course_input = QLineEdit()
        self.course_input.setPlaceholderText("Enter the course name...")
        self.course_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
            }
        """)
        submit_button = QPushButton("Create Assignment")
        submit_button.setStyleSheet("""
            QPushButton {
                background-color: #4A90E2;
                color: white;
                font-size: 18px;
                border-radius: 10px;
                padding: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: #357ABD;
            }
        """)
        submit_button.clicked.connect(self.save_assignment)
        layout.addWidget(title_label)
        layout.addWidget(self.title_input)
        layout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        layout.addWidget(desc_label)
        layout.addWidget(self.desc_input)
        layout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        layout.addWidget(date_label)
        layout.addWidget(self.date_input)
        layout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        layout.addWidget(course_label)
        layout.addWidget(self.course_input)
        layout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        layout.addWidget(submit_button)
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        widget.setLayout(layout)
        return widget
            
    def save_assignment(self):
        title = self.title_input.text()
        description = self.desc_input.toPlainText()
        due_date = self.date_input.date().toString("yyyy-MM-dd")
        course = self.course_input.text()

        if not title or not description or not course:
            QMessageBox.warning(None, "Input Error", "Please fill in all fields.")
            return

        assignment = {
            "title": title,
            "description": description,
            "due_date": due_date,
            "course": course
        }

        assignments.append(assignment)
        QMessageBox.information(None, "Success", "Assignment created successfully!")

        self.title_input.clear()
        self.desc_input.clear()
        self.course_input.clear()
        self.date_input.setDate(QDate.currentDate())
        for assignment in assignments:
            print(assignment)


    def create_quiz(self):
        widget = QWidget()
        layout = QVBoxLayout()

        titleQ_label = QLabel("Quiz Topics:")
        self.titleQ_input = QLineEdit()
        self.titleQ_input.setPlaceholderText("Enter the quiz topic...")
        self.titleQ_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
            }
        """)
        
        descQ_label = QLabel("Description:")
        self.descQ_input = QTextEdit()
        self.descQ_input.setPlaceholderText("Enter a brief description about the nature of quiz...")
        self.descQ_input.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                min-height: 150px;
            }
        """)

        dateQ_label = QLabel("Quiz Date:")
        self.dateQ_input = QDateEdit()
        self.dateQ_input.setCalendarPopup(True)
        self.dateQ_input.setDate(QDate.currentDate())
        self.dateQ_input.setStyleSheet("""
            QDateEdit {
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
            }
        """)

        courseQ_label = QLabel("Course Name:")
        self.courseQ_input = QLineEdit()
        self.courseQ_input.setPlaceholderText("Enter the course name...")
        self.courseQ_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
            }
        """)

        submit_button = QPushButton("Create Quiz")
        submit_button.setStyleSheet("""
            QPushButton {
                background-color: #4A90E2;
                color: white;
                font-size: 18px;
                border-radius: 10px;
                padding: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: #357ABD;
            }
        """)
        submit_button.clicked.connect(self.save_quiz)

        layout.addWidget(titleQ_label)
        layout.addWidget(self.titleQ_input)
        layout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        layout.addWidget(descQ_label)
        layout.addWidget(self.descQ_input)
        layout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        layout.addWidget(dateQ_label)
        layout.addWidget(self.dateQ_input)
        layout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        layout.addWidget(courseQ_label)
        layout.addWidget(self.courseQ_input)
        layout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        layout.addWidget(submit_button)
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        widget.setLayout(layout)
        return widget
            
    def save_quiz(self):
        topic = self.titleQ_input.text()
        descriptionQ = self.descQ_input.toPlainText()
        dueQ_date = self.dateQ_input.date().toString("yyyy-MM-dd")
        courseQ = self.courseQ_input.text()

        if not topic or not descriptionQ or not courseQ:
            QMessageBox.warning(None, "Input Error", "Please fill in all fields.")
            return

        quizz = {
            "topics": topic,
            "description": descriptionQ,
            "due_date": dueQ_date,
            "course": courseQ
        }

        quizzes.append(quizz)
        QMessageBox.information(None, "Success", "Quiz created successfully!")

        self.titleQ_input.clear()
        self.descQ_input.clear()
        self.courseQ_input.clear()
        self.dateQ_input.setDate(QDate.currentDate())

    
    def add_notification(self):
        widget = QWidget()
        widget.setStyleSheet("""
            QWidget {
                background-color: #f5f7fa;
            }
        """)
        
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        card = QWidget()
        card_layout = QVBoxLayout()
        card.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 15px;
                padding: 25px;
                max-width: 500px;
                box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
            }
        """)

        header = QLabel("🔔 Create New Notification")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: #4A90E2; margin-bottom: 20px;")

        titleN_label = QLabel("Notification Subject:")
        titleN_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.titleN_input = QLineEdit()
        self.titleN_input.setPlaceholderText("e.g., Class Cancelled, Urgent Update")
        self.titleN_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
            }
            QLineEdit:focus {
                border: 1.5px solid #4A90E2;
                background-color: #f0f8ff;
            }
        """)

        descN_label = QLabel("Description:")
        descN_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.descN_input = QTextEdit()
        self.descN_input.setPlaceholderText("Write details of the notification...")
        self.descN_input.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                min-height: 120px;
            }
            QTextEdit:focus {
                border: 1.5px solid #4A90E2;
                background-color: #f0f8ff;
            }
        """)

        submit_button = QPushButton("🚀 Send Notification")
        submit_button.setCursor(Qt.PointingHandCursor)
        submit_button.setStyleSheet("""
            QPushButton {
                background-color: #4A90E2;
                color: white;
                font-size: 18px;
                font-weight: bold;
                border-radius: 10px;
                padding: 12px;
                margin-top: 15px;
            }
            QPushButton:hover {
                background-color: #357ABD;
            }
        """)
        submit_button.clicked.connect(self.save_noti)

        card_layout.addWidget(header)
        card_layout.addWidget(titleN_label)
        card_layout.addWidget(self.titleN_input)
        card_layout.addSpacing(10)
        card_layout.addWidget(descN_label)
        card_layout.addWidget(self.descN_input)
        card_layout.addWidget(submit_button)
        card.setLayout(card_layout)

        main_layout.addWidget(card)
        widget.setLayout(main_layout)
        return widget

    def save_noti(self):
        topicN = self.titleN_input.text()
        descriptionN = self.descN_input.toPlainText()

        if not topicN or not descriptionN:
            QMessageBox.warning(None, "Input Error", "Please fill in all fields.")
            return

        notification = {
            "topics": topicN,
            "description": descriptionN,
        }

        notifications.append(notification)
        QMessageBox.information(None, "Success", "Notification alert added successfully!")

        self.titleN_input.clear()
        self.descN_input.clear()


    def add_course_content(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        header = QLabel("📚 Add Course Content")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #4A90E2;
                margin-bottom: 20px;
                padding: 10px;
                background-color: #e6f2fb;
                border: 2px solid #4A90E2;
                border-radius: 12px;
            }
        """)
        layout.addWidget(header)

        name_label = QLabel("Course Name:")
        name_label.setStyleSheet("font-size: 16px; font-weight: 600; color: #333;")
        self.course_name_input = QLineEdit()
        self.course_name_input.setPlaceholderText("e.g., Data Structures")
        self.course_name_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
            }
        """)

        content_label = QLabel("Course Content:")
        content_label.setStyleSheet("font-size: 16px; font-weight: 600; color: #333;")
        self.course_content_input = QTextEdit()
        self.course_content_input.setPlaceholderText("Enter the detailed course material or summary...")
        self.course_content_input.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                min-height: 150px;
            }
        """)

        submit_button = QPushButton("Add Content")
        submit_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 18px;
                font-weight: bold;
                border-radius: 10px;
                padding: 10px;
                margin-top: 15px;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
        """)
        submit_button.clicked.connect(self.save_course_content)

        layout.addWidget(name_label)
        layout.addWidget(self.course_name_input)
        layout.addSpacing(10)
        layout.addWidget(content_label)
        layout.addWidget(self.course_content_input)
        layout.addWidget(submit_button)

        widget.setLayout(layout)
        return widget

    def save_course_content(self):
        course_name = self.course_name_input.text().strip()
        course_text = self.course_content_input.toPlainText().strip()

        if not course_name or not course_text:
            QMessageBox.warning(None, "Incomplete", "Please fill in both the course name and content.")
            return

        course_contents.append({
            "name": course_name,
            "content": course_text
        })
        QMessageBox.information(None, "Saved", f"Course content for '{course_name}' added successfully!")
        self.course_name_input.clear()
        self.course_content_input.clear()


    def logout(self):
        self.logout_callback()
        self.close()


