"""
Embedding generation using SentenceTransformer
"""

import logging
from typing import List, Optional
import numpy as np
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

class EmbeddingManager:
    """Handles document embedding generation."""

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2"
    ):
        self.model_name = model_name
        self.model: Optional[SentenceTransformer] = None
        self._load_model()

    def _load_model(self) -> None:
        """Load the SentenceTransformer model"""
        try:
            logger.info(f"Loading embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            logger.info(
                f"Model loaded. Dimension: {self.model.get_sentence_embedding_dimension()}"
            )
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise

    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """generate embeddings for {len(texts)} texts"""
        if not self.model:
            raise ValueError("Model not loaded")

        logger.info(f"Generating embeddings for {len(texts)} texts ")
        embeddings = self.model.encode(texts, show_progress_bar=True)
        return embeddings

    def get_dimension(self) -> int:
        """Get the embedding dimenstions. """
        if not self.model:
            raise ValueError("Model not loaded.")
        return self.model.get_sentence_embedding_dimension()


