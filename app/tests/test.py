from dotenv import load_dotenv
load_dotenv("/Users/jojo/PycharmProjects/IntroToProgrammingProject/app/.env")

import boto3
from contextlib import closing
import tempfile
import os


class PollyTTS:
    def __init__(self, region='us-east-1'):
        self.polly = boto3.client(
            'polly',
            aws_access_key_id=os.getenv('POLLY_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('POLLY_SECRET_KEY'),
            region_name='us-east-1',
        )

    def speak(self, text, voice='Lupe', engine='standard'):
        """Speak text using Amazon Polly"""
        response = self.polly.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            VoiceId=voice,
            Engine=engine
        )

        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
            temp_file = fp.name
            with closing(response["AudioStream"]) as stream:
                fp.write(stream.read())

        os.system(f"afplay {temp_file}")
        os.remove(temp_file)

    def list_spanish_voices(self):
        """List all Spanish voices"""
        for lang_code in ['es-ES', 'es-US', 'es-MX']:
            response = self.polly.describe_voices(LanguageCode=lang_code)
            for voice in response['Voices']:
                print(f"{voice['Id']:15} - {voice['Gender']:6} - {voice['LanguageName']:15} - {voice['SupportedEngines']}")


# Usage
tts = PollyTTS()

# List voices
print("Available voices:")
tts.list_spanish_voices()
print()

# Try different voices
#tts.speak("Hola, soy Lucia. Me gusta la mañana.", voice='Lucia', engine="neural")
#tts.speak("Hola, soy Sergio. Me gusta la mañana.", voice='Sergio', engine="neural")
tts.speak("Hola, soy Mia. Me gusta la mañana.", voice='Mia', engine="neural")
tts.speak("Hola, soy Andres. Me gusta la mañana.", voice='Andres', engine="neural")

