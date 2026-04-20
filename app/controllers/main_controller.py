import os
import subprocess
import tempfile

import pygame
from mutagen.mp3 import MP3

from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6.QtCore import QTimer, QThread, pyqtSignal

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
from app.services.polly_service import PollyService

pygame.mixer.init()


# ── Background workers ────────────────────────────────────────────────────────

class _PollyWorker(QThread):
    finished = pyqtSignal(bytes)
    error = pyqtSignal(str)

    def __init__(self, text: str):
        super().__init__()
        self.text = text

    def run(self):
        try:
            self.finished.emit(PollyService.synthesize(self.text))
        except Exception as exc:
            self.error.emit(str(exc))


class _SpeedWorker(QThread):
    """Re-encodes audio_bytes at the given speed factor. seek_ms is the
    original-time millisecond position to start from after the new file loads."""
    finished = pyqtSignal(bytes, int)   # (processed_bytes, seek_original_ms)
    error = pyqtSignal(str)

    def __init__(self, audio_bytes: bytes, speed: float, seek_original_ms: int):
        super().__init__()
        self.audio_bytes = audio_bytes
        self.speed = speed
        self.seek_original_ms = seek_original_ms

    def run(self):
        in_tmp = out_tmp = None
        try:
            if abs(self.speed - 1.0) < 0.02:
                self.finished.emit(self.audio_bytes, self.seek_original_ms)
                return

            in_tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            in_tmp.write(self.audio_bytes)
            in_tmp.close()

            out_tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            out_tmp.close()

            subprocess.run(
                ['ffmpeg', '-y', '-i', in_tmp.name,
                 '-filter:a', f'atempo={self.speed}',
                 out_tmp.name],
                check=True,
                capture_output=True,
            )

            with open(out_tmp.name, 'rb') as f:
                self.finished.emit(f.read(), self.seek_original_ms)
        except Exception as exc:
            self.error.emit(str(exc))
        finally:
            for path in (in_tmp, out_tmp):
                if path and os.path.exists(path.name):
                    try:
                        os.remove(path.name)
                    except OSError:
                        pass


# ── Controller ────────────────────────────────────────────────────────────────

