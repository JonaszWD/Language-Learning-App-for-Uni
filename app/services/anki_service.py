import os
import shutil
import tempfile
from typing import Callable
import tkinter as tk
from tkinter import filedialog
import genanki

from app.services.polly_service import PollyService

_MODEL = genanki.Model(
    1480120634,
    'Spanish Vocabulary',
    fields=[
        {'name': 'English'},
        {'name': 'Spanish'},
        {'name': 'Audio'},
    ],
    templates=[{
        'name': 'Card',
        'qfmt': '<div class=eng>{{English}}</div>',
        'afmt': (
            '{{FrontSide}}<hr id=answer>'
            '<div class=esp>{{Spanish}}</div>'
            '<div class=audio>{{Audio}}</div>'
        ),
    }],
    css=(
        '.card { font-family: Arial, sans-serif; font-size: 24px; text-align: center; }'
        '.eng { color: #1c1c1e; } .esp { color: #0071e3; font-weight: 600; }'
    ),
)


class AnkiService:
    @staticmethod
    def create_deck(
        vocabularies,
        output_path: str,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> None:
        deck = genanki.Deck(1953481399, 'Spanish Vocabulary')
        tmp_dir = tempfile.mkdtemp()
        media_files = []

        try:
            total = len(vocabularies)
            for i, vocab in enumerate(vocabularies):
                if progress_callback:
                    progress_callback(i + 1, total)

                audio_bytes = PollyService.synthesize(vocab.word)
                audio_filename = f'vocab_{vocab.id}.mp3'
                audio_path = os.path.join(tmp_dir, audio_filename)
                with open(audio_path, 'wb') as f:
                    f.write(audio_bytes)
                media_files.append(audio_path)

                note = genanki.Note(
                    model=_MODEL,
                    fields=[
                        vocab.translation or '',
                        vocab.word,
                        f'[sound:{audio_filename}]',
                    ],
                )
                deck.add_note(note)

            package = genanki.Package(deck)
            package.media_files = media_files
            package.write_to_file(output_path)
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)
