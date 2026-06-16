import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtGui import QIcon 

from view.kasir_view import KasirView
from view.login_view import LoginView
from controller.kasir_controller import KasirController

def main():
    app = QApplication(sys.argv)
    base_dir = os.path.dirname(os.path.dirname(__file__))
    icon_path = os.path.join(base_dir, "assets", "favicon.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    current_window = [None]
    current_controller = [None]

    def show_login():
        nonlocal current_window, current_controller

        current_window[0] = None
        current_controller[0] = None

        login_view = LoginView()
        if login_view.exec_() == QDialog.Accepted:
            name = login_view.logged_in_name
            show_kasir(name=name)
            return True
        else:
            QApplication.quit()
            return False

    def show_kasir(name):
        nonlocal current_window, current_controller

        current_window[0] = KasirView(cashier_name=name)
        current_controller[0] = KasirController(current_window[0])
        current_window[0].logout_signal.connect(show_login)
        current_window[0].show()
        current_window[0].resize_columns()

    if show_login():
        sys.exit(app.exec_())
    sys.exit(0)


if __name__ == "__main__":
    main()
