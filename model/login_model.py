import os
from supabase import create_client, Client
from dotenv import load_dotenv


class LoginModel:
    """Model untuk handle login user"""
    
    def __init__(self):
        load_dotenv()
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        if not url or not key:
            raise RuntimeError("Konfigurasi Supabase belum lengkap. Periksa SUPABASE_URL dan SUPABASE_KEY di file .env.")

        self.supabase: Client = create_client(url, key)

    def validate_user(self, user, passw):
        """Validasi username dan password"""
        username = (user or "").strip()
        password = "" if passw is None else str(passw)

        if not username or password == "":
            return None

        response = (
            self.supabase.table("users")
            .select("name")
            .eq("username", username)
            .eq("password", password)
            .limit(1)
            .execute()
        )
        if response.data:
            return response.data[0].get("name") or username
        return None

