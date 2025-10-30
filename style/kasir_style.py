class KasirStyle:
    def get_stylesheet(self):
        return """
            QMainWindow {
                background-color: #f5f5f5;
            }
            
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 10pt;
            }
            
            QLineEdit#barcodeInput {
                padding: 10px;
                border: 2px solid #ddd;
                border-radius: 6px;
                background-color: white;
                font-size: 11pt;
            }
            
            QLineEdit#barcodeInput:focus {
                border: 2px solid #4CAF50;
            }
            
            QPushButton {
                padding: 10px 20px;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                min-width: 100px;
            }
            
            QPushButton#addButton {
                background-color: #4CAF50;
                color: white;
            }
            
            QPushButton#addButton:hover {
                background-color: #45a049;
            }
            
            QPushButton#addButton:pressed {
                background-color: #3d8b40;
            }
            
            QPushButton#logoutButton {
                background-color: #fff;
                border: 2px solid red;
                color: red;
            }

            QPushButton#logoutButton:hover {
                background-color: rgba(255, 0, 0, 0.1);
            }
            
            QPushButton#payButton_top {
                background-color: #4CAF50;
                color: white;
            }

            QPushButton#payButton_top:hover {
                background-color: #45a049;
            }
            
            QPushButton#deleteButton {
                background-color: #f44336;
                color: white;
            }
            
            QPushButton#deleteButton:hover {
                background-color: #da190b;
            }
            
            QPushButton#refreshButton {
                background-color: #FF9800;
                color: white;
            }
            
            QPushButton#refreshButton:hover {
                background-color: #e68900;
            }
            
            QPushButton#payButton_bottom {
                background-color: #4CAF50;
                color: white;
                padding: 12px 40px;
                font-size: 12pt;
                min-width: 150px;
            }
            
            QPushButton#payButton:hover {
                background-color: #45a049;
            }
            
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
            
            QTableWidget#cartTable {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 6px;
                gridline-color: #e0e0e0;
            }
                        
            QTableWidget#cartTable::item:selected {
                background-color: #4CAF50;
                color: white;
            }
            
            QHeaderView::section {
                background-color: #2c3e50;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
                border-right: 1px solid #34495e;
                border-bottom: 2px solid #34495e;
            }
            
            QTableWidget#cartTable QTableCornerButton::section {
                background-color: #2c3e50;
            }
            
            QLabel#totalLabel {
                font-size: 18pt;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px;
                background-color: white;
                border: 2px solid #4CAF50;
                border-radius: 6px;
                min-width: 250px;
            }
            
            QStatusBar {
                background-color: #2c3e50;
                color: white;
                font-weight: bold;
            }
            
            QMessageBox {
                background-color: white;
            }
            
            QMessageBox QPushButton {
                min-width: 80px;
            }
        """