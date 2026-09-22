"""
Here we will combines between retrieval and LLM generation
- here is one of example how we use two classes in one file
"""

import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from PersonalRAG.core.reranker import Reranker
from PersonalRAG.core.retriever import RAGRetriever
from PersonalRAG.llm.base import BaseLLM

logger = logging.getLogger(__name__)

@dataclass
class RAGResponse:
    """Structured response from the RAG pipeline."""
    answer: str
    sources: List[Dict[str, Any]]
    confidence: float
    context: Optional[str] = None

class RAGPipeline:
    """
    complete rag pipeline: retrieve + generate

    The Flow:
        1. User ask question
        2. Retriever finds relevant documents
        3. Context is built from documents
        4. LLM generates the answer using context
        5. Return answer + sources + confidence

    """

    def __init__(
        self,
        retriever: RAGRetriever,
        llm: BaseLLM,
        reranker: Optional[Reranker] = None,
        top_k: int = 5,
        retrieve_k: int = 20,
        score_threshold: float = 0.2,
    ):
        """
        Initialize the RAG pipeline
            describing each argument
        Args: 
            retriever: Handles document retrieval
            llm: LLM provider for generation
            top_k: Number of documents to retrieve
            score_threshold: Minimum similarity score
        """
        self.retriever = retriever
        self.reranker = reranker
        self.llm = llm
        self.top_k = top_k
        self.retrieve_k = retrieve_k
        self.score_threshold = score_threshold

    def query(
        self,
        question: str,
        return_context: bool = False,
    ) -> RAGResponse:
        """
        Execute the full RAG pipeline
        """
        logger.info(f" Processing query: {question}")

# ╔════════════════════════════════════════════╗ 
# ║              STEP 1: RETRIEVE              ║ 
# ╚════════════════════════════════════════════╝ 
        # step 1 we retrieve the relevant documents
        retrieve_count = self.retrieve_k if self.reranker else self.top_k

        logger.info(f"Step 1/4: retrieving top {retrieve_count} documents... ")

        results = self.retriever.retrieve(
            question, 
            top_k=retrieve_count,
            score_threshold=self.score_threshold,
        )

        if not results:
            logger.warning(" No relevant documents found")
            return RAGResponse(
                answer=(" I don't have enough information to answer this question."
                       " Please make sure that you have ingested documents first. "
                ),
                sources = [],
                confidence=0.0,
                context="" if return_context else None,
            )
        # step 2: Build the context
        logger.info(f" Retrieved {len(results)} documents")
# ╔════════════════════════════════════════════╗ 
# ║         STEP 2: BUILD THE CONTEXT          ║ 
# ╚════════════════════════════════════════════╝ 
        # step 2 build the context
        if self.reranker:
            logger.info('Step 2/4: Reranking to top {self.top_k} .... ')
            results = self.reranker.rerank(question, results)
            logger.info(f"Reranked to {len(results)} documents")
        else:
            logger.info(f"Step 2/4: Reranking to top {self.top_k}...")

# ╔════════════════════════════════════════════╗ 
# ║           STEP 3: BUILD CONTEXT            ║ 
# ╚════════════════════════════════════════════╝ 
        # build_context means ? 
        logger.info("STEP 3/4: Building Context... ")
        context = self._build_context(results)
        sources = self._build_sources(results)
        confidence = self._calculate_confidence(results)
# ╔════════════════════════════════════════════╗ 
# ║             STEP 4: GENERATIVE             ║ 
# ╚════════════════════════════════════════════╝ 
        logger.info("Step 4/4: Generating answer... ")
        answer = self.llm.generate_with_context(
            query=question,
            context=context,
        )

        logger.info(f" Answer generated (confidence: {confidence:.2%}")

        return RAGResponse(
            answer=answer,
            sources=sources,
            confidence=confidence,
            context=context if return_context else None
        )
        # what is _build_context ??
    def _build_context(self, results: List[Dict[str, Any]]) -> str:
        context_parts = []

        for i, doc in enumerate(results, 1):
            source = doc['metadata'].get('source', 'unknown')
            page = doc['metadata'].get(
                'page_number',
                doc['metadata'].get('page', 'N/A')
            )

            header = f"[Document {i} - {source}"
            if page != 'N/A':
                header += f", page {page}"
            header += f" (relevance: {doc['similarity_score']:.2%})]"

            context_parts.append(f"{header}\n{doc['content']}\n")

        return "\n".join(context_parts)

    def _build_sources(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """build sources list from retrieved documents"""
        sources = []

        for doc in results:
            score = doc.get('rerank_score', doc.get('similarity_score', 0))
        
            source = {
                'source': doc['metadata'].get('source', 'unknown'),
                'page': doc['metadata'].get(
                    'page_number',
                    doc['metadata'].get('page', 'N/A')
                ),
                'score': doc['similarity_score'],
                'preview': (
                    doc['content'][:200] + "..."
                    if len(doc['content']) > 200
                    else doc['content']
                ),
                'metadata': doc['metadata'],
            }
            sources.append(source)

        return sources

    def _calculate_confidence(self, results: List[Dict[str, Any]]) -> float:
        """calculate overall confidence from retrieval scores. """
        if not results:
            return 0.0

        scores = [
            doc.get('rerank_score', doc.get('similarity_score', 0))
            for doc in results
        ]

        max_score = max(scores)

        if self.reranker:
            import math
            normalized = 1 / (1 + math.exp(-max_score))
            return min(normalized, 1.0)

        return min(max_score, 1.0)









