from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import QTimer

from app.controllers.auth_controller import AuthController
from app.controllers.search_controller import SearchController
from app.controllers.text_controller import TextController
from app.controllers.vocabulary_controller import VocabularyController
from app.services.vocabulary_service import VocabularyService

from app.views.windows.login_window import LoginWindow
from app.views.windows.gemini_window import GeminiWindow
from app.views.windows.main_window import MainWindow
from app.views.windows.register_window import RegisterWindow
from app.utils.session import Session

from app.services.text_service import TextService
from app.services.gemini_service import GeminiService
from app.services.search_service import SearchService


class MainController:
    def __init__(self, session: Session, search_panel, text_panel, vocabulary_panel, main_window):
        self.session = session
        self.search_panel = search_panel
        self.text_panel = text_panel
        self.vocabulary_panel = vocabulary_panel
        self.main_window = main_window

        self.search_controller = SearchController(
            session=self.session,
            search_view=self.search_panel,
            text_view=self.text_panel,
        )
        self.text_controller = TextController(
            text_panel=self.text_panel,
        )

        self.vocabulary_controller = VocabularyController(
            session=self.session,
            search_view=self.search_panel,
            vocabulary_view=self.vocabulary_panel,
        )
        # ── Translation debounce ──────────────────────────────────────────────
        self._pending_text = ""
        self._translation_timer = QTimer()
        self._translation_timer.setSingleShot(True)
        self._translation_timer.setInterval(400)
        self._translation_timer.timeout.connect(self._do_translate)

        self.text_panel.translation_requested.connect(self._on_translation_requested)
        self.search_panel.gemini_requested.connect(self._open_gemini_window)

    # ── Translation ───────────────────────────────────────────────────────────

    def _on_translation_requested(self, text: str):
        """Receives every selection change — restarts the debounce timer."""
        self._pending_text = text
        self._translation_timer.start()

    def _do_translate(self):
        """Called once the user stops changing selection for 400ms."""
        if not self._pending_text:
            return
        translation = TextService.translate_text(self._pending_text)
        self.text_panel.show_translation(translation)

    # ── Logout / reopen ───────────────────────────────────────────────────────

    def handle_logout(self):
        self.session.logout()
        self.main_window.close()

        login_view = LoginWindow()
        register_view = RegisterWindow(login_view)

        self.auth_controller = AuthController(
            session=self.session,
            login_view=login_view,
            register_view=register_view,
        )

        login_view.set_controller(self.auth_controller)
        register_view.set_controller(self.auth_controller)

        if login_view.exec() == QDialog.DialogCode.Accepted:
            self._reopen_main(login_view)

    def _reopen_main(self, login_view: LoginWindow):
        login_view.close()

        self.main_window = MainWindow(session=self.session)
        self.main_window.set_controller(self)

        self.search_panel = self.main_window.search_panel
        self.text_panel = self.main_window.text_panel
        self.vocabulary_panel = self.main_window.vocabulary_panel

        self.search_controller = SearchController(
            session=self.session,
            search_view=self.search_panel,
            text_view=self.text_panel,
        )

        self.text_panel.translation_requested.connect(self._on_translation_requested)
        self.search_panel.gemini_requested.connect(self._open_gemini_window)

        self.main_window.show()

    # ── Gemini ────────────────────────────────────────────────────────────────

    def _open_gemini_window(self, text: str):
        self.gemini_window = GeminiWindow(parent=self.main_window)
        self.gemini_window.create_requested.connect(self.handle_gemini_create)
        self.gemini_window.exec()

    def handle_gemini_create(self, level: str, wordcount: str, optional: str):
        self.gemini = GeminiService()
        title, content = self.gemini.create_story(level, wordcount, optional)

        # sending error to Gemini window, if errors exist with the story creation.
        # Error message is saved under title.
        if content == "":
            self.gemini_window.error_label.setText(title)
        else:
            story_id = SearchService.save(
                title=title,
                content=content,
                user_id=self.session.user_id
            )

            VocabularyService.save(
                story_id=story_id,
                user_id=self.session.user_id,
                story=content
            )

            self.search_controller.on_result_selected(story_id)
            self.gemini_window.accept()