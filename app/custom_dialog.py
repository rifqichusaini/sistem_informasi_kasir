from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox

class CustomDialog(QtWidgets.QDialog):
    # def __init__(self):
        
    def payment_dialog(self, total, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Pembayaran")
        self.setModal(True)
        self.setFixedSize(460, 430)
        self.total = total
        
        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(12)
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

        self.change_label = QtWidgets.QLabel("Kembalian: Rp 0")
        self.change_label.setAlignment(QtCore.Qt.AlignCenter)
        self.change_label.setFixedHeight(44)
        self.change_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                background-color: #f8f9fa;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
            }
        """)
        layout.addWidget(self.change_label)
        
        # Input field
        label = QtWidgets.QLabel("Jumlah Uang Dibayar:")
        label.setContentsMargins(0, 4, 0, 0)
        label.setStyleSheet("font-weight: bold; font-size: 11pt;")
        layout.addWidget(label)
        
        self.input_field = QtWidgets.QLineEdit()
        validator = QtGui.QRegExpValidator(QtCore.QRegExp("[0-9,]*"))
        self.input_field.setValidator(validator)
        self.input_field.setPlaceholderText("Masukkan jumlah uang...")
        self.input_field.setFixedHeight(40)
        self.input_field.setStyleSheet("""
            QLineEdit {
                border: 2px solid #ddd;
                border-radius: 6px;
                font-size: 12pt;
                background-color: white;
                padding-left: 10px;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
        """)
        self.input_field.textChanged.connect(self.format_currency_input)
        layout.addWidget(self.input_field)

        quick_money_layout = QtWidgets.QGridLayout()
        quick_money_layout.setHorizontalSpacing(8)
        quick_money_layout.setVerticalSpacing(8)
        self.quick_money_buttons = []
        quick_money_options = [
            ("5rb", 5000),
            ("10rb", 10000),
            ("20rb", 20000),
            ("50rb", 50000),
            ("100rb", 100000),
        ]

        for label_text, amount in quick_money_options:
            quick_btn = QtWidgets.QPushButton(label_text)
            quick_btn.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            quick_btn.setMinimumHeight(36)
            quick_btn.setCursor(QtCore.Qt.PointingHandCursor)
            quick_btn.setStyleSheet("""
                QPushButton {
                    background-color: #eef7ef;
                    color: #2e7d32;
                    border: 1px solid #4CAF50;
                    border-radius: 6px;
                    padding: 8px 14px;
                    font-weight: bold;
                    font-size: 10pt;
                }
                QPushButton:hover {
                    background-color: #dff1e1;
                }
                QPushButton:pressed {
                    background-color: #cfe8d2;
                }
            """)
            quick_btn.adjustSize()
            quick_btn.clicked.connect(lambda _, value=amount: self.add_quick_money(value))
            button_index = len(self.quick_money_buttons)
            quick_money_layout.addWidget(
                quick_btn,
                button_index // 3,
                button_index % 3,
                alignment=QtCore.Qt.AlignCenter
            )
            self.quick_money_buttons.append(quick_btn)

        reset_btn = QtWidgets.QPushButton("Reset")
        reset_btn.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        reset_btn.setMinimumHeight(36)
        reset_btn.setCursor(QtCore.Qt.PointingHandCursor)
        reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #fff4e5;
                color: #b26a00;
                border: 1px solid #f0ad4e;
                border-radius: 6px;
                padding: 8px 14px;
                font-weight: bold;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #ffe8c2;
            }
            QPushButton:pressed {
                background-color: #ffd99a;
            }
        """)
        reset_btn.adjustSize()
        reset_btn.clicked.connect(self.reset_payment_input)
        quick_money_layout.addWidget(reset_btn, 1, 2, alignment=QtCore.Qt.AlignCenter)
        self.reset_money_btn = reset_btn

        layout.addLayout(quick_money_layout)

        self.payment_status_label = QtWidgets.QLabel("")
        self.payment_status_label.setFixedHeight(22)
        self.payment_status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.payment_status_label.setStyleSheet("""
            QLabel {
                color: #f44336;
                font-size: 10pt;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.payment_status_label)
        
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
        
        self.ok_btn = QtWidgets.QPushButton("Bayar")
        self.ok_btn.setEnabled(False)
        self.ok_btn.setStyleSheet("""
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
            QPushButton:disabled {
                background-color: #c8c8c8;
                color: #777;
            }
        """)
        self.ok_btn.clicked.connect(self.validate_and_accept)
        self.ok_btn.setDefault(True)
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(self.ok_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Style dialog
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
        """)
        self.update_payment_state()
    
    def format_currency_input(self):
        """Format input dengan koma setiap 3 digit"""
        self.input_field.textChanged.disconnect(self.format_currency_input)
        text = self.input_field.text().replace(",", "")

        if text:
            try:
                formatted = f"{int(text):,}"
                self.input_field.setText(formatted)
                self.input_field.setCursorPosition(len(formatted))
            except ValueError:
                self.input_field.clear()
        else:
            self.input_field.clear()

        self.input_field.textChanged.connect(self.format_currency_input)
        self.update_payment_state()

    def add_quick_money(self, amount):
        current_value = self.get_value()
        self.input_field.setText(f"{current_value + amount:,}")
        self.input_field.setCursorPosition(len(self.input_field.text()))
        self.input_field.setFocus()

    def reset_payment_input(self):
        self.input_field.clear()
        self.input_field.setFocus()

    def update_payment_state(self):
        uang = self.get_value()
        kembalian = max(uang - self.total, 0)
        self.change_label.setText(f"Kembalian: Rp {kembalian:,}")

        if uang <= 0:
            self.payment_status_label.clear()
            self.ok_btn.setEnabled(False)
            return

        if uang < self.total:
            kurang = self.total - uang
            self.payment_status_label.setText(f"Uang tidak cukup. Kurang Rp {kurang:,}")
            self.ok_btn.setEnabled(False)
            return

        self.payment_status_label.clear()
        self.ok_btn.setEnabled(True)
    
    def get_value(self):
        try:
            # Remove koma sebelum convert ke int
            return int(self.input_field.text().replace(",", ""))
        except ValueError:
            return 0
    
    def validate_and_accept(self):
        try:
            # Remove koma sebelum convert
            uang = int(self.input_field.text().replace(",", "").strip())
            if uang < self.total:
                self.update_payment_state()
                self.input_field.setFocus()
                return
            self.accept()
        except ValueError:
            self.show_message("Input Invalid", "Masukkan jumlah uang yang valid!", "warning")
            self.input_field.clear()
            self.input_field.setFocus()
        
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
    
