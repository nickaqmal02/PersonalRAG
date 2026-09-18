# the question is how to retrieve from database ?? which is we find the relevant document from vector store
# what actually needed for us to produce the return value
#
import logging
from typing import List, Dict, Any

from PersonalRAG.core.vector_store import VectorStore
from PersonalRAG.core.embedding_manager import EmbeddingManager

logger = logging.getLogger(__name__)

class RAGRetriever:
    """
    Retrieves relevant documents from the vector store.

    Flow:
        1. Take user query which is string
        2. Embed it by converting to vector
        3. Search vector store
        4. Filter by score
        5. Return ranked results

    """
    # all things that we need to pass we need to initialize in this init method
    def __init__(
        self,
        vector_store: VectorStore,
        embedding_manager: EmbeddingManager,
    ):
        """
        Initialize the retriever.

        Args:
            vector_store: ChromaDB store with documents
            embedding_manager: Converts text to vectors
        """
        self.vector_store = vector_store
        self.embedding_manager = embedding_manager

    def retrieve(
        self,
        query: str,
        top_k: int=5,
        score_threshold: float = 0.0,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for a query.

        Args: 
            query: User's query
            top_k: how many documents to return
            score_threshold: Minimum similarity (0.0 - 1.0)

        Returns:
            List of documents, each with:
                - id: unique identifier
                - content: the text chunk
                - metadata: source, page, etc
                - similarity_score: 0.0 - 1.0
                - distance: raw chroma db distance

        """
        logger.debug(f"Retrieving for: {query} with top_k = {top_k}")

        # step 1: embed the query
        query_embedding = self.embedding_manager.generate_embeddings([query])[0]

        # step 2 : search the vector store
        results = self.vector_store.query(
            query_embedding=query_embedding.tolist(),
            top_k=top_k,
        )

        # step 3: process results so first we declare empy list of dictionary
        retrieved_docs: List[Dict[str, Any]] = []
        # so here we say that from that results 
        if results.get('documents'):
            documents = results['documents'][0]
            metadatas = results['metadatas'][0]
            distances = results['distances'][0]
            ids = results['ids'][0]

            for doc_id, document, metadata, distance in zip(
                ids, documents, metadatas, distances
            ):

                # convert distance to similarity_score
                # chromadb uses cosine distance
                # so siimilarity score = 1 - distance
                similarity_score = max(0.0, 1 - distance) # clamping from [0, 1]

                if similarity_score < score_threshold:
                    continue

                retrieved_docs.append({
                    'id': doc_id,
                    'content': document,
                    'metadata': metadata,
                    'similarity_score': similarity_score,
                    'distance': distance,
                })

        logger.debug(
            f"Retrieved {len(retrieved_docs)} docs"
            f"(threshold = {score_threshold})"
        )

        return retrieved_docs



        









