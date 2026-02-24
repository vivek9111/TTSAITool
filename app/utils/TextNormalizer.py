import unicodedata
import re

class TextNormalizer:
    @staticmethod
    def normalizeHindi(text: str) -> str:
        # Unicode normalization (NFC)
        normalized = unicodedata.normalize("NFC", text)

        # Remove excessive punctuation
        normalized = re.sub(r"[!?.]{2,}", ".", normalized)

        # Collapse extra spaces
        normalized = re.sub(r"\s+", " ", normalized)

        return normalized.strip()