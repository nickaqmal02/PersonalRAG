"""
storing vector data 
with ChromaDB
"""

import logging
import os
import uuid
from typing import List, Any, Optional, Dict
import numpy as np
import chromadb
from langchain_core.documents import Document

# like alway declaring logger first
logger = logging.getLogger(__name__)

# how to create vector db ??
# this class VectorStore called as wrapper (clean, consistent)
class VectorStore:
    """manages document embeddings in ChromaDB. """
    def __init__(
        self,
        persist_directory: str= "./data/vector_store",
        collection_name: str = "rag_documents",
        clear_existing: bool = True,
    ):
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.clear_existing = clear_existing

        self.client: Optional[chromadb.PersistentClient] = None
        self.collection: Optional[chromadb.Collection] = None
        self._initialize()

    def _initialize(self) -> None:
        """initialize ChromaDB client and collection"""
        try:
            os.makedirs(self.persist_directory, exist_ok=True)
            self.client = chromadb.PersistentClient(
                path=self.persist_directory,
                settings=ChromaSettings(anonymized_telemetry=False), # add this
            )

            if self.clear_existing:
                try:
                    self.client.delete_collection(self.collection_name)
                    logger.info("Cleared existing collection")
                except:
                    logger.debug("No existing collection to clear")

            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "RAG document embeddings"},
            )

            logger.info(f"Vector store initialized. Collection {self.collection_name}")
            logger.info(f"Documents in collection: {self.collection.count()}")

        except Exception as e:
            logger.info(f"Error initializing vector store: {e}")
            raise

    def add_documents(self, documents: List[Document], embeddings: np.ndarray,) -> int:
        """Add documents and embeddings to the store"""
        if len(documents) != len(embeddings):
            raise ValueError(
                f"Document count ({len(documents)}) != Emedding count ({len(embeddings)})"
            )
        if not self.collection:
            raise ValueError("Collection not initialized")

        logger.info(f"Adding {len(documents)} documents to vector store")

        ids = []
        metadatas = []
        documents_text = []
        embeddings_list = []

        for i, (doc, embedding) in enumerate(zip(documents, embeddings)):
            doc_id = f"doc_{uuid.uuid4().hex[:8]}_{i}"
            ids.append(doc_id)

            metadata = dict(doc.metadata)
            metadata['doc_index'] = i
            metadata['content_length'] = len(doc.page_content)
            
            metadatas.append(metadata)

            documents_text.append(doc.page_content)
            embeddings_list.append(embedding.tolist())

        try:
            self.collection.add(
                ids=ids,
                embeddings=embeddings_list,
                metadatas=metadatas,
                documents=documents_text,
            )
            logger.info(f"Added {len(documents)} documents")
            logger.info(f"Total: {self.collection.count()}")
            return len(documents)

        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            raise

    def query(self, query_embedding: List[float], top_k: int = 5, ) -> Dict[str, Any]:
        """Query the vector store."""
        if not self.collection:
            raise ValueError("Collection not initialized")

        try:
            results = self.collection.query(
         query_embeddings=[query_embedding],
                n_results=top_k,
                include=["documents","metadatas", "distances"],
            )
            return results
        except Exception as e:
            logger.error(f"Error querying vector store: {e}")
            return {"documents": [], "metadatas": [], "distances": [], "ids": []}

    def count(self) -> int:
        """Get the number of documents in the collection"""
        if not self.collection:
            return 0
        return self.collection.count()


