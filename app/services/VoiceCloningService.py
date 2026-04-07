from app.core.ModelRegistry import ModelRegistry
from app.services.VoiceService import VoiceService
from app.utils.TextNormalizerIndic import IndicXTTSPreProcessor
from indicnlp.tokenize import sentence_tokenize

class VoiceCloningService:
    """
    Service for voice cloning operations. This service provides methods to clone a voice given a reference audio file and input text, 
    using the XTTS v2 model from Coqui TTS. It supports both generating the entire audio at once and streaming the audio as it is synthesized.
    The service relies on the VoiceService to retrieve stored reference audio files for given voice IDs, 
    and uses the ModelRegistry to access the globally loaded XTTS model. 
    The IndicXTTSPreProcessor is used to clean and normalize input text for better performance with the XTTS model.
    """
    
    def __init__(self):
        self.voiceService = VoiceService()
        self.indicXTTSPreProcessor = IndicXTTSPreProcessor()
        
    def cloneVoiceFromId(self, voiceId: str, text: str, language: str = "hi"):
        """
        Clones a voice given a voiceId and input text. Returns the generated audio path.
        """
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

    def cloneVoiceStreaming(self, voiceId: str, text: str, language: str = "hi"):
        """
        Clones a voice given a voiceId and input text. Returns a generator that yields PCM audio chunks as they are synthesized.
        """
        
        if not text:
            raise ValueError("Input text is empty")

        # get stored reference wav file for the given voiceId
        speaker_wav = self.voiceService.getVoiceFile(voiceId)
        
        if not speaker_wav:
            raise ValueError("Speaker wav file not found for voiceId: " + voiceId)
        
        # Split long text into sentences to bypass the XTTS context limit
        # This allows for infinite text length
        sentences = sentence_tokenize.sentence_split(text, lang=language)

        # get globally loaded XTTS model
        xtts_loader = ModelRegistry.getXttsModel()

        # Define a generator that cleans and generates each sentence
        def pcm_generator():
            for sent in sentences:
                clean_text = self.indicXTTSPreProcessor.clean_for_xtts(sent, language)
                # Yield the audio data for this specific sentence
                yield from xtts_loader.generate_stream([clean_text], speaker_wav, language)

        return pcm_generator()