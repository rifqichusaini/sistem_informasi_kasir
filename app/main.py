import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.login import LoginSystem
from app.kasir import Kasir


def main():
  login = LoginSystem()
  name = login.login()
  if not name:
    return
  

  os.system("cls")
  kasir = Kasir(name="name")
  kasir.menu()

if __name__ == "__main__":
  main()
