from PyQt6.QtCore import QTimer
from app.services.text_service import TextService
from app.views.components.text_panel import TextPanel


class TextController:
    def __init__(self, text_panel: TextPanel):
        self.text_panel = text_panel

        self._translation_timer = QTimer()
        self._translation_timer.setSingleShot(True)
        self._translation_timer.setInterval(400)  # wait 400ms after last change
        self._translation_timer.timeout.connect(self._do_translate)

        self._text_service = TextService()
        self._pending_text = ""

        self.text_panel.translation_requested.connect(self._on_translation_requested)

    def _on_translation_requested(self, text: str):
        """Called every time selection changes — just restarts the timer."""
        self._pending_text = text
        self._translation_timer.start()  # resets the 400ms countdown each call

    def _do_translate(self):
        """Only called once the user stops selecting for 400ms."""
        if not self._pending_text:
            return
        translation = self._text_service.translate_text(self._pending_text)
        self.text_panel.show_translation(translation)