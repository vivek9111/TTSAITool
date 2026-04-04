import os
from indicnlp import common as indic_common
from indicnlp.normalize import indic_normalize
from indicnlp.tokenize import indic_tokenize

# Get the directory where THIS script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Point to the resources folder relative to your script
# This assumes indic_nlp_resources is in the same folder as your script
INDIC_RESOURCES_PATH = os.path.join(BASE_DIR, "indic_nlp_resources")
indic_common.set_resources_path(INDIC_RESOURCES_PATH)

class IndicXTTSPreProcessor:
    def __init__(self):
        # Cache for normalizers to avoid re-initializing for each call
        self.normalizers = {}

    def get_normalizer(self, lang):
        if lang not in self.normalizers:
            # The factory picks the right class (Devanagari, Tamil, etc.) automatically
            factory = indic_normalize.IndicNormalizerFactory()
            self.normalizers[lang] = factory.get_normalizer(lang)
        return self.normalizers[lang]

    def clean_for_xtts(self, text, lang):
        """
        Main function to call before XTTS synthesis
        """
        # Step A: Normalize (Fixes Unicode inconsistencies)
        normalizer = self.get_normalizer(lang)
        normalized_text = normalizer.normalize(text)
        
        # Step B: Trivial Tokenization (Ensures clean spacing for the neural model)
        tokens = indic_tokenize.trivial_tokenize(normalized_text, lang)
        return " ".join(tokens)