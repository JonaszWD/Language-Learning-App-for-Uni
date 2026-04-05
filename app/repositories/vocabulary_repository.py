from typing import List

from sqlalchemy.orm import Session
from app.models.vocabulary import Vocabulary

class VocabularyRepository:
    def __init__(self, db: Session):
        self.db = db

    # ── Read ──────────────────────────────────────────────────────────────────

    def get_by_story(self, user_id: int, story_id: int) -> List[type[Vocabulary]]:
        return (
            self.db.query(Vocabulary)
            .filter(Vocabulary.story_id == story_id)
            .filter(Vocabulary.user_id == user_id)
            .all()
        )

    def get_by_user(self, user_id: int) -> List[type[Vocabulary]]:
        return (
            self.db.query(Vocabulary)
            .filter(Vocabulary.user_id == user_id)
            .all()
        )

    def get_by_vocabulary(self, vocabulary: str, user_id: int) -> type[Vocabulary]:
        return (
            self.db.query(Vocabulary)
            .filter(Vocabulary.user_id == user_id)
            .filter(Vocabulary.word == vocabulary)
            .first()
        )

    # ── Write ─────────────────────────────────────────────────────────────────

    def save(self, vocab: Vocabulary) -> Vocabulary:
        self.db.add(vocab)
        self.db.flush()
        self.db.refresh(vocab)

        return vocab

    # ── Delete ────────────────────────────────────────────────────────────────#
    def delete(self, vocab: str, user_id: int, story_id: int) -> bool:
        vocab = self.get_by_vocabulary(vocab, user_id, story_id)
        if not vocab:
            return False
        self.db.delete(vocab)
        self.db.flush()
        return True