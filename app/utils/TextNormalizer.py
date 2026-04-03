import unicodedata
import re
from nemo_text_processing.text_normalization.normalize import Normalizer

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