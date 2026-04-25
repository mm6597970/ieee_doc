import nltk
from typing import List

class NLTKSplitter:
    def __init__(self):
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
    
    def split(self, text: str) -> List[str]:
        """Splits a response into atomic claims using NLTK sentence tokenization."""
        return nltk.sent_tokenize(text)
