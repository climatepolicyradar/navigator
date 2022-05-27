"""Text encoders."""

from abc import ABC, abstractmethod
from typing import List

from sentence_transformers import SentenceTransformer
import numpy as np


class SentenceEncoder(ABC):
    """Base class for a sentence encoder"""

    @abstractmethod
    def encode(self, text: str) -> np.ndarray:
        """Encode a string, return a numpy array."""
        raise NotImplementedError

    @abstractmethod
    def encode_batch(self, text_batch: List[str], batch_size: int) -> np.ndarray:
        """Encode a batch of strings, return a numpy array."""
        raise NotImplementedError

    @property
    @abstractmethod
    def dimension(self) -> int:
        """Return the dimension of the embeddings produced by the encoder."""
        raise NotImplementedError


class SBERTEncoder(SentenceEncoder):
    """Encoder which uses the sentence-transformers library.

    A list of pretrained models is available at https://www.sbert.net/docs/pretrained_models.html.
    """

    def __init__(self, model_name: str):
        super(SBERTEncoder).__init__()
        # logger.debug("Downloading sentence-transformers model")
        self.encoder = SentenceTransformer(model_name)

    def encode(self, text: str) -> np.ndarray:
        """Encode a string, return a numpy array.

        Args:
            text (str): string to encode.

        Returns:
            np.ndarray
        """
        return self.encoder.encode(text)

    def encode_batch(self, text_batch: List[str], batch_size: int = 32) -> np.ndarray:
        """Encode a batch of strings, return a numpy array.

        Args:
            text_batch (List[str]): list of strings to encode.
            batch_size (int, optional): batch size to encode strings in. Defaults to 32.

        Returns:
            np.ndarray
        """
        return self.encoder.encode(
            text_batch, batch_size=batch_size, show_progress_bar=False
        )

    @property
    def dimension(self) -> int:
        """Return the dimension of the embedding."""
        return self.encoder.get_sentence_embedding_dimension()
