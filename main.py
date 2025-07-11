import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QStackedWidget, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from admin import AdminDashboard
from student import StudentDashboard
from professor import ProfessorDashboard
from data import users

class RegisterPage(QWidget):
    def __init__(self, switch_to_login):
        super().__init__()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("background-color: #f0f2f5;")

        # Card-style container
        container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.setSpacing(25)
        container_layout.setContentsMargins(40, 40, 40, 40)

        container.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 16px;
                border: 1px solid #dcdde1;
            }
        """)

        title = QLabel("Student Registration")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #2c3e50;")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(title)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.style_input(self.username_input)
        container_layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.style_input(self.password_input)
        container_layout.addWidget(self.password_input)

        register_button = QPushButton("Register (Student Only)")
        register_button.clicked.connect(self.register)
        self.style_button(register_button, "#27ae60", "#1e8449")
        container_layout.addWidget(register_button)

        login_button = QPushButton("Back to Login")
        login_button.clicked.connect(switch_to_login)
        self.style_button(login_button, "#95a5a6", "#7f8c8d")
        container_layout.addWidget(login_button)

        container.setLayout(container_layout)
        container.setFixedWidth(450)
        layout.addWidget(container)

        self.setLayout(layout)

    def style_input(self, input_box):
        input_box.setStyleSheet("""
            QLineEdit {
                padding: 14px;
                font-size: 17px;
                border: 1px solid #ccc;
                border-radius: 10px;
            }
            QLineEdit:focus {
                border: 1px solid #27ae60;
            }
        """)

    def style_button(self, btn, bg_color, hover_color):
        btn.setStyleSheet(f"""
            QPushButton {{
                padding: 12px;
                font-size: 16px;
                background-color: {bg_color};
                color: white;
                border: none;
                border-radius: 10px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """)

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username in users:
            QMessageBox.warning(self, "Error", "User already exists!")
        else:
            users[username] = (password, "Student")
            QMessageBox.information(self, "Success", "Student registered successfully!")
            self.username_input.clear()
            self.password_input.clear()


class LoginPage(QWidget):
    def __init__(self, switch_to_register, switch_to_dashboard):
        super().__init__()
        self.switch_to_register = switch_to_register
        self.switch_to_dashboard = switch_to_dashboard

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("background-color: #f0f2f5;")

        # Container as a Card
        container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.setSpacing(25)
        container_layout.setContentsMargins(40, 40, 40, 40)

        container.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 16px;
                border: 1px solid #dcdde1;
            }
        """)

        title = QLabel("Login")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #2c3e50;")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(title)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.style_input(self.username_input)
        container_layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.style_input(self.password_input)
        container_layout.addWidget(self.password_input)

        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login)
        self.style_button(login_button, "#3498db", "#2980b9")
        container_layout.addWidget(login_button)

        register_button = QPushButton("Register as Student")
        register_button.clicked.connect(switch_to_register)
        self.style_button(register_button, "#95a5a6", "#7f8c8d")
        container_layout.addWidget(register_button)

        container.setLayout(container_layout)
        container.setFixedWidth(450)
        layout.addWidget(container)

        self.setLayout(layout)

    def style_input(self, input_box):
        input_box.setStyleSheet("""
            QLineEdit {
                padding: 14px;
                font-size: 17px;
                border: 1px solid #ccc;
                border-radius: 10px;
            }
            QLineEdit:focus {
                border: 1px solid #3498db;
            }
        """)

    def style_button(self, btn, bg_color, hover_color):
        btn.setStyleSheet(f"""
            QPushButton {{
                padding: 12px;
                font-size: 16px;
                background-color: {bg_color};
                color: white;
                border: none;
                border-radius: 10px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username in users and users[username][0] == password:
            role = users[username][1]
            QMessageBox.information(self, "Login Success", f"Welcome, {username}!\nRole: {role}")
            self.username_input.clear()
            self.password_input.clear()
            self.switch_to_dashboard(role)
        else:
            QMessageBox.warning(self, "Error", "Invalid credentials!")


class MainWindow(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.login_page = LoginPage(self.show_register_page, self.show_dashboard_page)
        self.register_page = RegisterPage(self.show_login_page)

        self.addWidget(self.login_page)       
        self.addWidget(self.register_page)     
        self.setCurrentIndex(0)

    def show_register_page(self):
        self.setCurrentIndex(1)

    def show_login_page(self):
        self.setCurrentIndex(0)

    def show_dashboard_page(self, role):
        if role == "Admin":
            if not hasattr(self, 'admin_dashboard'):
                self.admin_dashboard = AdminDashboard(self.back_to_login)
                self.addWidget(self.admin_dashboard)
            self.setCurrentWidget(self.admin_dashboard)

        elif role == "Student":
            if not hasattr(self, 'stud_dashboard'):
                self.stud_dashboard = StudentDashboard(self.back_to_login)
                self.addWidget(self.stud_dashboard)
            self.setCurrentWidget(self.stud_dashboard)

        elif role == "Professor":
            if not hasattr(self, 'prof_dashboard'):
                self.prof_dashboard = ProfessorDashboard(self.back_to_login)
                self.addWidget(self.prof_dashboard)
            self.setCurrentWidget(self.prof_dashboard)

    def back_to_login(self):
        self.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Login / Register")
    window.resize(600, 400)
    window.show()
    sys.exit(app.exec_())
