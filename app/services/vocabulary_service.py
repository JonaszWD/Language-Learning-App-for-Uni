import re

from app.repositories.vocabulary_repository import VocabularyRepository
from app.models.vocabulary import Vocabulary
from app.utils.db import get_db
from app.services.text_service import TextService

class VocabularyService:

    @staticmethod
    def get_by_story_id(user_id: int, story_id: int) -> list[type[Vocabulary]]:
        with get_db() as db:
            repo = VocabularyRepository(db)
            vocabs = repo.get_by_story(user_id, story_id)
            for vocab in vocabs:
                db.expunge(vocab)
            return vocabs

    @staticmethod
    def get_by_user_id(user_id: int) -> list[type[Vocabulary]]:
        with get_db() as db:
            repo = VocabularyRepository(db)
            vocabs = repo.get_by_user(user_id)
            for vocab in vocabs:
                db.expunge(vocab)
            return vocabs

    @staticmethod
    def check_word(word: str, user_id: int) -> bool:
        with get_db() as db:
            repo = VocabularyRepository(db)
            vocab = repo.get_by_vocabulary(word, user_id)
            if vocab is None:
                return False
            else:
                return True

    @staticmethod
    def save(story: str, user_id: int, story_id: int):
        if not story.strip():
            raise ValueError('No story provided')
            return

        words = VocabularyService._extract_words(story)

        with get_db() as db:
            for word in words:
                word_lower = word.lower()
                if not VocabularyService.check_word(word_lower, user_id):
                    repo = VocabularyRepository(db)
                    vocab = Vocabulary(
                        word=word_lower,
                        translation=TextService.translate_text(word_lower),
                        user_id=user_id,
                        story_id=story_id
                    )
                    print(vocab)
                    repo.save(vocab)
                else:
                    print('Vocabulary already exists', word)

    @staticmethod
    def _extract_words(text: str) -> list[str]:
        """
        Returns a list of clean unique words from the text,
        stripped of punctuation, numbers and extra whitespace.
        """
        words = re.findall(r"[a-záéíóúüñA-ZÁÉÍÓÚÜÑ]+", text)
        return list(dict.fromkeys(words))