from app.models.HindiVitsLoader import HindiVitsLoader
from app.models.VoiceCloningLoader import VoiceCloningLoader


class ModelRegistry:
    _hindiTtsModel = None
    _xttsModel = None

    @classmethod
    def loadModels(cls):
        print("Loading Hindi VITS model...")
        cls._hindiTtsModel = HindiVitsLoader()
        print("Hindi model loaded.")

        print("Loading XTTS v2 model...")
        cls._xttsModel = VoiceCloningLoader()
        print("XTTS model loaded.")

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