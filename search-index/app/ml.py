"""From prototype

- tidy up
"""

from abc import ABC

from sentence_transformers import SentenceTransformer
import numpy as np


class SentenceEncoder(ABC):
    """Base class for a sentence encoder"""

    def encode(self, text: str):
        """Encode a string, return a numpy array."""
        pass


class SBERTEncoder(SentenceEncoder):
    def __init__(self, model_name: str):
        super(SBERTEncoder).__init__()
        # logger.debug("Downloading sentence-transformers model")
        self.encoder = SentenceTransformer(model_name)

    def encode(self, text: str) -> np.ndarray:
        return self.encoder.encode(text)
