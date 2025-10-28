import os
from datetime import datetime
from style import StyleText
from api.barang_api import BarangAPI
from api.transaksi_api import TransaksiAPI

class Kasir:
  def __init__(self, name):
    self.style = StyleText()
    self.api_barang = BarangAPI()
    self.api_transaksi = TransaksiAPI() 
    self.name = name
    self.daftar_barang = []

  def menu(self):
    while True:
      print("="*20)
      print("Menu".center(20, " "))
      print("="*20)
      print(" 1. Tambah Barang")
      print(" 2. Edit Barang")
      print(" 3. Hapus Barang")
      print(" 4. Lihat Keranjang")
      print(" 5. Bayar")
      print(" 0. Logout")
      print("="*20)

      pilihan = input("Pilih menu: ")

      if pilihan == "1":
        self.tambah_barang()

      elif pilihan == "2":
        os.system('cls')
        self.edit_barang()
        os.system('pause')
        os.system('cls')

      elif pilihan == "3":
        os.system('cls')
        self.hapus_barang()
        os.system('pause')
        os.system('cls')

      elif pilihan == "4":
        os.system('cls')
        self.tampilkan_barang()
        os.system('pause')
        os.system('cls')

      elif pilihan == "5":
        os.system('cls')
        self.bayar()
        os.system('pause')
        os.system('cls')

      elif pilihan == "0":
        print("Terima kasih telah menggunakan sistem kasir.")
        return

      else:
        print(self.style.warning("Pilihan tidak valid."))
        os.system('pause')
        os.system('cls')

  def tambah_barang(self): 
    os.system('cls')
    print('='*30)
    print(' Tambah Barang '.center(30, "="))
    print('='*30)

    while True:
      barcode = input("Scan Barcode: ")
      try:
        if barcode == "" or int(barcode) == 0:
          os.system('pause')
          os.system('cls')
          return
      except ValueError:
        input(self.style.warning('Tolong masukkan hanya angka! '))
        continue

      if not any(data['barcode'] == barcode for data in self.daftar_barang):
        barang = self.api_barang.get_barang(barcode)
        if not barang:
          input('Barang tidak terdaftar ')
          continue
        else:
          self.daftar_barang.append(barang)
      else:
        for item in self.daftar_barang:
          if item['barcode'] == barcode:
            item['jumlah'] += 1

      print('barang berhasil ditambah!')

  def tampilkan_barang(self):
    total_harga = self.hitung_total()
    if not self.daftar_barang:
      print("Keranjang kosong. ")
      return False
    else:
      print('-' * 72)
      print(' Isi Keranjang '.center(72, '-'))
      print('-' * 72)
      print('| ', end='')
      print('No.'.center(4, ' '), end='|')
      print('Nama'.center(30, ' '), end='|')
      print('Harga'.center(15, ' '), end='|')
      print('Jumlah'.center(10, ' '), end='|')
      print('Stok'.center(5, ' '), '|')
      print('-' * 72)

      for idx, item in enumerate(self.daftar_barang):
        print('| ', end='')
        print(str(idx + 1).ljust(4, ' '), end='| ')
        print(item['nama'].ljust(29, ' '), end='| ')
        print(str(item['harga']).ljust(14, ' '), end='| ')
        print(str(item['jumlah']).ljust(8, ' '), end=' | ')
        print(str(item['stok']).ljust(5, ' '), end='|\n')

      print('-' * 72)
      print('| ', end='')
      print('Total Harga'.ljust(35, ' '), end=' ')
      print(str(f"Rp. {total_harga:,.0f}").ljust(33, ' '), end='|\n')
      print('-' * 72)

  def edit_barang(self):
    if self.tampilkan_barang() != 0:
      try:
        index = int(input('Masukkan nomor barang yang ingin di edit\n> '))
      except ValueError:
        print("Masukkan angka saja!")
        return
      if index > len(self.daftar_barang):
        print('Masukkan nomor yang valid!')
        return
      
      try:
        jumlah = int(input('Masukkan jumlah barang baru\n> '))
      except ValueError:
        print("Masukkan angka saja!")
        return
      
      if jumlah > self.daftar_barang[index - 1]['stok']:
        print(f"Stok barang hanya {self.daftar_barang[index - 1]['stok']}")
        return

      print('Barang berhasil diedit!')
      self.daftar_barang[index - 1]['jumlah'] = jumlah

  def hapus_barang(self):
    if self.tampilkan_barang() != 0:
      try:
        index = int(input('Masukkan nomor barang yang ingin di hapus\n> '))
      except ValueError:
        print("Masukkan angka saja!")
        return
      if index > len(self.daftar_barang):
        input('Masukkan nomor yang valid! ')
        return
      
      confirmDel = input('Barang yang dihapus tidak bisa di kembalikan!.\nApakah anda yakin?\n(y/n)> ')
      if confirmDel == 'y':
        del self.daftar_barang[index - 1]
        print('Barang berhasil dihapus!')
      else:
        print('Barang gagal dihapus!')

  def hitung_total(self):
    total_harga = 0
    for item in self.daftar_barang:
      total_harga += (item['harga'] * item['jumlah'])
    return total_harga
  
  def cetak_struk(self, total_harga, uang_dibayar):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    struk_dir = os.path.join(base_dir, "../data")
    os.makedirs(struk_dir, exist_ok=True)

    waktu = datetime.now().strftime("%Y%m%d-%H%M%S")
    nama_file = f"struk-{waktu}.txt"
    file_path = os.path.join(struk_dir, nama_file)

    kembalian = uang_dibayar - total_harga

    with open(file_path, "w") as f:
      f.write("=" * 40 + "\n")
      f.write("STRUK PEMBAYARAN KASIR".center(40, " ") + "\n")
      f.write("=" * 40 + "\n")
      f.write(f"Tanggal: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} | {self.name}\n")
      f.write("-" * 40 + "\n")

      for item in self.daftar_barang:
        subtotal = item["harga"] * item["jumlah"]
        f.write(f"{item['nama'][:20]:20} x{item['jumlah']:2}  Rp{subtotal:10,}\n")

      f.write("-" * 40 + "\n")
      f.write(f"Total: {'Rp ' + format(total_harga, ','):>27}\n")
      f.write(f"Uang Dibayar: {'Rp ' + format(uang_dibayar, ','):>20}\n")
      f.write(f"Kembalian: {'Rp ' + format(kembalian, ','):>23}\n")
      f.write("=" * 40 + "\n")
      f.write("Terima kasih telah berbelanja!".center(40, " ") + "\n")
      f.write("=" * 40 + "\n")
  
  def bayar(self):
    if self.tampilkan_barang() != 0:
      try:
        uang_dibayar = int(input("Masukkan uang pembayaran: "))
      except ValueError:
        print("tolong masukkan angka saja!")

      total = self.hitung_total()
      if uang_dibayar >= total:
        self.api_barang.update_barang(daftar_barang=self.daftar_barang)

        self.api_transaksi.simpan_transaksi(
          daftar_barang=self.daftar_barang,
          total_harga=total,
          uang_dibayar=uang_dibayar
        )
        
        kembalian = uang_dibayar - total
        print(f"Pembayaran berhasil. Kembalian: Rp{kembalian:,}")
        confirmChar = input('Cetak Struk?\n(y/n)> ')
        if confirmChar.lower() == 'y':
          self.cetak_struk(total, uang_dibayar)
          print(f"Struk berhasil dicetak!")
        elif confirmChar.lower() == 'n':
          print("Transaksi selesai tanpa cetak struk.")
        else:
          print('Pilihan Tidak valid!')
      else:
        print("Uang tidak cukup!")
