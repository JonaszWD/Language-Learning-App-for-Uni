import os
from google import genai
from google.genai.errors import ServerError

from dotenv import load_dotenv
load_dotenv("/Users/jojo/PycharmProjects/IntroToProgrammingProject/app/.env")

class GeminiService:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_KEY"))

    def create_story(self, level, wordcount, optional):
        print("creating story with ",  level, wordcount, optional)
        try:
            if optional == "":
                response = self.client.models.generate_content(
                    model="gemini-3-flash-preview", contents= f"Create only a {wordcount} word short story at {level} level spanish without any of the extras. Add a title that is between 2 and 4 words at the beginning of the story and start the story two lines after the title."
                )
            else:
                response = self.client.models.generate_content(
                    model = "gemini-3-flash-preview", contents = f"Create only a {wordcount} word short story at {level} level spanish that must include something written about {optional} without any of the extras. Add a title that is between 2 and 4 words at the beginning of the story and start the story two lines after the title."
            )
        except ServerError:
            return "Error: The Gemini API is currently unavailable. Please try again later.", ""

        return self._separate_title_and_story(response.text)

    @staticmethod
    def _separate_title_and_story(text: str) -> tuple[str, str]:
        """
        Splits a text block into a title (first line) and story (remainder).
        Returns (title, story).
        """
        lines = text.strip().splitlines()
        if not lines:
            return "", ""

        title = lines[0].strip()
        story = "\n".join(lines[1:]).strip()

        return title, story
