from TTS.api import TTS
import torch
import uuid
import os

class VoiceCloningLoader:

    def __init__(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
        print("XTTS model loaded on", device)

        self.outputDir = "generated_audio"
        os.makedirs(self.outputDir, exist_ok=True)

    def generate(self, text: str, speaker_wav: str, language="hi"):

        filePath = os.path.join(self.outputDir, f"{uuid.uuid4()}.wav")
        print("Generating wav of path: ", filePath)
        return self.model.tts_to_file(
            text=text,
            speaker_wav=speaker_wav,
            language=language,
            file_path=filePath
        )