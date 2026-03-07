from app.models.VoiceCloningLoader import VoiceCloningLoader
from app.services.VoiceService import VoiceService

class VoiceCloningService:
    def __init__(self):
        self.tts = VoiceCloningLoader()
        self.voiceService = VoiceService()

    def cloneVoiceFromId(self, voiceId: str, text: str):

        speaker_wav = self.voiceService.getVoiceFile(voiceId)

        return self.tts.generate(
            text=text,
            speaker_wav=speaker_wav,
            language="hi"
        )