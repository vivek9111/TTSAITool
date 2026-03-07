from app.models.HindiVitsLoader import HindiVitsLoader
from TTS.api import TTS
import torch


class ModelRegistry:
    _hindiTtsModel = None
    _xttsModel = None

    @classmethod
    def loadModels(cls):
        print("Loading Hindi VITS model...")
        cls._hindiTtsModel = HindiVitsLoader()
        print("Hindi model loaded.")

        print("Loading XTTS v2 model...")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        cls._xttsModel = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
        print("XTTS model loaded on", device)

    @classmethod
    def getHindiTtsModel(cls):
        if cls._hindiTtsModel is None:
            raise RuntimeError("Hindi TTS model not loaded.")
        return cls._hindiTtsModel

    @classmethod
    def getXttsModel(cls):
        if cls._xttsModel is None:
            raise RuntimeError("XTTS model not loaded.")
        return cls._xttsModel