from app.services.vocabulary_service import VocabularyService

story = "La casa de Rosa es vieja pero muy bonita. Está hecha de piedra y tiene muchas flores rojas en el jardín. En la cocina, hay un olor delicioso. Rosa está preparando una cena especial para su nieta. Vamos a cocinar juntas, dice Rosa. Ellas preparan una tortilla de patatas, que es la comida favorita de Elena. Elena corta las patatas y Rosa fríe las cebollas. Mientras cocinan, hablan de la familia y de los amigos. Rosa cuenta historias de cuando ella era niña y no había televisión ni internet. Elena escucha con mucha atención y ríe con las historias de su abuela"
story_id = 6
user_id = 6
import re

def extract_words(text: str) -> list[str]:
    """
    Returns a list of clean unique words from the text,
    stripped of punctuation, numbers and extra whitespace.
    """
    words = re.findall(r"[a-záéíóúüñA-ZÁÉÍÓÚÜÑ]+", text)
    return list(dict.fromkeys(words))

for word in extract_words(story):
    word_lower = word.lower()
    VocabularyService.save(word_lower, user_id, story_id)

