from app.utils.session import Session
from app.services.vocabulary_service import VocabularyService

class VocabularyController:
    def __init__(self, session: Session, vocabulary_view, search_view):
        self.session = session
        self.vocabulary_view = vocabulary_view
        self.search_view = search_view

        search_view.result_selected.connect(self.on_result_selected)

        # ── Search ────────────────────────────────────────────────────────────────

    def on_result_selected(self, post_id:int):
        vocabs = VocabularyService.get_by_story_id(
            user_id=self.session.user_id,
            story_id=post_id
        )
        if vocabs is None:
            return
        vocab_list = [(vocab.word, vocab.translation) for vocab in vocabs]
        self.vocabulary_view.set_vocabulary(vocab_list)

