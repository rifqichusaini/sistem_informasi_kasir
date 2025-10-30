from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (
    QDialog, QMessageBox
)

from api.login_api import LoginAPI

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login - Sistem Kasir")
        self.setFixedSize(400, 350)

        self.api_login = LoginAPI()

        # Apply consistent stylesheet
        self.setStyleSheet(self.get_stylesheet())

        # Header with icon/title
        self.login_label = QtWidgets.QLabel("SISTEM KASIR", self)
        self.login_label.setAlignment(QtCore.Qt.AlignCenter)
        self.login_label.setObjectName("headerLabel")

        self.subtitle_label = QtWidgets.QLabel("Silakan masuk untuk melanjutkan", self)
        self.subtitle_label.setAlignment(QtCore.Qt.AlignCenter)
        self.subtitle_label.setObjectName("subtitleLabel")

        # Username input
        self.username_input = QtWidgets.QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        self.username_input.setObjectName("loginInput")
        self.username_input.returnPressed.connect(lambda: self.password_input.setFocus())

        # Password input
        self.password_input = QtWidgets.QLineEdit(self)
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setObjectName("loginInput")
        self.password_input.returnPressed.connect(self.attempt_login)

        # Login button
        self.login_btn = QtWidgets.QPushButton("Login", self)
        self.login_btn.setObjectName("loginButton")
        self.login_btn.clicked.connect(self.attempt_login)
        self.login_btn.setAutoDefault(False)
        self.login_btn.setCursor(QtCore.Qt.PointingHandCursor)

        # Layout
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(15)
        
        layout.addWidget(self.login_label)
        layout.addWidget(self.subtitle_label)
        layout.addSpacing(10)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addSpacing(10)
        layout.addWidget(self.login_btn)
        layout.addStretch()
        
        self.setLayout(layout)

        self.logged_in_name = None

        # Focus pada username saat dialog dibuka
        self.username_input.setFocus()

    def get_stylesheet(self):
        return """
            QDialog {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #e3f2fd,
                    stop:1 #bbdefb
                );
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            QLabel#headerLabel {
                font-size: 20pt;
                font-weight: bold;
                color: #1976d2;
                padding: 10px;
            }
            
            QLabel#subtitleLabel {
                font-size: 10pt;
                color: #555;
                padding-bottom: 5px;
            }
            
            QLineEdit#loginInput {
                padding: 12px 15px;
                border: 2px solid #ddd;
                border-radius: 8px;
                background-color: white;
                font-size: 11pt;
                min-height: 20px;
            }
            
            QLineEdit#loginInput:focus {
                border: 2px solid #4CAF50;
                background-color: #fafafa;
            }
            
            QLineEdit#loginInput:hover {
                border: 2px solid #bbb;
            }
            
            QPushButton#loginButton {
                padding: 12px;
                border: none;
                border-radius: 8px;
                background-color: #4CAF50;
                color: white;
                font-size: 12pt;
                font-weight: bold;
                min-height: 25px;
            }
            
            QPushButton#loginButton:hover {
                background-color: #45a049;
            }
            
            QPushButton#loginButton:pressed {
                background-color: #3d8b40;
            }
            
            QMessageBox {
                background-color: white;
            }
            
            QMessageBox QPushButton {
                padding: 8px 20px;
                border: none;
                border-radius: 6px;
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                min-width: 80px;
            }
            
            QMessageBox QPushButton:hover {
                background-color: #45a049;
            }
        """

    def attempt_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Perhatian", "Isi username dan password terlebih dahulu.")
            return

        name = self.api_login.validate_user(user=username, passw=password)
        if name:
            QMessageBox.information(self, "Sukses", f"Login berhasil sebagai {name}!")
            self.logged_in_name = name
            self.accept()
        else:
            QMessageBox.warning(self, "Gagal", "Username atau password salah.")
            self.password_input.clear()
            self.password_input.setFocus()