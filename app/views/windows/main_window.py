from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QFrame, QToolBar, QLabel, QPushButton,
    QSizePolicy, QProgressBar, QSlider
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
        self.controller = None
        self.setWindowTitle("Dashboard")
        self.setMinimumSize(900, 600)
        self.resize(1100, 700)
        self._build_ui()

    def _build_ui(self):
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

        # ── Left: app name ────────────────────────────────────────────────────
        app_label = QLabel("MyApp")
        app_label.setObjectName("app_name")
        bar.addWidget(app_label)

        # ── Download button ───────────────────────────────────────────────────
        self.download_btn = QPushButton("⬇ Download")
        self.download_btn.setObjectName("ghost_btn")
        self.download_btn.setFixedHeight(30)
        self.download_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.download_btn.setEnabled(False)
        self.download_btn.setToolTip("Download audio for this story")
        bar.addWidget(self.download_btn)

        # ── Play / Pause button ───────────────────────────────────────────────
        self.play_btn = QPushButton("▶ Play")
        self.play_btn.setObjectName("ghost_btn")
        self.play_btn.setFixedHeight(30)
        self.play_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.play_btn.setEnabled(False)
        bar.addWidget(self.play_btn)

        # ── Progress container (always visible, grayed out until playing) ───────
        self.progress_container = QWidget()
        self.progress_container.setFixedWidth(180)
        self.progress_container.setEnabled(False)
        pc_layout = QHBoxLayout(self.progress_container)
        pc_layout.setContentsMargins(4, 0, 4, 0)
        pc_layout.setSpacing(6)

        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("audio_progress")
        self.progress_bar.setRange(0, 1000)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(6)
        pc_layout.addWidget(self.progress_bar)

        self.time_label = QLabel("0:00")
        self.time_label.setObjectName("user_indicator")
        self.time_label.setFixedWidth(38)
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        pc_layout.addWidget(self.time_label)

        bar.addWidget(self.progress_container)

        # ── Speed control ─────────────────────────────────────────────────────
        self.speed_widget = QWidget()
        self.speed_widget.setEnabled(False)
        sw_layout = QHBoxLayout(self.speed_widget)
        sw_layout.setContentsMargins(4, 0, 4, 0)
        sw_layout.setSpacing(4)

        slow_lbl = QLabel("0.5×")
        slow_lbl.setObjectName("user_indicator")
        sw_layout.addWidget(slow_lbl)

        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setObjectName("speed_slider")
        self.speed_slider.setRange(50, 200)
        self.speed_slider.setValue(100)
        self.speed_slider.setSingleStep(10)
        self.speed_slider.setPageStep(25)
        self.speed_slider.setFixedWidth(90)
        self.speed_slider.setCursor(Qt.CursorShape.PointingHandCursor)
        sw_layout.addWidget(self.speed_slider)

        fast_lbl = QLabel("2×")
        fast_lbl.setObjectName("user_indicator")
        sw_layout.addWidget(fast_lbl)

        self.speed_label = QLabel("1.0×")
        self.speed_label.setObjectName("user_indicator")
        self.speed_label.setFixedWidth(32)
        self.speed_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        sw_layout.addWidget(self.speed_label)

        bar.addWidget(self.speed_widget)

        # ── Spacer ────────────────────────────────────────────────────────────
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        bar.addWidget(spacer)

        # ── Right: Anki + user + logout ───────────────────────────────────────
        self.anki_btn = QPushButton("⬇ Anki Deck")
        self.anki_btn.setObjectName("ghost_btn")
        self.anki_btn.setFixedHeight(30)
        self.anki_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.anki_btn.setToolTip("Export all vocabulary as an Anki deck with audio")
        bar.addWidget(self.anki_btn)

        user_label = QLabel(f"Logged in as  {self.session.username}")
        user_label.setObjectName("user_indicator")
        bar.addWidget(user_label)

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
        layout.addWidget(self.search_panel, stretch=1)
        layout.addWidget(self._build_divider())

        self.text_panel = TextPanel()
        layout.addWidget(self.text_panel, stretch=2)
        layout.addWidget(self._build_divider())

        self.vocabulary_panel = VocabularyPanel()
        layout.addWidget(self.vocabulary_panel, stretch=1)

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
