from PyQt6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout,
    QLineEdit, QPushButton, QFrame
)
from PyQt6.QtCore import Qt
from app.views.widgets.wigets import make_label, make_input


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(400, 460)

        self.controller = None

        self._build_ui()
        self._center()

    def _center(self):
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(32, 32, 32, 32)

        card = QFrame()
        card.setObjectName("card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(32, 36, 32, 32)
        layout.setSpacing(0)

        # Header
        layout.addWidget(make_label("Welcome Back", "title", Qt.AlignmentFlag.AlignCenter))
        layout.addSpacing(6)
        layout.addWidget(make_label("Sign in to your account", "subtitle", Qt.AlignmentFlag.AlignCenter))
        layout.addSpacing(32)

        # Username
        layout.addWidget(make_label("Username", "field_label"))
        layout.addSpacing(6)
        self.username_input = make_input("Enter your username")
        layout.addWidget(self.username_input)
        layout.addSpacing(18)

        # Password
        layout.addWidget(make_label("Password", "field_label"))
        layout.addSpacing(6)
        self.password_input = make_input("Enter your password", QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)
        layout.addSpacing(8)

        # Error label
        self.error_label = make_label("", "error_label", Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.error_label)
        layout.addSpacing(20)

        # login button
        self.login_btn = QPushButton("Sign In")
        self.login_btn.setObjectName("primary_btn")
        self.login_btn.setFixedHeight(42)
        self.login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.login_btn)
        layout.addSpacing(14)

        # Divider
        layout.addWidget(make_label("— Don't have an account? —", "divider_label", Qt.AlignmentFlag.AlignCenter))
        layout.addSpacing(20)

        # Register button
        self.register_btn = QPushButton("Register")
        self.register_btn.setObjectName("ghost_btn")
        self.register_btn.setFixedHeight(40)
        self.register_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.register_btn)
        layout.addSpacing(14)

        outer.addWidget(card)

    def set_controller(self, controller):
        self.controller = controller

        self.login_btn.clicked.connect(self.controller.handle_login)
        self.register_btn.clicked.connect(self.controller.show_register)