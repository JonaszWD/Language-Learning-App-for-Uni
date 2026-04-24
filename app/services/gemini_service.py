import os
from google import genai
from google.genai.errors import ServerError

from dotenv import load_dotenv
load_dotenv("/Users/jojo/PycharmProjects/IntroToProgrammingProject/.env")

class GeminiService:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_KEY"))

    def create_story(self, level, wordcount, optional, language = "Spanish"):
        print("creating a story: ", language, level, wordcount, optional)
        try:
            response = self.client.models.generate_content(
                model="gemini-3-flash-preview", contents=self.create_language_story_prompt(language, level, wordcount, optional)
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

    @staticmethod
    def create_language_story_prompt(
            language: str,
            level: str,
            wordcount: int,
            content: str = None
    ) -> str:
        """
        Generate a customized prompt for creating language learning stories.

        Args:
            language: Target language (e.g., "Spanish", "French", "Japanese")
            level: CEFR level (A1, A2, B1, B2, C1, C2)
            wordcount: Approximate word count for the story
            content: Optional content focus (e.g., "daily life", "travel and food",
                     "business meeting with past tense")

        Returns:
            Formatted prompt string
        """

        # Base prompt
        prompt = f"""Write a {wordcount}-word short story in {language} at {level} level (CEFR scale).

    Requirements:
    - Title: 2-4 words in {language}, followed by two line breaks
    - Vocabulary and grammar appropriate for {level} learners"""

        # Add tense guidance based on level
        if level in ["A1", "A2"]:
            prompt += "\n- Use primarily present tense (easier for beginners)"
        elif level in ["B1", "B2"]:
            prompt += "\n- Use present and past tenses; introduce future tense where natural"
        else:  # C1, C2
            prompt += "\n- Use varied tenses as appropriate for natural storytelling"

        # Add sentence complexity based on level
        if level in ["A1", "A2"]:
            prompt += "\n- Use simple, short sentences with basic sentence structures"
        elif level in ["B1", "B2"]:
            prompt += "\n- Use moderately complex sentences with some subordinate clauses"
        else:  # C1, C2
            prompt += "\n- Use sophisticated sentence structures and varied syntax"

        # Add vocabulary guidance
        prompt += "\n- Include 3-5 common, high-frequency words relevant to everyday situations"

        # Add natural dialogue
        prompt += "\n- Natural dialogue is encouraged"

        # Optional: Content focus
        if content:
            prompt += f"\n- Content focus: {content}"

        # Closing requirements
        prompt += "\n\nStory only—no preamble, commentary, translations, explanations, or learning tips."

        return prompt