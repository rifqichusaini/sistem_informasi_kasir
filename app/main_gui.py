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
        
        # Close kasir window jika masih terbuka
        if current_window[0] is not None:
            current_window[0].close()
            current_window[0] = None

        login_dialog = LoginDialog()
        if login_dialog.exec_() == QDialog.Accepted:
            name = login_dialog.logged_in_name
        # debug untuk melewati login
        # if True:
        #     name = "Kasir"
            show_kasir(name=name)
        else:
            QApplication.quit()

    def show_kasir(name):
        nonlocal current_window

        current_window[0] = KasirWindow(cashier_name=name)
        current_window[0].logout_signal.connect(show_login)
        current_window[0].show()
        current_window[0].resize_columns()

    show_login()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
