import os
from datetime import datetime
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QInputDialog

from model.barang_model import BarangModel
from model.transaksi_model import TransaksiModel
from app.custom_dialog import CustomDialog


class KasirController:
    """Controller layer - business logic"""
    
    def __init__(self, view):
        self.view = view
        self.custom_dialog = CustomDialog()
        
        self.barang_model = BarangModel()
        self.transaksi_model = TransaksiModel()
        
        # daftar_barang akan menyimpan dict seperti: {barcode, nama, harga, stok, jumlah}
        self.daftar_barang = []
        
        # Connect signals
        self.view.barcode_input.returnPressed.connect(self.tambah_barang_from_input)
        self.view.add_btn.clicked.connect(self.tambah_barang_from_input)
        self.view.logout_btn.clicked.connect(self.logout)
        self.view.delete_btn.clicked.connect(self.hapus_selected_item)
        self.view.pay_btn_top.clicked.connect(self.bayar)
        self.view.pay_btn_bottom.clicked.connect(self.bayar)
        self.view.table.itemChanged.connect(self.on_item_changed)
        self.view.logout_signal.connect(self.handle_close_event)
        
        # Initial refresh
        self.refresh_view()

    def refresh_view(self):
        """Refresh view"""
        self.view.refresh_table(self.daftar_barang)
        self.update_total_label()

    def tambah_barang_from_input(self):
        barcode = self.view.barcode_input.text().strip()
        if not barcode:
            self.custom_dialog.show_message("Perhatian", "Masukkan barcode terlebih dahulu.", "warning")
            return

        try:
            int(barcode)
        except ValueError:
            self.custom_dialog.show_message("Perhatian", "Barcode harus berupa angka.", "warning")
            self.view.barcode_input.clear()
            self.view.barcode_input.setFocus()
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
                self.view.barcode_input.clear()
                self.view.barcode_input.setFocus()
                return
            self.daftar_barang.append(barang)

        self.view.barcode_input.clear()
        self.view.barcode_input.setFocus()
        self.refresh_view()

    def update_total_label(self):
        total = self.hitung_total()
        self.view.update_total_label(total)

    def hitung_total(self):
        total = 0
        for item in self.daftar_barang:
            total += item['harga'] * item['jumlah']
        return total

    def on_item_changed(self, item):
        # Hanya proses jika kolom jumlah (kolom index 4)
        if item.column() != 4:
            return
        
        # Disconnect signal sementara agar tidak trigger loop
        self.view.table.itemChanged.disconnect(self.on_item_changed)
        
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
            self.refresh_view()
            self.view.table.itemChanged.connect(self.on_item_changed)

    def hapus_selected_item(self):
        idx = self.view.get_selected_index()
        if idx is None:
            self.custom_dialog.show_message("Perhatian", "Pilih baris yang ingin dihapus.", "warning")
            return
        confirm = self.custom_dialog.show_message("Konfirmasi", "Hapus barang terpilih dari keranjang?", "question")
        if confirm == 1:
            del self.daftar_barang[idx]
            self.refresh_view()

    def logout(self):
        if not self.confirm_logout():
            return
        
        self.view._confirmed_logout = True
        self.custom_dialog.show_message("Sukses", "Berhasil keluar!", "info")
        self.view.close()
        self.view.logout_signal.emit()

    def handle_close_event(self):
        """Handle close dari X button"""
        if not self.confirm_logout():
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

    def bayar(self):
        if not self.daftar_barang:
            self.custom_dialog.show_message("Keranjang Kosong", "Tidak ada barang untuk dibayar.", "info")
            return

        total = self.hitung_total()
        self.custom_dialog.payment_dialog(total, self.view)
        ok = self.custom_dialog.exec_() == QtWidgets.QDialog.Accepted
        uang = self.custom_dialog.get_value() if ok else 0
        if not ok:
            return

        # Update stok via model
        try:
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
        self.refresh_view()

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
            f.write(f"Tanggal: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} | {self.view.cashier_name}\n")
            f.write("-" * 40 + "\n")

            for item in self.daftar_barang:
                subtotal = item["harga"] * item["jumlah"]
                # truncate name to width 20 for neatness
                f.write(f"{item['nama'][:20]:20} x{item['jumlah']:2}  Rp{int(subtotal):>10,}\n")

            f.write("-" * 40 + "\n")
            f.write(f"Total:{int(total_harga):>33,} Rp\n")
            f.write(f"Uang Dibayar:{int(uang_dibayar):>28,} Rp\n")
            f.write(f"Kembalian:{int(kembalian):>31,} Rp\n")
            f.write("=" * 40 + "\n")
            f.write("Terima kasih telah berbelanja!".center(40, " ") + "\n")
            f.write("=" * 40 + "\n")
