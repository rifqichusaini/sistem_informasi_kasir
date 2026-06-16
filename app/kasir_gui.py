import os
from datetime import datetime
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QMainWindow, QMessageBox,
    QTableWidgetItem, QInputDialog
)

from model.barang_model import BarangModel
from model.transaksi_model import TransaksiModel
from app.custom_dialog import CustomDialog
from style.kasir_style import KasirStyle


class KasirWindow(QMainWindow):
    logout_signal = pyqtSignal()

    def __init__(self, cashier_name: str):
        super().__init__()
        self.setWindowTitle("Aplikasi Kasir")
        self.setMinimumSize(900, 600)
        # self.showMaximized()

        # custom dialog
        self.custom_dialog = CustomDialog()

        # kasir style
        self.kasir_style = KasirStyle()

        self.cashier_name = cashier_name
        self.barang_model = BarangModel()
        self.transaksi_model = TransaksiModel()

        # daftar_barang akan menyimpan dict seperti: {barcode, nama, harga, stok, jumlah}
        self.daftar_barang = []
        
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
        self.barcode_input.setPlaceholderText("Masukkan / scan barcode")
        self.barcode_input.setObjectName("barcodeInput")
        self.barcode_input.returnPressed.connect(self.tambah_barang_from_input)
        
        self.add_btn = QtWidgets.QPushButton("Tambah Barang")
        self.add_btn.setObjectName("addButton")
        self.add_btn.clicked.connect(self.tambah_barang_from_input)
        
        self.logout_btn = QtWidgets.QPushButton("Logout")
        self.logout_btn.setObjectName("logoutButton")
        self.logout_btn.clicked.connect(self.logout)
        
        self.delete_btn = QtWidgets.QPushButton("Hapus Barang")
        self.delete_btn.setObjectName("deleteButton")
        self.delete_btn.clicked.connect(self.hapus_selected_item)
        
        self.pay_btn = QtWidgets.QPushButton("Bayar")
        self.pay_btn.setObjectName("payButton_top")
        self.pay_btn.clicked.connect(self.bayar)

        controls_layout.addWidget(self.barcode_input, 2)
        controls_layout.addWidget(self.add_btn)
        controls_layout.addWidget(self.delete_btn)
        controls_layout.addWidget(self.pay_btn)
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
        self.table.itemChanged.connect(self.on_item_changed)
        main_layout.addWidget(self.table)

        # Bottom: totals and pembayaran
        bottom_layout = QtWidgets.QHBoxLayout()
        bottom_layout.setSpacing(10)
        
        self.total_label = QtWidgets.QLabel("Total: Rp 0")
        self.total_label.setObjectName("totalLabel")
        bottom_layout.addWidget(self.total_label)
        bottom_layout.addStretch()

        self.pay_btn = QtWidgets.QPushButton("Bayar")
        self.pay_btn.setObjectName("payButton_bottom")
        self.pay_btn.clicked.connect(self.bayar)
        bottom_layout.addWidget(self.pay_btn)

        main_layout.addLayout(bottom_layout)

        status_bar = self.statusBar()
        status_bar.showMessage(f"Login: {self.cashier_name}")

        # Initial refresh
        self.refresh_table()

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

    def tambah_barang_from_input(self):
        barcode = self.barcode_input.text().strip()
        if not barcode:
            self.custom_dialog.show_message("Perhatian", "Masukkan barcode terlebih dahulu.", "warning")
            return

        try:
            int(barcode)
        except ValueError:
            self.custom_dialog.show_message("Perhatian", "Barcode harus berupa angka.", "warning")
            self.barcode_input.clear()
            self.barcode_input.setFocus()
            return

        # Check if already in cart - convert both to string for comparison
        found = next((b for b in self.daftar_barang if str(b['barcode']) == str(barcode)), None)
        if found:
            # increment jumlah but check stok
            if found['jumlah'] + 1 > found['stok']:
                self.custom_dialog.show_message("Stok Habis", f"Stok hanya {found['stok']}.", "warning")
                return
            found['jumlah'] += 1
        else:
            barang = self.barang_model.get_barang(barcode)
            if not barang:
                self.custom_dialog.show_message("Tidak Ditemukan", "Barang tidak terdaftar.", "warning")
                self.barcode_input.clear()
                self.barcode_input.setFocus()
                return
            self.daftar_barang.append(barang)

        self.barcode_input.clear()
        self.barcode_input.setFocus()
        self.refresh_table()

    def refresh_table(self):
        self.table.setRowCount(0)
        for idx, item in enumerate(self.daftar_barang):
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

        self.update_total_label()

    def logout(self):
        if not self.confirm_logout():
            return
        
        self._confirmed_logout = True
        self.custom_dialog.show_message("Sukses", "Berhasil keluar!", "info")
        self.close()
        self.logout_signal.emit()
        return

    def confirm_logout(self):
        """Check transaksi belum selesai dan minta konfirmasi"""
        if len(self.daftar_barang) > 0:
            konf = self.custom_dialog.show_message(
                "Konfirmasi", 
                "Ada transaksi yang belum terselesaikan\nApakah anda yakin ingin keluar?", 
                "question"
            )
            return konf
        else:
            konf = self.custom_dialog.show_message(
                "Konfirmasi", 
                "Apakah anda yakin ingin keluar?", 
                "question"
            )
            return konf

    def closeEvent(self, event):
        """Handle ketika user klik X button"""
        # Jika sudah dikonfirmasi via logout button, langsung tutup
        if self._confirmed_logout:
            event.accept()
            return
        
        # Jika user klik X button, minta konfirmasi
        if not self.confirm_logout():
            event.ignore()
            return
        
        # Jika konfirmasi dari X button (bukan dari logout button), langsung tutup tanpa emit signal
        event.accept()

    def on_item_changed(self, item):
        # Hanya proses jika kolom jumlah (kolom index 4)
        if item.column() != 4:
            return
        
        # Disconnect signal sementara agar tidak trigger loop
        self.table.itemChanged.disconnect(self.on_item_changed)
        
        row = item.row()
        try:
            jumlah_baru = int(item.text().strip())
            if jumlah_baru < 0:
                self.custom_dialog.show_message("Input Invalid", "Masukkan angka yang valid.", "warning")
                return
            elif jumlah_baru == 0:
                self.hapus_selected_item()
                return
            
            barang = self.daftar_barang[row]
            if jumlah_baru > barang['stok']:
                self.custom_dialog.show_message("Stok Kurang", f"Stok barang hanya {barang['stok']}.", "warning")
                item.setText("    " + str(barang['jumlah']))  # Kembalikan ke nilai lama
            else:
                barang['jumlah'] = jumlah_baru
                self.update_total_label()
        except (ValueError, IndexError):
            self.custom_dialog.show_message("Input Invalid", "Masukkan angka yang valid.", "warning")
            if row < len(self.daftar_barang):
                item.setText("    " + str(self.daftar_barang[row]['jumlah']))
        finally:
            self.refresh_table()
            self.table.itemChanged.connect(self.on_item_changed)

    def update_total_label(self):
        total = self.hitung_total()
        self.total_label.setText(f"Total: Rp {total:,}")

    def hitung_total(self):
        total = 0
        for item in self.daftar_barang:
            total += item['harga'] * item['jumlah']
        return total

    def get_selected_index(self):
        selection = self.table.selectionModel().selectedRows()
        if not selection:
            return None
        return selection[0].row()

    def edit_selected_item(self):
        idx = self.get_selected_index()
        if idx is None:
            self.custom_dialog.show_message("Perhatian", "Pilih baris yang ingin diedit.", "warning")
            return
        item = self.daftar_barang[idx]
        jumlah, ok = QInputDialog.getInt(self, "Edit Jumlah", f"Masukkan jumlah baru (stok {item['stok']})", value=item['jumlah'], min=1)
        if not ok:
            return
        if jumlah > item['stok']:
            self.custom_dialog.show_message("Stok Kurang", f"Stok barang hanya {item['stok']}.", "warning")
            return
        item['jumlah'] = jumlah
        self.refresh_table()

    def hapus_selected_item(self):
        idx = self.get_selected_index()
        if idx is None:
            self.custom_dialog.show_message("Perhatian", "Pilih baris yang ingin dihapus.", "warning")
            return
        confirm = self.custom_dialog.show_message("Konfirmasi", "Hapus barang terpilih dari keranjang?", "question")
        if confirm == 1:
            del self.daftar_barang[idx]
            self.refresh_table()

    def bayar(self):
        if not self.daftar_barang:
            self.custom_dialog.show_message("Keranjang Kosong", "Tidak ada barang untuk dibayar.", "info")
            return

        total = self.hitung_total()
        # uang, ok = QInputDialog.getInt(self, "Pembayaran", f"Total: Rp {total:,}\nMasukkan jumlah uang dibayar:", min=0)
        self.custom_dialog.payment_dialog(total, self)
        ok = self.custom_dialog.exec_() == QtWidgets.QDialog.Accepted
        uang = self.custom_dialog.get_value() if ok else 0
        if not ok:
            return

        # Update stok via model
        try:
            # Convert items to expected format (they already match)
            self.barang_model.update_barang(daftar_barang=self.daftar_barang)
        except Exception as e:
            self.custom_dialog.show_message("Error", f"Gagal update stok: {e}", "critical")
            return

        # Simpan transaksi
        try:
            self.transaksi_model.simpan_transaksi(
                daftar_barang=self.daftar_barang,
                total_harga=total,
                uang_dibayar=uang
            )
        except Exception as e:
            self.custom_dialog.show_message("Error", f"Gagal menyimpan transaksi: {e}", "critical")
            return

        kembalian = uang - total
        self.custom_dialog.show_message("Sukses", f"Pembayaran berhasil.\nKembalian: Rp {kembalian:,}", "info")

        # Tanyakan cetak struk
        reply = self.custom_dialog.show_message("Cetak Struk", "Cetak struk transaksi?", "question")
        if reply == 1:
            try:
                self.cetak_struk(total, uang)
                self.custom_dialog.show_message("Struk", "Struk berhasil dibuat di folder data", "info")
            except Exception as e:
                self.custom_dialog.show_message("Error", f"Gagal membuat struk: {e}", "critical")

        # Kosongkan keranjang setelah transaksi
        self.daftar_barang = []
        self.refresh_table()

    def cetak_struk(self, total_harga, uang_dibayar):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        struk_dir = os.path.join(base_dir, "../data")
        os.makedirs(struk_dir, exist_ok=True)

        waktu = datetime.now().strftime("%Y%m%d-%H%M%S")
        nama_file = f"struk-{waktu}.txt"
        file_path = os.path.join(struk_dir, nama_file)

        kembalian = uang_dibayar - total_harga

        with open(file_path, "w", encoding="utf-8") as f:
            f.write("=" * 40 + "\n")
            f.write("STRUK PEMBAYARAN KASIR".center(40, " ") + "\n")
            f.write("=" * 40 + "\n")
            f.write(f"Tanggal: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} | {self.cashier_name}\n")
            f.write("-" * 40 + "\n")

            for item in self.daftar_barang:
                subtotal = item["harga"] * item["jumlah"]
                # truncate name to width 20 for neatness
                f.write(f"{item['nama'][:20]:20} x{item['jumlah']:2}  Rp{subtotal:10,}\n")

            f.write("-" * 40 + "\n")
            f.write(f"Total: {'Rp ' + format(total_harga, ','):>27}\n")
            f.write(f"Uang Dibayar: {'Rp ' + format(uang_dibayar, ','):>20}\n")
            f.write(f"Kembalian: {'Rp ' + format(kembalian, ','):>23}\n")
            f.write("=" * 40 + "\n")
            f.write("Terima kasih telah berbelanja!".center(40, " ") + "\n")
            f.write("=" * 40 + "\n")