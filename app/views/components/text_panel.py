from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit
from PyQt6.QtCore import QPoint, pyqtSignal
from PyQt6.QtGui import QTextCursor, QTextBlockFormat

from app.views.widgets.tranlationbubble_widget import TranslationBubble


class TextPanel(QWidget):

    translation_requested = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Text Panel")
        self._bubble = TranslationBubble()
        self._build_ui()
        self._last_line_data = []

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)

        layout.addWidget(self._build_title())
        layout.addWidget(self._build_content())
        return layout

    def _build_title(self) -> QLabel:
        self.title_label = QLabel("Title")
        self.title_label.setObjectName("doc_title")
        return self.title_label

    def _build_content(self) -> QTextEdit:
        self.main_text = QTextEdit()
        self.main_text.setObjectName("main_text")
        self.main_text.setPlaceholderText("Spanish text will appear here...")
        self.main_text.setReadOnly(True)
        self.main_text.selectionChanged.connect(self._on_selection_changed)

        return self.main_text

    # ── Translation ───────────────────────────────────────────────────────────

    def _on_selection_changed(self):
        cursor = self.main_text.textCursor()
        selected = cursor.selectedText().strip()

        if not selected:
            self._bubble.hide()
            return

        self._last_line_data = self._get_selection_lines(cursor)
        self.translation_requested.emit(selected)  # ask controller for translation

    def _get_selection_lines(self, cursor: QTextCursor) -> list[tuple[int, int, int]]:
        """
        Walk through the selection line by line and return a list of
        (global_x, global_y, width) for each line's selected portion.
        """
        doc = self.main_text.document()
        sel_start = cursor.selectionStart()
        sel_end = cursor.selectionEnd()

        line_data = []
        pos = sel_start

        while pos < sel_end:
            # Cursor at the start of this line's selected portion
            c_start = QTextCursor(doc)
            c_start.setPosition(pos)
            start_rect = self.main_text.cursorRect(c_start)

            # Find the end of the current visual line
            c_eol = QTextCursor(doc)
            c_eol.setPosition(pos)
            c_eol.movePosition(QTextCursor.MoveOperation.EndOfLine)

            # Clamp to the selection end
            line_end_pos = min(c_eol.position(), sel_end)

            c_end = QTextCursor(doc)
            c_end.setPosition(line_end_pos)
            end_rect = self.main_text.cursorRect(c_end)

            x = start_rect.left()
            y = start_rect.top()
            width = max(end_rect.right() - start_rect.left(), 40)

            global_topleft = self.main_text.mapToGlobal(QPoint(x, y))
            line_data.append((global_topleft.x(), global_topleft.y(), width))

            # Stop if we've reached the end of the selection
            if c_eol.position() >= sel_end:
                break

            # Advance past the line break to the next line
            next_pos = c_eol.position() + 1
            if next_pos <= pos:
                break
            pos = next_pos

        return line_data

    # ── Public API ────────────────────────────────────────────────────────────

    def set_title(self, title: str):
        """Called by the controller to load a post's title."""
        self.title_label.setText(title)

    def set_content(self, content: str):
        """Called by the controller to load a post's content."""
        self.main_text.setPlainText(content or "")

        # Apply line spacing after text is loaded
        block_format = QTextBlockFormat()
        block_format.setLineHeight(
            300,
            QTextBlockFormat.LineHeightTypes.ProportionalHeight.value
        )
        cursor = self.main_text.textCursor()
        cursor.select(QTextCursor.SelectionType.Document)
        cursor.mergeBlockFormat(block_format)

    def show_translation(self, translation: str):
        """Called by the controller once the API responds."""
        if self._last_line_data:
            self._bubble.show_lines(self._last_line_data, translation)