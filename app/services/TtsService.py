from app.models.HindiVitsLoader import HindiVitsLoader

class TtsService:
    def __init__(self):
        self.vitsLoader = HindiVitsLoader()

    def generateSpeech(self, text: str, language: str, voiceId: str):
        # For now: Hindi only
        return self.vitsLoader.generateAudio(text)