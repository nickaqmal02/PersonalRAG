"""
Test wether our VectorStore with ChromaDB working really well or not
"""
import logging
from langchain_core.documents import Document
from PersonalRAG.core.embedding_manager import EmbeddingManager
from PersonalRAG.core.vector_store import VectorStore

# setup the basic logger configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S',
)
logger = logging.getLogger(__name__)

def main():
    print("=" * 60)
    print(" === TESTING THE VECTOR STORE === ")
    print("=" * 60)

    # =========================
    # Step 1: Create sample documents
    # =========================
    print("\n Step 1: Creating sample documents... ")

    documents = [
        
    ]
    
