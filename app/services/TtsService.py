from app.core.ModelRegistry import ModelRegistry
from app.utils.TextNormalizerIndic import IndicXTTSPreProcessor
from indicnlp.tokenize import sentence_tokenize

class TtsService:
    """
    Service for text-to-speech (TTS) operations.
    This service provides methods to generate speech from text using the Hindi VITS model.
    It also supports streaming TTS, which allows for generating and sending audio in chunks as it is synthesized, bypassing the typical context length limitations of TTS models.
    The service relies on the ModelRegistry to access the globally loaded Hindi TTS model (VITS-based) and uses the IndicXTTSPreProcessor to clean and normalize input text for better TTS performance.
    """
    def __init__(self):
        self.preprocessor = IndicXTTSPreProcessor()

    def generateSpeech(self, text: str, language: str, voiceId: str):
        """ 
        Generates speech from text. Returns the entire audio as a single PCM chunk.
        """
        if language != "hi":
            raise ValueError("Unsupported language")

        vitsLoader = ModelRegistry.getHindiTtsModel()

        if vitsLoader is None:
            raise RuntimeError("Hindi TTS model not loaded")

        cleanText = self.preprocessor.clean_for_xtts(text, language)

        if not cleanText:
            raise ValueError("Input text is empty")

        return vitsLoader.generateAudio(cleanText)
    

    def streamSpeech(self, text: str, language: str, voiceId: str):
        """ 
        Streams synthesized audio as it is generated. Returns a generator that yields PCM audio chunks.
        """
        if language != "hi":
            raise ValueError("Only Hindi supported")
        
        # 1. Break long text into sentences
        # This is the "Secret Sauce" to bypass the 250-character limit
        sentences = sentence_tokenize.sentence_split(text, lang=language)
        
        vitsLoader = ModelRegistry.getHindiTtsModel()
        if vitsLoader is None:
            raise RuntimeError("Hindi TTS model not loaded")
        
        # 2. Create a generator that yields audio chunk by chunk
        def audio_generator():
            for sentence in sentences:
                # Clean each individual sentence
                clean_sent = self.preprocessor.clean_for_xtts(sentence, language)
                if not clean_sent.strip():
                    continue
                
                # Generate audio for THIS sentence only
                # This returns immediately as soon as one sentence is done
                pcm_chunk = vitsLoader.generateAudio(clean_sent)
                yield pcm_chunk

        return audio_generator()