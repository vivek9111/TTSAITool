from app.core.ModelRegistry import ModelRegistry
from app.services.VoiceService import VoiceService

class VoiceCloningService:

    def __init__(self):
        self.voiceService = VoiceService()

    def cloneVoiceFromId(self, voiceId: str, text: str, language: str = "hi"):

        # get stored reference wav
        speaker_wav = self.voiceService.getVoiceFile(voiceId)

        # get globally loaded XTTS model
        xtts = ModelRegistry.getXttsModel()

        # generate audio in memory
        return xtts.generate(
            text=text,
            speaker_wav=speaker_wav,
            language=language
        )