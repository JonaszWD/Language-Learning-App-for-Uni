from app.services.text_service import TextService


def test_empty_sentence_returns_error_without_calling_deepl():
    assert TextService.translate_text("") == "Error, no sentence provided"
