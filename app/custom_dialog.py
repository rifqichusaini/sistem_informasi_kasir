from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox

class CustomDialog(QtWidgets.QDialog):
    # def __init__(self):
        
    def payment_dialog(self, total, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Pembayaran")
        self.setModal(True)
        self.setFixedSize(400, 250)
        
        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Total label
        total_label = QtWidgets.QLabel(f"Total Pembayaran: Rp {total:,}")
        total_label.setAlignment(QtCore.Qt.AlignCenter)
        total_label.setFixedHeight(50)
        total_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #2c3e50;
                background-color: #f0f0f0;
                border-radius: 8px;
            }
        """)
        layout.addWidget(total_label)
        
        # Input field
        label = QtWidgets.QLabel("Jumlah Uang Dibayar:")
        label.setContentsMargins(0, 10, 0, 0)
        label.setStyleSheet("font-weight: bold; font-size: 11pt;")
        layout.addWidget(label)
        
        self.input_field = QtWidgets.QLineEdit()
        validator = QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]+"))
        self.input_field.setValidator(validator)
        self.input_field.setPlaceholderText("Masukkan jumlah uang...")
        self.input_field.setFixedHeight(40)
        self.input_field.setStyleSheet("""
            QLineEdit {
                border: 2px solid #ddd;
                border-radius: 6px;
                font-size: 12pt;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
        """)
        layout.addWidget(self.input_field)
        
        # Buttons
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(10)
        
        cancel_btn = QtWidgets.QPushButton("Batal")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 5px 20px;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 11pt;
                min-width: 100px;
                min-height: 25px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        ok_btn = QtWidgets.QPushButton("Bayar")
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 5px 20px;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 11pt;
                min-width: 100px;
                min-height: 25px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        ok_btn.clicked.connect(self.accept)
        ok_btn.setDefault(True)
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(ok_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Style dialog
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
        """)
    
    def get_value(self):
        try:
            return int(self.input_field.text())
        except ValueError:
            return 0
        
    def show_message(self, title, text, msg_type):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(text)
        
        # Set icon sesuai tipe
        if msg_type == "info":
            msg.setIcon(QMessageBox.Information)
        elif msg_type == "warning":
            msg.setIcon(QMessageBox.Warning)
        elif msg_type == "error":
            msg.setIcon(QMessageBox.Critical)
        elif msg_type == "question":
            msg.setIcon(QMessageBox.Question)

        if msg_type == "question":
            yes_btn = msg.addButton("Yes", QMessageBox.YesRole)
            no_btn = msg.addButton("No", QMessageBox.NoRole)
            yes_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    padding: 8px 20px;
                    border-radius: 4px;
                    min-width: 80px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            no_btn.setStyleSheet("""
                QPushButton {
                    background-color: #f44336;
                    color: white;
                    padding: 8px 20px;
                    border-radius: 4px;
                    min-width: 80px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #da190b;
                }
            """)
            result = msg.exec_()
            return result == 0  # YesRole returns 0
        else:
            ok_btn = msg.addButton("OK", QMessageBox.AcceptRole)
            ok_btn.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    padding: 8px 20px;
                    border-radius: 4px;
                    min-width: 80px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #0b7dda;
                }
            """)
            msg.exec_()
            return True
    