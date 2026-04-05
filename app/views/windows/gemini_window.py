from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QComboBox,
    QTextEdit, QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal
from app.views.widgets.wigets import make_label

class GeminiWindow(QDialog):
    """
    Modal dialog for Gemini text generation.
    Blocks the main window while open without closing it.

    Signals:
        create_requested (str, str, str): Emitted when the user clicks Create.
                                          Passes (option_a, option_b, extra_text).
    """

    create_requested = pyqtSignal(str, str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gemini Text Generation")
        self.setMinimumWidth(420)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)
        self._build_ui()
        self.controller = None

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # ── Option A ──────────────────────────────────────────────────────────
        layout.addWidget(self._build_label("What level do you want it to be? *"))
        self.option_a = QComboBox()
        self.option_a.setObjectName("dropdown")
        self.option_a.addItems([
            "Select an option",
            "A1",
            "A2",
            "B1",
            "B2",
            "C1",
            "C2",
        ])
        layout.addWidget(self.option_a)

        # ── Option B ──────────────────────────────────────────────────────────
        layout.addWidget(self._build_label("How many words do you want? *"))
        self.option_b = QComboBox()
        self.option_b.setObjectName("dropdown")
        self.option_b.addItems([
            "Select an option",
            "200-400",
            "400-600",
            "600-800",
            "800-1000",
        ])
        layout.addWidget(self.option_b)

        # ── Optional text ─────────────────────────────────────────────────────
        layout.addWidget(self._build_label("About what would you want the story to be about? (optional)"))
        self.extra_text = QTextEdit()
        self.extra_text.setObjectName("main_text")
        self.extra_text.setPlaceholderText("Add any extra ideas here...")
        self.extra_text.setFixedHeight(100)
        layout.addWidget(self.extra_text)

        # ── Feedback label (shown on validation error) ────────────────────────
        self.feedback_label = QLabel("")
        self.feedback_label.setObjectName("error_label")
        self.feedback_label.hide()
        layout.addWidget(self.feedback_label)

        layout.addStretch()

        # ── Create Error label ──────────────────────────────────────────────────
        self.error_label = make_label("", "error_label", Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.error_label)
        layout.addSpacing(20)

        # ── Create button ─────────────────────────────────────────────────────
        self.create_btn = QPushButton("Create")
        self.create_btn.setObjectName("primary_btn")
        self.create_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.create_btn.clicked.connect(self._on_create)
        layout.addWidget(self.create_btn)

    def _build_label(self, text: str) -> QLabel:
        label = QLabel(text)
        label.setObjectName("field_label")
        return label

    # ── Slots ─────────────────────────────────────────────────────────────────

    def _on_create(self):
        option_a = self.option_a.currentText()
        option_b = self.option_b.currentText()

        if option_a == "Select an option":
            self._show_feedback("Please select a level.")
            return
        if option_b == "Select an option":
            self._show_feedback("Please select a word count.")
            return

        self.create_btn.setText("Loading...")
        self.create_btn.setEnabled(False)  # ← disable button
        extra = self.extra_text.toPlainText().strip()

        self.create_requested.emit(option_a, option_b, extra)

    def _show_feedback(self, message: str):
        self.feedback_label.setText(message)
        self.feedback_label.show()

    # ── Public API ────────────────────────────────────────────────────────────

    def set_controller(self, controller):
        self.controller = controller
