import os
from supabase import create_client, Client
from dotenv import load_dotenv

class LoginAPI:
	def __init__(self):
		load_dotenv()
		url = os.getenv("SUPABASE_URL")
		key = os.getenv("SUPABASE_KEY")
		self.supabase: Client = create_client(url, key)

	def validate_user(self, user, passw):
		response = (
			self.supabase.table("users")
			.select("*")
			.eq("username", user)
			.eq("password", passw)
			.execute()
		)
		if len(response.data) > 0:
			return response.data[0]['name']
		return None
