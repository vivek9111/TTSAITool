from TTS.api import TTS
import torch
import uuid
import os

class VoiceCloningLoader:
    """
    Loader for the XTTS v2 voice cloning model from Coqui TTS
    This class is responsible for:
    1. Initializing the XTTS model and loading it into memory
    2. Providing a method to generate audio from input text and a reference speaker wav file
    The generate() method takes in the text to be synthesized, the path to the speaker's reference wav file, and the language code. It returns the generated audio as a list of floats (PCM data).
    """

    def __init__(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        # Ensure you allow for the Coqui license if prompted in console
        self.model = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
        print("XTTS model loaded on", device)

        self.outputDir = "generated_audio"
        os.makedirs(self.outputDir, exist_ok=True)
    
    def generate(self, text: str, speaker_wav: str, language="hi"):
        """
        Generates audio from input text and a reference speaker wav file.
        """
        filePath = os.path.join(self.outputDir, f"{uuid.uuid4()}.wav")
        print("Generating wav of path: ", filePath)
        return self.model.tts_to_file(
            text=text,
            speaker_wav=speaker_wav,
            language=language,
            file_path=filePath
        )

    def generate_stream(self, text_chunks, speaker_wav, language="hi"):
        """
        Takes a list of sentences and yields audio for each sentence.
        """
        for chunk in text_chunks:
            if not chunk.strip():
                continue
            
            # .tts() returns a list of floats (PCM)
            # This happens in memory - much faster for streaming than tts_to_file
            audio = self.model.tts(
                text=chunk,
                speaker_wav=speaker_wav,
                language=language
            )
            yield audio