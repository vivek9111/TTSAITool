from app.core.ModelRegistry import ModelRegistry
from app.services.VoiceService import VoiceService
from app.utils.TextNormalizerIndic import IndicXTTSPreProcessor

class VoiceCloningService:
    
    def __init__(self):
        self.voiceService = VoiceService()
        self.indicXTTSPreProcessor = IndicXTTSPreProcessor()

    def cloneVoiceFromId(self, voiceId: str, text: str, language: str = "hi"):
        
        if not text:
            raise ValueError("Input text is empty")

        # get stored reference wav file for the given voiceId
        speaker_wav = self.voiceService.getVoiceFile(voiceId)
        
        if not speaker_wav:
            raise ValueError("Speaker wav file not found for voiceId: " + voiceId)
        
        # normalize input text using Indic NLP library for better XTTS performance
        cleanText = self.indicXTTSPreProcessor.clean_for_xtts(text, language)

        # get globally loaded XTTS model
        xtts = ModelRegistry.getXttsModel()

        # generate audio in memory
        return xtts.generate(
            text=cleanText,
            speaker_wav=speaker_wav,
            language=language
        )