from app.utils.TextNormalizer import TextNormalizer
from app.core.ModelRegistry import ModelRegistry

class TtsService:

    def generateSpeech(self, text: str, language: str, voiceId: str):
        if language != "hi":
            raise ValueError("Unsupported language")

        vitsLoader = ModelRegistry.getHindiTtsModel()

        if vitsLoader is None:
            raise RuntimeError("Hindi TTS model not loaded")

        cleanText = TextNormalizer.normalizeHindi(text)

        if not cleanText:
            raise ValueError("Input text is empty")

        return vitsLoader.generateAudio(cleanText)
    

    def streamSpeech(self, text: str, language: str, voiceId: str):
        if language != "hi":
            raise ValueError("Only Hindi supported")

        clean = TextNormalizer.normalizeHindi(text)
        vitsLoader = ModelRegistry.getHindiTtsModel()
        pcm = vitsLoader.generateAudio(clean)
        return pcm