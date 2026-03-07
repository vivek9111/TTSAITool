from TTS.api import TTS
import torch
import uuid
import os

class VoiceCloningLoader:

    def __init__(self):
        self.model = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

        if torch.cuda.is_available():
            self.model = self.model.to("cuda")

        self.outputDir = "generated_audio"
        os.makedirs(self.outputDir, exist_ok=True)

    def generate(self, text: str, speaker_wav: str, language="hi"):

        filePath = os.path.join(self.outputDir, f"{uuid.uuid4()}.wav")

        return self.model.tts_to_file(
            text=text,
            speaker_wav=speaker_wav,
            language=language,
            file_path=filePath
        )