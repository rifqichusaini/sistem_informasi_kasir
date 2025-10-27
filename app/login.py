from api.login_api import LoginAPI
from app.style import StyleText
import os

class LoginSystem:
	def __init__(self):
		self.api_login = LoginAPI()
		self.style = StyleText()

	def login(self):
		tryLoginCounter = 0
		confirmChar = 'n'
		while True:
			os.system("cls")
			print("="*30)
			print(" Sistem Kasir v1.0 ".center(30, "="))
			print(" login ".center(30, "="))

			if tryLoginCounter > 0:
				print(self.style.warning(f"kesempatan percobaan tersisa {3-tryLoginCounter}."))

			username = input("Username: ")
			password = input("Password: ")
			
			name = self.api_login.validate_user(user=username, passw=password)
			if name:
				print(self.style.approve(f"Login berhasil sebagai {name}!"))
				os.system('pause')
				return name
			else:
				tryLoginCounter+=1
				print(self.style.warning("Username atau password salah!"))
				if tryLoginCounter == 3:
					print(self.style.approve("Anda telah di blokir!"))
					os.system('pause')
					return False
				
				prompt = self.style.attention(f"Coba login lagi?\n")
				print(prompt, end="")
				confirmChar = input('(y/n)> ')

				if confirmChar.lower() == 'y':
					continue
				elif confirmChar.lower() == 'n':
					return False
				else:
					print(self.style.warning('Pilihan Tidak valid!'))
					continue
