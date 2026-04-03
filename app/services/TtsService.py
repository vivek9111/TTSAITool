from app.core.ModelRegistry import ModelRegistry
from app.utils.TextNormalizerIndic import IndicXTTSPreProcessor

class TtsService:

    def generateSpeech(self, text: str, language: str, voiceId: str):
        if language != "hi":
            raise ValueError("Unsupported language")

        vitsLoader = ModelRegistry.getHindiTtsModel()

        if vitsLoader is None:
            raise RuntimeError("Hindi TTS model not loaded")

        cleanText = IndicXTTSPreProcessor().clean_for_xtts(text, language)

        if not cleanText:
            raise ValueError("Input text is empty")

        return vitsLoader.generateAudio(cleanText)
    

    def streamSpeech(self, text: str, language: str, voiceId: str):
        if language != "hi":
            raise ValueError("Only Hindi supported")

        clean = IndicXTTSPreProcessor().clean_for_xtts(text, language)

        if not clean:
            raise ValueError("Input text is empty")
        
        vitsLoader = ModelRegistry.getHindiTtsModel()
        
        if vitsLoader is None:
            raise RuntimeError("Hindi TTS model not loaded")
        
        pcm = vitsLoader.generateAudio(clean)
        return pcm