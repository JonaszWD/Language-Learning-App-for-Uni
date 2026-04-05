from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt


class VocabularyPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("panel")
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        title = QLabel("NEW VOCABULARY")
        title.setObjectName("section_title")
        layout.addWidget(title)

        self.vocab_list = QListWidget()
        self.vocab_list.setObjectName("result_list")
        self.vocab_list.setSpacing(2)
        self.vocab_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        layout.addWidget(self.vocab_list)

    # ── Public API ────────────────────────────────────────────────────────────

    def set_vocabulary(self, entries: list[tuple[str, str]]):
        """
        Populate the list with vocabulary entries.
        Each entry is a (word, translation) tuple.
        Called by the controller.
        """
        self.vocab_list.clear()
        for word, translation in entries:
            item = QListWidgetItem()
            item.setText(f"{word}  →  {translation}")
            item.setToolTip(f"{word}: {translation}")
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            self.vocab_list.addItem(item)

    def add_entry(self, word: str, translation: str):
        """Add a single vocabulary entry to the list."""
        item = QListWidgetItem()
        item.setText(f"{word}  →  {translation}")
        item.setToolTip(f"{word}: {translation}")
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
        self.vocab_list.addItem(item)

    def clear(self):
        """Clear all vocabulary entries."""
        self.vocab_list.clear()