import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtGui import QIcon 

from kasir_gui import KasirWindow
from login_gui import LoginDialog

def main():
    app = QApplication(sys.argv)
    base_dir = os.path.dirname(os.path.dirname(__file__))
    icon_path = os.path.join(base_dir, "assets", "favicon.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    current_window = [None]

    def show_login():
        nonlocal current_window

        login_dialog = LoginDialog()
        if login_dialog.exec_() == QDialog.Accepted:
            name = login_dialog.logged_in_name
        # if True:
        #     name = "Kasir"
            show_kasir(name=name)
        else:
            QApplication.quit()

    def show_kasir(name):
        nonlocal current_window

        current_window = KasirWindow(cashier_name=name)
        current_window.logout_signal.connect(show_login)
        current_window.show()
        current_window.resize_columns()

    show_login()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
