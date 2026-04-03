from app.core.ModelRegistry import ModelRegistry
from app.services.VoiceService import VoiceService
from app.utils.TextNormalizer import TextNormalizer

class VoiceCloningService:

    def cloneVoiceFromId(self, voiceId: str, text: str, language: str = "hi"):

        # get stored reference wav file for the given voiceId
        speaker_wav = VoiceService.getVoiceFile(voiceId)

        # normalize input text
        cleanText = TextNormalizer.normalizeHindi(text)

        # get globally loaded XTTS model
        xtts = ModelRegistry.getXttsModel()

        # generate audio in memory
        return xtts.generate(
            text=cleanText,
            speaker_wav=speaker_wav,
            language=language
        )