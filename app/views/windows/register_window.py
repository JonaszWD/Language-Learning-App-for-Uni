from PyQt6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout,
    QLineEdit, QPushButton, QFrame
)
from PyQt6.QtCore import Qt
from app.views.widgets.wigets import make_label, make_input


class RegisterWindow(QDialog):
    def __init__(self, login_window):
        super().__init__(login_window)

        self.login_window = login_window
        self.controller = None

        self.setWindowTitle("Create Account")
        self.setFixedSize(400, 520)

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
        layout.addWidget(make_label("Create Account", "title", Qt.AlignmentFlag.AlignCenter))
        layout.addSpacing(6)
        layout.addWidget(make_label("Fill in your details to register", "subtitle", Qt.AlignmentFlag.AlignCenter))
        layout.addSpacing(32)

        # Username
        layout.addWidget(make_label("Username", "field_label"))
        layout.addSpacing(6)
        self.username_input = make_input("Choose a username")
        layout.addWidget(self.username_input)
        layout.addSpacing(18)

        # Password
        layout.addWidget(make_label("Password", "field_label"))
        layout.addSpacing(6)
        self.password_input = make_input("Min. 8 characters", QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)
        layout.addSpacing(18)

        # Confirm password
        layout.addWidget(make_label("Confirm Password", "field_label"))
        layout.addSpacing(6)
        self.confirm_input = make_input("Re-enter your password", QLineEdit.EchoMode.Password)
        layout.addWidget(self.confirm_input)
        layout.addSpacing(8)

        # Feedback label
        self.feedback_label = make_label("", "error_label", Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.feedback_label)
        layout.addSpacing(20)

        # Register button
        self.register_btn = QPushButton("Create Account")
        self.register_btn.setObjectName("primary_btn")
        self.register_btn.setFixedHeight(42)
        self.register_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.register_btn)
        layout.addSpacing(14)

        # Divider
        layout.addWidget(make_label("— Already have an account? —", "divider_label", Qt.AlignmentFlag.AlignCenter))
        layout.addSpacing(20)

        # Back to login
        self.back_btn = QPushButton("Back to Login")
        self.back_btn.setObjectName("ghost_btn")
        self.back_btn.setFixedHeight(40)
        self.back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_btn.clicked.connect(self._back_to_login)
        layout.addWidget(self.back_btn)

        outer.addWidget(card)

    def set_feedback(self, text, is_error=True):
        color = "#cc0000" if is_error else "#007a3d"
        self.feedback_label.setText(text)
        self.feedback_label.setStyleSheet(f"color: {color}; font-size: 12px;")

    def _back_to_login(self):
        if self.controller:
            self.controller.show_login()

    def set_controller(self, controller):
        self.controller = controller
        self.register_btn.clicked.connect(self.controller.handle_register)
        self.back_btn.clicked.connect(self.controller.show_login)

    def closeEvent(self, event):
        event.accept()