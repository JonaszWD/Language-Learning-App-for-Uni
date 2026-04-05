from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt, pyqtSignal


class SearchPanel(QWidget):
    """
    A reusable search panel component.

    Signals:
        result_selected (str): Emitted when the user clicks a result.
                               Passes the selected item's text.
        add_requested  (str): Emitted when the user clicks the + button.
                               Passes the current search input text.
    """

    result_selected = pyqtSignal(int)
    add_requested = pyqtSignal(str)
    search_changed = pyqtSignal(str)
    gemini_requested = pyqtSignal(str)

    def __init__(self, title: str = "Search", parent=None):
        super().__init__(parent)
        self.setObjectName("Search panel")
        self._title = title
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        layout.addWidget(self._build_title())
        layout.addLayout(self._build_search_row())
        layout.addWidget(self._build_result_list())

    def _build_title(self) -> QLabel:
        label = QLabel(self._title.upper())
        label.setObjectName("section_title")
        return label

    def _build_search_row(self) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setSpacing(6)

        self.search_input = QLineEdit()
        self.search_input.setObjectName("search_input")
        self.search_input.setPlaceholderText("Search...")
        self.search_input.setFixedHeight(36)
        self.search_input.textChanged.connect(self._on_text_changed)
        self.search_input.returnPressed.connect(self._on_return_pressed)
        row.addWidget(self.search_input)

        self.add_btn = QPushButton("+")
        self.add_btn.setObjectName("icon_btn")
        self.add_btn.setFixedSize(36, 36)
        self.add_btn.setToolTip("Add new entry")
        self.add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_btn.clicked.connect(self._on_add_clicked)
        row.addWidget(self.add_btn)

        return row

    def _build_result_list(self) -> QListWidget:
        self.result_list = QListWidget()
        self.result_list.setObjectName("result_list")
        self.result_list.setCursor(Qt.CursorShape.PointingHandCursor)
        self.result_list.itemClicked.connect(self._on_item_clicked)
        return self.result_list

    # ── Public API ────────────────────────────────────────────────────────────

    def set_results(self, posts: list):
        """Populate the result list. Called by the controller."""
        self.result_list.clear()
        for post in posts:
            item = QListWidgetItem(post.title)
            item.setData(Qt.ItemDataRole.UserRole, post.id)  # store ID invisibly
            self.result_list.addItem(item)

    def clear_results(self):
        """Clear all results from the list."""
        self.result_list.clear()

    def clear_input(self):
        """Clear the search input field."""
        self.search_input.clear()

    def get_input_text(self) -> str:
        """Return the current search input text."""
        return self.search_input.text().strip()

    def set_placeholder(self, text: str):
        """Change the placeholder text on the search input."""
        self.search_input.setPlaceholderText(text)

    def set_loading(self, loading: bool):
        """
        Disable/enable the panel while a search is in progress.
        The controller calls this to prevent double-clicks during DB queries.
        """
        self.search_input.setEnabled(not loading)
        self.add_btn.setEnabled(not loading)
        self.result_list.setEnabled(not loading)

    # ── Private slots ─────────────────────────────────────────────────────────

    def _on_text_changed(self, text: str):
        """
        Fired on every keystroke. The controller decides whether to
        query the DB immediately (live search) or wait for Return.
        We emit the signal and let the controller handle the logic.
        """
        if not text.strip():
            self.clear_results()
        self.search_changed.emit(text)


    def _on_return_pressed(self):
        """Trigger search when the user presses Enter."""
        text = self.get_input_text()
        if text:
            # Re-use add_requested so the controller can handle Enter
            # the same way as clicking the + button, or connect separately.
            self.add_requested.emit(text)

    def _on_add_clicked(self):
        text = self.get_input_text()
        self.gemini_requested.emit(text)

    def _on_item_clicked(self, item: QListWidgetItem):
        """A result row was clicked — pass it up to the controller."""
        post_id = item.data(Qt.ItemDataRole.UserRole)
        self.result_selected.emit(post_id)