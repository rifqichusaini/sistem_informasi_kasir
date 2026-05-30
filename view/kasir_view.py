import os
from datetime import datetime
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QMainWindow, QMessageBox,
    QTableWidgetItem, QInputDialog
)

from app.custom_dialog import CustomDialog
from style.kasir_style import KasirStyle


class KasirView(QMainWindow):
    """View layer - hanya untuk UI"""
    logout_signal = pyqtSignal()

    def __init__(self, cashier_name: str):
        super().__init__()
        self.setWindowTitle("Aplikasi Kasir")
        self.setMinimumSize(900, 600)

        # custom dialog
        self.custom_dialog = CustomDialog()

        # kasir style
        self.kasir_style = KasirStyle()

        self.cashier_name = cashier_name
        
        # Flag untuk track apakah sudah dikonfirmasi logout
        self._confirmed_logout = False

        # Apply stylesheet
        self.setStyleSheet(self.kasir_style.get_stylesheet())

        # --- UI elements ---
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        central.setLayout(main_layout)

        # Top: controls (barcode input & actions)
        controls_layout = QtWidgets.QHBoxLayout()
        controls_layout.setSpacing(10)
        
        self.barcode_input = QtWidgets.QLineEdit()
        self.barcode_input.setPlaceholderText("Masukkan / scan barcode lalu tekan Tambah")
        self.barcode_input.setObjectName("barcodeInput")
        
        self.add_btn = QtWidgets.QPushButton("Tambah Barang")
        self.add_btn.setObjectName("addButton")
        
        self.logout_btn = QtWidgets.QPushButton("Logout")
        self.logout_btn.setObjectName("logoutButton")
        
        self.delete_btn = QtWidgets.QPushButton("Hapus Barang")
        self.delete_btn.setObjectName("deleteButton")
        
        self.pay_btn_top = QtWidgets.QPushButton("Bayar")
        self.pay_btn_top.setObjectName("payButton_top")

        controls_layout.addWidget(self.barcode_input, 2)
        controls_layout.addWidget(self.add_btn)
        controls_layout.addWidget(self.delete_btn)
        controls_layout.addWidget(self.pay_btn_top)
        controls_layout.addWidget(self.logout_btn)

        main_layout.addLayout(controls_layout)

        # Middle: table keranjang
        self.table = QtWidgets.QTableWidget(0, 6)
        self.table.setObjectName("cartTable")
        self.table.setHorizontalHeaderLabels(["No.", "Barcode", "Nama", "Harga", "Jumlah", "Stok"])
        self.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff) 
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        main_layout.addWidget(self.table)

        # Bottom: totals and pembayaran
        bottom_layout = QtWidgets.QHBoxLayout()
        bottom_layout.setSpacing(10)
        
        self.total_label = QtWidgets.QLabel("Total: Rp 0")
        self.total_label.setObjectName("totalLabel")
        bottom_layout.addWidget(self.total_label)
        bottom_layout.addStretch()

        self.pay_btn_bottom = QtWidgets.QPushButton("Bayar")
        self.pay_btn_bottom.setObjectName("payButton_bottom")
        bottom_layout.addWidget(self.pay_btn_bottom)

        main_layout.addLayout(bottom_layout)

        status_bar = self.statusBar()
        status_bar.showMessage(f"Login: {self.cashier_name}")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resize_columns()
    
    def resize_columns(self):
        table_width = self.table.viewport().width()
        self.table.setColumnWidth(0, int(table_width * 0.05))   # 5% - No (lebih kecil)
        self.table.setColumnWidth(1, int(table_width * 0.20))   # 12% - Barcode
        self.table.setColumnWidth(2, int(table_width * 0.35))   # 50% - Nama (lebih besar)
        self.table.setColumnWidth(3, int(table_width * 0.15))   # 15% - Harga
        self.table.setColumnWidth(4, int(table_width * 0.13))   # 18% - Jumlah
        self.table.setColumnWidth(5, int(table_width * 0.07))   # 18% - Jumlah

    def refresh_table(self, daftar_barang):
        """Refresh table display"""
        self.table.setRowCount(0)
        for idx, item in enumerate(daftar_barang):
            self.table.insertRow(idx)

            item_no = QTableWidgetItem("    " + str(idx + 1))
            item_no.setFlags(item_no.flags() & ~QtCore.Qt.ItemIsEditable)
            self.table.setItem(idx, 0, item_no)
            
            item_barcode = QTableWidgetItem("    " + str(item['barcode']))
            item_barcode.setFlags(item_barcode.flags() & ~QtCore.Qt.ItemIsEditable)
            self.table.setItem(idx, 1, item_barcode)
            
            item_nama = QTableWidgetItem("    " + item['nama'])
            item_nama.setFlags(item_nama.flags() & ~QtCore.Qt.ItemIsEditable)
            self.table.setItem(idx, 2, item_nama)
            
            item_harga = QTableWidgetItem(f"    Rp {item['harga']:,}")
            item_harga.setFlags(item_harga.flags() & ~QtCore.Qt.ItemIsEditable)
            self.table.setItem(idx, 3, item_harga)

            self.table.setItem(idx, 4, QTableWidgetItem("    " + str(item['jumlah'])))
            self.table.setRowHeight(idx, 45)

            item_stok = QTableWidgetItem(f"    {item['stok']}")
            item_stok.setFlags(item_stok.flags() & ~QtCore.Qt.ItemIsEditable)
            self.table.setItem(idx, 5, item_stok)

    def update_total_label(self, total):
        """Update total label"""
        self.total_label.setText(f"Total: Rp {total:,}")

    def get_selected_index(self):
        """Get selected row index"""
        selection = self.table.selectionModel().selectedRows()
        if not selection:
            return None
        return selection[0].row()

    def closeEvent(self, event):
        """Handle ketika user klik X button"""
        # Jika sudah dikonfirmasi via logout button, langsung tutup
        if self._confirmed_logout:
            event.accept()
            return
        
        # Jika user klik X button, emit signal untuk controller handle
        self.logout_signal.emit()
        event.accept()
