from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QFrame, QToolBar, QLabel, QPushButton, QSizePolicy
)
from app.views.components.search_panel import SearchPanel
from app.views.components.vocabulary_panel import VocabularyPanel
from app.views.components.text_panel import TextPanel

from app.utils.session import Session
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self, session: Session):
        super().__init__()
        self.session = session
        self.setWindowTitle("Main Window")

        self.controller = None
        self.setWindowTitle("Dashboard")
        self.setMinimumSize(900, 600)
        self.resize(1100, 700)

        self._build_ui()

    def _build_ui(self):
        self.setWindowTitle("Dashboard")
        self.addToolBar(self._build_top_bar())

        central = QWidget()
        self.setCentralWidget(central)

        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addLayout(self._build_content_area())

    def _build_top_bar(self):
        bar = QToolBar()
        bar.setObjectName("toolbar")
        bar.setFixedHeight(48)
        bar.setMovable(False)

        # App name on the left
        app_label = QLabel("MyApp")
        app_label.setObjectName("app_name")
        bar.addWidget(app_label)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        bar.addWidget(spacer)

        # Logged-in user indicator
        user_label = QLabel(f"Logged in as  {self.session.username}")
        user_label.setObjectName("user_indicator")
        bar.addWidget(user_label)

        # Logout button
        logout_btn = QPushButton("Log out")
        logout_btn.setObjectName("ghost_btn")
        logout_btn.setFixedHeight(30)
        logout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        logout_btn.clicked.connect(self._handle_logout)
        bar.addWidget(logout_btn)

        return bar

    def _build_content_area(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        self.search_panel = SearchPanel(title="Search")
        layout.addWidget(self.search_panel,  stretch=1)
        layout.addWidget(self._build_divider())

        self.text_panel = TextPanel()
        layout.addWidget(self.text_panel, stretch=2)
        layout.addWidget(self._build_divider())

        self.vocabulary_panel = VocabularyPanel()
        layout.addWidget(self.vocabulary_panel,  stretch=1)

        return layout

    @staticmethod
    def _build_divider():
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setObjectName("divider")
        return line

    def _handle_logout(self):
        if self.controller:
            self.controller.handle_logout()

    def set_controller(self, controller):
        self.controller = controller
