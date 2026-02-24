from app.models.HindiVitsLoader import HindiVitsLoader

class ModelRegistry:
    _hindiTtsModel = None

    @classmethod
    def loadModels(cls):
        print("Loading Hindi model...")
        cls._hindiTtsModel = HindiVitsLoader()
        print("Hindi model assigned:", cls._hindiTtsModel)

    @classmethod
    def getHindiTtsModel(cls):
        print("Returning model:", cls._hindiTtsModel)
        return cls._hindiTtsModel