class MainController:
    def __init__(self, session: Session, search_panel, text_panel, vocabulary_panel, main_window):
        self.session = session
        self.search_panel = search_panel
        self.text_panel = text_panel
        self.vocabulary_panel = vocabulary_panel
        self.main_window = main_window

        # Audio state
        self._current_post_id: int | None = None
        self._raw_audio_bytes: bytes | None = None   # original 1× bytes from DB
        self._processed_speed: float = 1.0           # speed of currently loaded audio
        self._total_original_ms: int = 0
        self._session_start_original_ms: int = 0     # original-ms position at last play()
        self._is_paused: bool = False
        self._audio_tmp_path: str | None = None

        self._polly_worker: _PollyWorker | None = None
        self._speed_worker: _SpeedWorker | None = None

        # 200 ms poll for progress bar
        self._progress_timer = QTimer()
        self._progress_timer.setInterval(200)
        self._progress_timer.timeout.connect(self._update_progress)

        self.search_controller = SearchController(
            session=self.session,
            search_view=self.search_panel,
            text_view=self.text_panel,
        )
        self.text_controller = TextController(text_panel=self.text_panel)
        self.vocabulary_controller = VocabularyController(
            session=self.session,
            search_view=self.search_panel,
            vocabulary_view=self.vocabulary_panel,
        )

        # Translation debounce
        self._pending_text = ""
        self._translation_timer = QTimer()
        self._translation_timer.setSingleShot(True)
        self._translation_timer.setInterval(400)
        self._translation_timer.timeout.connect(self._do_translate)

        self._wire_signals()

    def _wire_signals(self):
        self.text_panel.translation_requested.connect(self._on_translation_requested)
        self.search_panel.gemini_requested.connect(self._open_gemini_window)
        self.search_panel.result_selected.connect(self._on_story_selected)
        self.main_window.download_btn.clicked.connect(self._handle_download)
        self.main_window.play_btn.clicked.connect(self._handle_play_pause)
        self.main_window.speed_slider.valueChanged.connect(self._on_slider_moved)
        self.main_window.speed_slider.sliderReleased.connect(self._on_speed_changed)

    # ── Story selection ───────────────────────────────────────────────────────

    def _on_story_selected(self, post_id: int):
        self._reset_playback()
        self._current_post_id = post_id
        self._raw_audio_bytes = None
        self.main_window.download_btn.setEnabled(True)

        audio = SearchService.get_audio(post_id, self.session.user_id)
        if audio:
            self._raw_audio_bytes = audio
            self._total_original_ms = self._read_duration_ms(audio)
            self._enable_audio_controls(True)
        else:
            self._enable_audio_controls(False)

    def _enable_audio_controls(self, enabled: bool):
        self.main_window.play_btn.setEnabled(enabled)
        self.main_window.speed_widget.setEnabled(enabled)

    # ── Download ──────────────────────────────────────────────────────────────

    def _handle_download(self):
        if self._current_post_id is None:
            return
        post = SearchService.get_by_id(self._current_post_id, self.session.user_id)
        if post is None:
            return

        self.main_window.download_btn.setEnabled(False)
        self.main_window.download_btn.setText("…")

        self._polly_worker = _PollyWorker(post.content or post.title)
        self._polly_worker.finished.connect(self._on_audio_ready)
        self._polly_worker.error.connect(self._on_audio_error)
        self._polly_worker.start()

    def _on_audio_ready(self, audio: bytes):
        SearchService.save_audio(self._current_post_id, self.session.user_id, audio)
        self._raw_audio_bytes = audio
        self._total_original_ms = self._read_duration_ms(audio)
        self.main_window.download_btn.setText("⬇")
        self.main_window.download_btn.setEnabled(False)
        self._enable_audio_controls(True)

    def _on_audio_error(self, message: str):
        self.main_window.download_btn.setText("⬇")
        self.main_window.download_btn.setEnabled(True)
        QMessageBox.critical(self.main_window, "Audio Error", f"Failed to generate audio:\n{message}")

    # ── Play / Pause ──────────────────────────────────────────────────────────

    def _handle_play_pause(self):
        if self._speed_worker and self._speed_worker.isRunning():
            return  # still processing, ignore click

        if self._is_paused:
            pygame.mixer.music.unpause()
            self._is_paused = False
            self._progress_timer.start()
            self.main_window.play_btn.setText("⏸ Pause")
            return

        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self._is_paused = True
            self._progress_timer.stop()
            self.main_window.play_btn.setText("▶ Resume")
            return

        # Start fresh from beginning
        if self._raw_audio_bytes is None:
            return
        self._begin_processing(seek_original_ms=0)

    # ── Speed slider ──────────────────────────────────────────────────────────

    def _on_slider_moved(self, value: int):
        self.main_window.speed_label.setText(f"{value / 100:.1f}×")

    def _on_speed_changed(self):
        if self._speed_worker and self._speed_worker.isRunning():
            return
        if self._raw_audio_bytes is None:
            return

        active = pygame.mixer.music.get_busy() or self._is_paused
        if not active:
            return  # nothing playing; speed will apply on next Play press

        # Calculate original-time position right now
        seek_original_ms = (
            self._session_start_original_ms
            + pygame.mixer.music.get_pos() * self._processed_speed
        )
        self._begin_processing(seek_original_ms=int(seek_original_ms))

    # ── Processing ────────────────────────────────────────────────────────────

    def _begin_processing(self, seek_original_ms: int):
        speed = self.main_window.speed_slider.value() / 100.0
        self._progress_timer.stop()
        pygame.mixer.music.stop()
        self._is_paused = False

        self.main_window.play_btn.setEnabled(False)
        self.main_window.play_btn.setText("Loading…")

        self._speed_worker = _SpeedWorker(self._raw_audio_bytes, speed, seek_original_ms)
        self._speed_worker.finished.connect(self._on_processed)
        self._speed_worker.error.connect(self._on_process_error)
        self._speed_worker.start()

    def _on_processed(self, processed_bytes: bytes, seek_original_ms: int):
        speed = self.main_window.speed_slider.value() / 100.0
        self._processed_speed = speed
        self._session_start_original_ms = seek_original_ms

        # Write processed audio to temp file
        self._cleanup_tmp()
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        tmp.write(processed_bytes)
        tmp.close()
        self._audio_tmp_path = tmp.name

        seek_s = seek_original_ms / 1000.0 / speed  # position in processed audio
        pygame.mixer.music.load(self._audio_tmp_path)
        pygame.mixer.music.play(start=seek_s)

        self.main_window.play_btn.setText("⏸ Pause")
        self.main_window.play_btn.setEnabled(True)
        self.main_window.progress_container.setEnabled(True)
        self._progress_timer.start()

    def _on_process_error(self, message: str):
        self.main_window.play_btn.setText("▶ Play")
        self.main_window.play_btn.setEnabled(True)
        QMessageBox.critical(self.main_window, "Audio Error", f"Failed to process audio:\n{message}")

    # ── Progress polling ──────────────────────────────────────────────────────

    def _update_progress(self):
        if not pygame.mixer.music.get_busy() and not self._is_paused:
            self._reset_playback()
            return

        pos_ms = pygame.mixer.music.get_pos()
        original_ms = self._session_start_original_ms + pos_ms * self._processed_speed

        if self._total_original_ms > 0:
            self.main_window.progress_bar.setValue(
                int(min(original_ms / self._total_original_ms, 1.0) * 1000)
            )
            remaining_s = max(0, int((self._total_original_ms - original_ms) / 1000))
            self.main_window.time_label.setText(
                f"{remaining_s // 60}:{remaining_s % 60:02d}"
            )

    # ── Helpers ───────────────────────────────────────────────────────────────

    @staticmethod
    def _read_duration_ms(audio_bytes: bytes) -> int:
        try:
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            tmp.write(audio_bytes)
            tmp.close()
            ms = int(MP3(tmp.name).info.length * 1000)
            os.remove(tmp.name)
            return ms
        except Exception:
            return 0

    def _reset_playback(self):
        self._progress_timer.stop()
        pygame.mixer.music.stop()
        self._is_paused = False
        self._session_start_original_ms = 0
        self._cleanup_tmp()
        self.main_window.play_btn.setText("▶ Play")
        self.main_window.progress_bar.setValue(0)
        self.main_window.time_label.setText("0:00")
        self.main_window.progress_container.setEnabled(False)

    def _cleanup_tmp(self):
        if self._audio_tmp_path and os.path.exists(self._audio_tmp_path):
            try:
                os.remove(self._audio_tmp_path)
            except OSError:
                pass
        self._audio_tmp_path = None

    # ── Translation ───────────────────────────────────────────────────────────

    def _on_translation_requested(self, text: str):
        self._pending_text = text
        self._translation_timer.start()

    def _do_translate(self):
        if not self._pending_text:
            return
        translation = TextService.translate_text(self._pending_text)
        self.text_panel.show_translation(translation)

    # ── Logout / reopen ───────────────────────────────────────────────────────

    def handle_logout(self):
        self._reset_playback()
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
        self.vocabulary_controller = VocabularyController(
            session=self.session,
            search_view=self.search_panel,
            vocabulary_view=self.vocabulary_panel,
        )

        self._current_post_id = None
        self._raw_audio_bytes = None
        self._is_paused = False
        self._wire_signals()
        self.main_window.show()

    # ── Gemini ────────────────────────────────────────────────────────────────

    def _open_gemini_window(self, text: str):
        self.gemini_window = GeminiWindow(parent=self.main_window)
        self.gemini_window.create_requested.connect(self.handle_gemini_create)
        self.gemini_window.exec()

    def handle_gemini_create(self, level: str, wordcount: str, optional: str):
        self.gemini = GeminiService()
        title, content = self.gemini.create_story(level, wordcount, optional)

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
