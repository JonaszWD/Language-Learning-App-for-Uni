import os
import deepl

from dotenv import load_dotenv
load_dotenv("/Users/jojo/PycharmProjects/IntroToProgrammingProject/app/.env")

class TextService:

    @staticmethod
    def translate_text(sentence: str):
        """
        Translate text to Spanish from any given language using the DeepL API.
        If no sentence is provided, return an error message.
        """
        if sentence != "":
            deepl_client = deepl.DeepLClient(os.getenv("DEEPL_KEY"))
            result = deepl_client.translate_text(sentence, source_lang="ES", target_lang="EN-GB").text
            #result = deepl_client.translate_text(sentence, target_lang="EN-GB").text
        else:
            result = "Error, no sentence provided"
        print(result)
        return result

