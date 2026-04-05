from app.services.auth_service import AuthService
from app.utils.session import Session
from app.core.security import hash_password, verify_password

class AuthController:

    """
    Handles login and register logic.
    Receives signals from LoginWindow / RegisterWindow,
    talks to AuthService, and writes the result into Session.
    """

    def __init__(self, session: Session, login_view, register_view=None, on_login_success=None):
        self.login_view = login_view
        self.register_view = register_view
        self.session = session
        self.on_login_success = on_login_success


    def handle_login(self):
        """
        Handles login logic.
        """
        username = self.login_view.username_input.text().strip()
        password = self.login_view.password_input.text()

        if not AuthService.find_user(username):
            self.login_view.error_label.setText("Username does not exist.")
            return

        user = AuthService.get_user(username)

        if not verify_password(password, user.password):
             self.login_view.error_label.setText("Password is wrong.")
             return

        self.session.login(user.id, user.name)
        self.login_view.accept()

    def handle_register(self):
        """
        Handles register logic.
        """
        username = self.register_view.username_input.text().strip()
        password = self.register_view.password_input.text()
        confirm = self.register_view.confirm_input.text()

        if not username or not password or not confirm:
            self.register_view.set_feedback("Please fill in all fields.")
            return

        if password != confirm:
            self.register_view.set_feedback("Passwords do not match.")
            return

        password = hash_password(password)

        if AuthService.find_user(username):
            self.register_view.set_feedback("Username already exists.")
            return

        AuthService.register(
            username,
            password
        )

        self.register_view.set_feedback("Registration successful! Please log in.", False)

    def show_register(self):
        """
        Shows the register view.
        """
        self.register_view.exec()

    def show_login(self):
        """
        Shows the login view.
        """
        self.register_view.close()
