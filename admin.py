import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QLabel, QVBoxLayout,
    QHBoxLayout, QStackedWidget, QSizePolicy, QTableWidget, QTableWidgetItem,
    QLineEdit, QMessageBox, QFormLayout, QTextEdit, QGridLayout, QFrame, QDateEdit
    ,QScrollArea
)
from PyQt5.QtCore import QDate
from PyQt5.QtCore import Qt
from data import users
from PyQt5.QtGui import QFont

events = []
materials = []

class AdminDashboard(QMainWindow):
    def __init__(self, logout_callback):
        super().__init__()
        self.saved_events = []
        self.logout_callback = logout_callback
        self.setWindowTitle("Admin Dashboard")
        self.resize(1000, 650)
        self.setStyleSheet("background-color: #ffffff;")

        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        sidebar = QVBoxLayout()
        sidebar.setSpacing(15)
        sidebar.setAlignment(Qt.AlignTop)

        app_name_label = QLabel("StudyMate Admin")
        app_name_label.setFont(QFont("Georgia", 16, QFont.Bold))
        app_name_label.setStyleSheet("""
            color: #2c3e50;
            margin-bottom: 25px;
            letter-spacing: 1.5px;
            font-style: italic;
        """)
        app_name_label.setAlignment(Qt.AlignCenter)
        sidebar.addWidget(app_name_label)

        # Buttons and navigation
        self.buttons = {}
        nav_items = {
            "Dashboard": 0,
            "Manage Users": 1,
            "Events": 2,
            "System Status": 3,
            "Add Admin": 4,
            "Add Professor": 5
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
        self.pages.addWidget(self.manage_users_page())
        self.pages.addWidget(self.events_page())
        #self.pages.addWidget(self.materials_page())
        self.pages.addWidget(self.system_status_page())
        self.pages.addWidget(self.add_admin_page())
        self.pages.addWidget(self.add_professor_page())

        main_layout.addWidget(sidebar_widget)
        main_layout.addWidget(self.pages)

        self.pages.setCurrentIndex(0)

    def update_dashboard_page(self):
        total_users = len(users)
        total_admins = sum(1 for u in users.values() if u[1] == "Admin")
        total_professors = sum(1 for u in users.values() if u[1] == "Professor")
        total_events = len(events)  

        self.update_dashboard_card(self.dashboard_widget, "Total Users", total_users, "#3498db")
        self.update_dashboard_card(self.dashboard_widget, "Admins", total_admins, "#9b59b6")
        self.update_dashboard_card(self.dashboard_widget, "Professors", total_professors, "#1abc9c")
        self.update_dashboard_card(self.dashboard_widget, "Events", total_events, "#e67e22")
        
        self.pages.setCurrentIndex(0)  


    def dashboard_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(10)

        welcome_label = QLabel("Welcome to StudyMate Admin Dashboard 👋")
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

        total_users = len(users)
        total_admins = sum(1 for u in users.values() if u[1] == "Admin")
        total_professors = sum(1 for u in users.values() if u[1] == "Professor")
        total_events = 5  # to replace 

        card_layout.addWidget(create_card("Total Users", total_users, "#3498db"), 0, 0)
        card_layout.addWidget(create_card("Admins", total_admins, "#9b59b6"), 0, 1)
        card_layout.addWidget(create_card("Professors", total_professors, "#1abc9c"), 1, 0)
        card_layout.addWidget(create_card("Events", total_events, "#e67e22"), 1, 1)

        layout.addLayout(card_layout)
        page.setLayout(layout)
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


    def manage_users_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        table = QTableWidget(len(users), 2)
        table.setHorizontalHeaderLabels(["Username", "Role"])

        table.setStyleSheet("""
            QTableWidget {
                background-color: #f8f9fa;
                font-family: 'Segoe UI', sans-serif;
                font-size: 16px;
                border: 2px solid #bdc3c7;
                gridline-color: #7f8c8d;
                alternate-background-color: #e8f0fe;
            }
            QHeaderView::section {
                background-color: #2c3e50;
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
                border: 2px solid #7f8c8d;
            }
            QTableWidget::item {
                padding: 10px;
                border: 1px solid #7f8c8d;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QTableWidget::item:hover {
                background-color: #d6eaf8;
            }
            QTableCornerButton::section {
                background-color: #2c3e50;
                border: 2px solid #7f8c8d;
            }
        """)

        table.setAlternatingRowColors(True)

        for i, (user, (pw, role)) in enumerate(users.items()):
            table.setItem(i, 0, QTableWidgetItem(user))
            table.setItem(i, 1, QTableWidgetItem(role))

        table.resizeColumnsToContents()
        for i in range(len(users)):
            table.setRowHeight(i, 50)

        table.horizontalHeader().setStretchLastSection(True)
        table.verticalHeader().setVisible(False)

        layout.addWidget(table)
        self.update_manage_users_table = lambda: self.refresh_table(table)

        page.setLayout(layout)
        return page



    def refresh_table(self, table):
        table.setRowCount(0)  
        for i, (user, (pw, role)) in enumerate(users.items()):
            table.insertRow(i)
            table.setItem(i, 0, QTableWidgetItem(user))
            table.setItem(i, 1, QTableWidgetItem(role))

    def events_page(self):
        page = QWidget()
        outer_layout = QVBoxLayout()
        outer_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        form_container = QWidget()
        form_layout = QVBoxLayout(form_container)
        form_layout.setAlignment(Qt.AlignCenter)
        form_layout.setSpacing(15)

        self.event_name_input = QLineEdit()
        self.event_name_input.setPlaceholderText("Enter event name")
        self.event_name_input.setFixedWidth(400)
        self.event_name_input.setStyleSheet("""
            QLineEdit {
                padding: 14px;
                font-size: 16px;
                border: 2px solid #ccc;
                border-radius: 12px;
                background-color: #ffffff;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: #ecf5fd;
            }
        """)

        start_date_label = QLabel("Event Start Date:")
        self.event_start_date_input = QDateEdit()
        self.event_start_date_input.setDisplayFormat("yyyy-MM-dd")
        self.event_start_date_input.setStyleSheet("""
            QDateEdit {
                padding: 14px;
                font-size: 16px;
                border: 2px solid #ccc;
                border-radius: 12px;
                background-color: #ffffff;
            }
            QDateEdit:focus {
                border-color: #3498db;
                background-color: #ecf5fd;
            }
        """)

        end_date_label = QLabel("Event End Date:")
        self.event_deadline_input = QDateEdit()
        self.event_deadline_input.setDisplayFormat("yyyy-MM-dd")
        self.event_deadline_input.setStyleSheet("""
            QDateEdit {
                padding: 14px;
                font-size: 16px;
                border: 2px solid #ccc;
                border-radius: 12px;
                background-color: #ffffff;
            }
            QDateEdit:focus {
                border-color: #3498db;
                background-color: #ecf5fd;
            }
        """)

        add_event_btn = QPushButton("Add Event")
        add_event_btn.setFixedWidth(200)
        add_event_btn.clicked.connect(self.add_event)
        add_event_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 12px;
                font-size: 16px;
                border: none;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        show_all_btn = QPushButton("Show All Events")
        show_all_btn.setFixedWidth(200)
        show_all_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                padding: 12px;
                font-size: 16px;
                border: none;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        show_all_btn.clicked.connect(self.refresh_event_list)

        form_layout.addWidget(self.event_name_input)
        form_layout.addWidget(start_date_label)
        form_layout.addWidget(self.event_start_date_input)
        form_layout.addWidget(end_date_label)
        form_layout.addWidget(self.event_deadline_input)
        form_layout.addWidget(add_event_btn)
        form_layout.addWidget(show_all_btn)

        # --- Scroll area to display events ---
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; }")

        self.event_list_widget = QWidget()
        self.event_list = QVBoxLayout(self.event_list_widget)
        self.event_list.setSpacing(12)
        self.event_list.setContentsMargins(10, 10, 10, 10)
        self.event_list.setAlignment(Qt.AlignTop)

        scroll_area.setWidget(self.event_list_widget)

        outer_layout.addWidget(form_container)
        outer_layout.addWidget(scroll_area)
        outer_layout.setContentsMargins(40, 40, 40, 40)
        outer_layout.setSpacing(20)

        page.setLayout(outer_layout)
        page.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', sans-serif;
                background-color: #f5f7fa;
            }
            QLabel {
                font-size: 14px;
                color: #34495e;
            }
        """)

        return page

    def add_event(self):
        event_name = self.event_name_input.text().strip()
        start_date_str = self.event_start_date_input.text().strip()
        end_date_str = self.event_deadline_input.text().strip()

        if not event_name or not start_date_str or not end_date_str:
            self.show_message("All fields are required.", "Error")
            return
        try:
            start_date = QDate.fromString(start_date_str, "yyyy-MM-dd")
            end_date = QDate.fromString(end_date_str, "yyyy-MM-dd")
        except ValueError:
            self.show_message("Please enter valid dates in the format YYYY-MM-DD.", "Error")
            return

        if start_date > end_date:
            self.show_message("Start date must be earlier than end date.", "Error")
            return

        event = {
            'name': event_name,
            'start_date': start_date.toString("yyyy-MM-dd"),
            'end_date': end_date.toString("yyyy-MM-dd")
        }
        self.saved_events.append(event)
        self.show_message("Event added successfully!", "Success")
        self.event_name_input.clear()
        self.event_start_date_input.clear()
        self.event_deadline_input.clear()


    def show_message(self, message, title):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information if title == "Success" else QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.exec_()


    def materials_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        self.material_input = QTextEdit()
        self.material_input.setPlaceholderText("Enter material content")
        add_material_btn = QPushButton("Add Material")
        add_material_btn.clicked.connect(self.add_material)

        self.material_list = QVBoxLayout()
        self.refresh_material_list()

        layout.addWidget(self.material_input)
        layout.addWidget(add_material_btn)
        layout.addLayout(self.material_list)

        page.setLayout(layout)
        return page

    def system_status_page(self):
        return self.create_label_page("System running fine. All services OK.")

    def add_admin_page(self):
        return self.create_user_form("Admin")

    def add_professor_page(self):
        return self.create_user_form("Professor")

    def create_label_page(self, title):
        page = QWidget()
        layout = QVBoxLayout()
        label = QLabel(title)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(label)
        page.setLayout(layout)
        return page

    def create_user_form(self, role):
        page = QWidget()

        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(0, 50, 0, 0) 
        outer_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        form_widget = QWidget()
        form_layout = QFormLayout()
        form_widget.setLayout(form_layout)
        form_widget.setFixedWidth(600)

        username_input = QLineEdit()
        username_input.setPlaceholderText("Enter username")
        username_input.setStyleSheet("""
            QLineEdit {
                padding: 14px;
                font-size: 18px;
                border: 2px solid #ccc;
                border-radius: 8px;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: #eef8ff;
            }
        """)

        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.Password)
        password_input.setPlaceholderText("Enter password")
        password_input.setStyleSheet(username_input.styleSheet())

        submit_btn = QPushButton(f"Create {role}")
        submit_btn.setFixedWidth(200)
        submit_btn.setCursor(Qt.PointingHandCursor)
        submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 15px;
                font-size: 18px;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        def submit():
            username = username_input.text()
            password = password_input.text()

            if not username or not password:
                QMessageBox.warning(page, "Error", "Username and password cannot be empty!")
            elif username in users:
                QMessageBox.warning(page, "Error", "User already exists!")
            else:
                users[username] = (password, role)
                QMessageBox.information(page, "Success", f"{role} added successfully!")
                username_input.clear()
                password_input.clear()
                self.update_manage_users_table()

        submit_btn.clicked.connect(submit)

        form_layout.addRow("Username:", username_input)
        form_layout.addRow("Password:", password_input)
        form_layout.addRow("", submit_btn)  
        outer_layout.addWidget(form_widget)
        page.setLayout(outer_layout)

        page.setStyleSheet("""
            QWidget {
                background-color: #f4f6f9;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
            }
        """)

        return page


    def refresh_event_list(self):
        for i in reversed(range(self.event_list.count())):
            widget_to_remove = self.event_list.itemAt(i).widget()
            if widget_to_remove:
                widget_to_remove.setParent(None)

        for event in self.saved_events:
            card = QFrame()
            card.setStyleSheet("""
                QFrame {
                    background-color: #ecf0f1;
                    border: 1px solid #bdc3c7;
                    border-radius: 10px;
                    padding: 10px;
                }
            """)

            # Create a label to display event details (event name, start date, deadline)
            event_details = f"Event: {event['name']}\nStart Date: {event['start_date']}\nDeadline: {event['end_date']}"
            label = QLabel(event_details)
            label.setStyleSheet("font-size: 15px; color: #2c3e50;")

            card_layout = QVBoxLayout(card)
            card_layout.addWidget(label)
            self.event_list.addWidget(card)



    def add_material(self):
        content = self.material_input.toPlainText()
        if content:
            materials.append(content)
            self.material_input.clear()
            self.refresh_material_list()

    def refresh_material_list(self):
        for i in reversed(range(self.material_list.count())):
            self.material_list.itemAt(i).widget().deleteLater()
        for mat in materials:
            lbl = QLabel(mat)
            self.material_list.addWidget(lbl)

    def logout(self):
        self.logout_callback()
        self.close()


