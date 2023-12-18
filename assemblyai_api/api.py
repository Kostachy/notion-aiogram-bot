import logging

from assemblyai import settings as assemblyai_settings, TranscriptionConfig
from assemblyai import Transcriber, AssemblyAIError, LanguageCode
from config import settings


class AssemblyaiHelper:
    def __init__(self):
        assemblyai_settings.api_key = settings.ASSEMBLYAI_TOKEN
        config = TranscriptionConfig(language_code=LanguageCode.ru)
        self.transcriber = Transcriber(config=config)

    def get_text_from_voice(self, audio_url: str):
        try:
            transcript = self.transcriber.transcribe(audio_url)
            return transcript.text
        except AssemblyAIError as err:
            logging.info(err)


assemblyai_helper = AssemblyaiHelper()
