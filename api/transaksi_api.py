import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime

class TransaksiAPI:
  def __init__(self):
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    self.supabase: Client = create_client(url, key)

  def simpan_transaksi(self, daftar_barang, total_harga, uang_dibayar):
    kembalian = uang_dibayar - total_harga

    transaksi_data = {
      "tanggal": datetime.now().isoformat(),
      "total_harga": total_harga,
      "uang_dibayar": uang_dibayar,
      "kembalian": kembalian
    }

    transaksi_response = (
      self.supabase.table("transaksi")
      .insert(transaksi_data)
      .execute()
    )

    transaksi_id = transaksi_response.data[0]["id"]

    for item in daftar_barang:
      detail_data = {
        "transaksi_id": transaksi_id,
        "barcode": item["barcode"],
        "nama_barang": item["nama"],
        "harga_satuan": item["harga"],
        "jumlah": item["jumlah"],
        "subtotal": item["harga"] * item["jumlah"]
      }

      self.supabase.table("transaksi_detail").insert(detail_data).execute()
    return True
