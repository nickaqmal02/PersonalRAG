"""
Reranker using CrossEncoder for precise document ranking.
"""

import logging
from typing import List, Dict, Any

from sentence_transformers import CrossEncoder

logger = logging.getLogger(__name__)

class Reranker:
    """
    Reranks documents using a cross-encoder model.

    why we shall rerank >>
    - Bi-encoders (vector search) are faster
    - Cross-encoders are slow but precise
    - Retrieve many, rerank and keep best
    """

    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
        top_k: int = 5,
    ):
        """
        Initialize the reranker

        Args: ?
            model_name: CrossEncoder model name
            top_k: Number of documents to keep after reranking
        """

        self.model_name = model_name
        self.top_k = top_k
        self.model: CrossEncoder = None
        self._load_model()

    def _load_model(self) -> None:
        """Load the CrossEncoder model."""
        try:
            logger.info(f"Loading reranker: {self.model_name}")
            self.model = CrossEncoder(self.model_name)
            logger.info("Reranker loaded")
        except Exception as e:
            logger.error(f"Error loading reranker: {e}")
            raise

    def rerank(
        self,
        query: str,
        documents: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        rerank documents by relevance to query.

        Args:
            query: User's question
            documents: List of retrieved documents

        Returns:
            Reranked and trimmed list of documents
        """

        if not documents:
            return []

        logger.info(f"Reranking {len(documents)} documents")

        # create query-document pairs
        pairs = [
            (query, doc["content"])
            for doc in documents
        ]

        # score all pairs
        scores = self.model.predict(pairs)

        # attach scores to documents
        for doc, score in zip(documents, scores):
            doc["rerank_score"] = float(score)

        # sort by rerank score
        reranked = sorted(
            documents,
            key=lambda x: x["rerank_score"],
            reverse=True,
        )

        # keep only top_K
        result = reranked[:self.top_k]

        logger.info(
            f"Kept top {len(result)} documents"
            f"(scores: {[f'{['rerank_score']:.2f}' for d in result]})"
        )

        return result



