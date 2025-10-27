from supabase import create_client, Client
from dotenv import load_dotenv
import os

class BarangAPI:
  def __init__(self):
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    self.supabase = create_client(url, key)

  def get_barang(self, barcode):
    response = (
			self.supabase.table("barang")
			.select("*")
			.eq("barcode", barcode)
			.execute()
		)
    jumlah = 1;
    if len(response.data) > 0:
      barang = response.data[0]
      return {
        "barcode": barang['barcode'],
        "nama": barang["nama_barang"],
        "harga": barang["harga"],
        "stok": barang["stok"],
        "jumlah": jumlah,
      }
    else:
      return False
  
  def update_barang(self, daftar_barang):
    new_stok = 0

    for item in daftar_barang:
      new_stok = item['stok'] - item['jumlah']
      (
        self.supabase.table("barang")
        .update({"stok": new_stok})
        .eq("barcode", item['barcode'])
        .execute()
      )

    return