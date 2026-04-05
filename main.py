import sys

from alembic.config import Config
from alembic import command

from PyQt6.QtWidgets import QApplication, QDialog

from app.controllers.auth_controller import AuthController
from app.controllers.main_controller import MainController

from app.views.windows.login_window import LoginWindow
from app.views.windows.register_window import RegisterWindow
from app.views.windows.main_window import MainWindow

from app.utils.session import Session


def run_migrations() -> None:
    """Apply any pending Alembic migrations before the app starts."""
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


def load_stylesheet(path: str) -> str:
    """Load a QSS stylesheet from the given file path."""
    with open(path, "r") as f:
        return f.read()


def run_pyqt() -> None:
    """Initialize and run the PyQt6 application."""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(load_stylesheet("app/resources/styles/style.qss"))

    session = Session()
    login_window = LoginWindow()
    register_window = RegisterWindow(login_window)

    controller = AuthController(
        session=session,
        login_view=login_window,
        register_view=register_window,
    )

    login_window.set_controller(controller)
    register_window.set_controller(controller)

    if login_window.exec() != QDialog.DialogCode.Accepted:
        sys.exit(0)

    print("opening main window")
    main_window = MainWindow(session=session)
    main_controller = MainController(
        session=session,
        search_panel=main_window.search_panel,
        text_panel=main_window.text_panel,
        vocabulary_panel=main_window.vocabulary_panel,
        main_window = main_window
        )

    main_window.set_controller(main_controller)
    main_window.show()
    sys.exit(app.exec())


def main() -> None:
    run_migrations()
    run_pyqt()


if __name__ == "__main__":
    main()