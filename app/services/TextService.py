from app.utils.TextNormalizer import TextNormalizer


class TextService:
    def __init__(self):
        pass

    def preprocessText(self, inputText: str, language: str) -> str:
        cleanedText = inputText.strip()

        if language == "hi":
            return cleanedText
        
        if language == "eng":
            return cleanedText
        
        return cleanedText