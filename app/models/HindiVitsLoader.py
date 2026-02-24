import torch
import soundfile as sf
from transformers import AutoTokenizer, VitsModel
import os

class HindiVitsLoader:
    def __init__(self):
        # Meta MMS Hindi TTS (VITS-based)
        self.modelName = "facebook/mms-tts-hin"

        # Tokenizer converts text → model tokens
        self.tokenizer = AutoTokenizer.from_pretrained(self.modelName)

        # VitsModel is REQUIRED for waveform output
        self.model = VitsModel.from_pretrained(self.modelName)

        # Equivalent to model.eval() in PyTorch best practice
        self.model.eval()

        self.outputDir = "generated_audio"
        os.makedirs(self.outputDir, exist_ok=True)

    def generateAudio(self, text: str) -> str:
        # Step 1: Text → tokens
        inputs = self.tokenizer(text, return_tensors="pt")

        # Step 2: Inference (no gradients, faster & safer)
        with torch.no_grad():
            output = self.model(**inputs)

        # output.waveform shape: (1, num_samples)
        audio = output.waveform.squeeze().cpu().numpy()

        return audio