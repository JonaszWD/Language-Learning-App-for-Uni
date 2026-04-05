from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontMetrics


class BubbleSegment(QWidget):
    """
    A single horizontal strip of the translation bubble.
    One segment is created per selected line.
    """

    def __init__(self):
        super().__init__(None, Qt.WindowType.ToolTip)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # ToolTip windows sit outside the widget tree and don't inherit
        # the app stylesheet automatically — pull and apply it explicitly.
        self.setStyleSheet(QApplication.instance().styleSheet())

        # Outer window is fully transparent so rounded corners are visible.
        # The inner container carries the objectName and gets the QSS
        # background + border-radius applied to it correctly.
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        self.container = QWidget()
        self.container.setObjectName("translation_bubble")
        outer.addWidget(self.container)

        inner = QVBoxLayout(self.container)
        inner.setContentsMargins(10, 6, 10, 6)

        self.label = QLabel()
        self.label.setWordWrap(False)
        inner.addWidget(self.label)

    def show_at(self, x: int, y: int, text: str):
        """Position this segment above (x, y), sized purely to content."""
        self.label.setText(text)

        # Measure text directly with font metrics — bypasses all Qt layout caching.
        fm = QFontMetrics(self.label.font())
        text_width = fm.horizontalAdvance(text)
        h_padding = 20  # 10px left + 10px right from inner layout margins
        v_padding = 12  # 6px top + 6px bottom from inner layout margins

        new_w = text_width + h_padding
        new_h = fm.height() + v_padding

        # setFixedSize on the container forces the layout to reflow immediately,
        # overriding any cached sizes from the previous call.
        self.container.setFixedSize(new_w, new_h)
        self.adjustSize()

        # Sit just above the selection line
        self.move(x, y - self.height())
        self.show()


class TranslationBubble:
    """
    Manages a pool of BubbleSegments — one per selected line.
    Mirrors the shape of the selection, positioned just above each line.
    """

    def __init__(self):
        self._segments: list[BubbleSegment] = []

    def _get_segment(self, index: int) -> BubbleSegment:
        """Return segment at index, creating it if needed."""
        while len(self._segments) <= index:
            self._segments.append(BubbleSegment())
        return self._segments[index]

    def show_lines(self, line_data: list[tuple[int, int, int]], translation: str):
        """
        Show one bubble segment per selected line.

        Args:
            line_data: list of (global_x, global_y, width) — one per selected line.
                       global_x/y is the top-left of the selection on that line.
                       width is how wide the selection spans on that line.
            translation: the full translated string to distribute across segments.
        """
        # Hide any leftover segments from a previous longer selection
        for i in range(len(line_data), len(self._segments)):
            self._segments[i].hide()

        if not line_data:
            return

        texts = self._distribute(translation, [w for _, _, w in line_data])

        for i, ((x, y, _), text) in enumerate(zip(line_data, texts)):
            self._get_segment(i).show_at(x, y, text)

    def hide(self):
        for seg in self._segments:
            seg.hide()

    # ── Text distribution ─────────────────────────────────────────────────────

    def _distribute(self, text: str, widths: list[int]) -> list[str]:
        """
        Split translation words proportionally across segments
        based on the pixel width of each selected line.
        """
        if len(widths) == 1:
            return [text]

        words = text.split()
        if not words:
            return [''] * len(widths)

        total_width = sum(widths)
        result = []
        word_idx = 0

        for i, width in enumerate(widths):
            if i == len(widths) - 1:
                # Last segment gets all remaining words
                result.append(' '.join(words[word_idx:]))
            else:
                n = max(1, round(len(words) * width / total_width))
                result.append(' '.join(words[word_idx:word_idx + n]))
                word_idx = min(word_idx + n, len(words))

        return result