import torch
import numpy as np
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech
from transformers import SpeechT5HifiGan

class HfLoader:
    def __init__(self):
        self.device = "cpu"

        self.processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
        self.model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
        self.vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")

        self.model.to(self.device)
        self.vocoder.to(self.device)

    def generateAudio(self, text: str):
        inputs = self.processor(text=text, return_tensors="pt")

        # Speaker embedding (required)
        speaker_embeddings = torch.zeros((1, 512))

        with torch.no_grad():
            speech = self.model.generate_speech(
                inputs["input_ids"],
                speaker_embeddings,
                vocoder=self.vocoder
            )

        audioArray = speech.cpu().numpy()
        return audioArray
