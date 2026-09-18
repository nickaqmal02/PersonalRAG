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

# ╔════════════════════════════════════════════╗ 
# ║         CREATING SAMPLE DOCUMENTS          ║ 
# ╚════════════════════════════════════════════╝ 

    print("\n Step 1: Creating sample documents... ")

    documents = [
        Document(
            page_content="Machine learning is a subset of artificial intelligence that enables systems to learn from data.",
            metadata={
                "source": "ml_basics.txt",
                "page_number": 1,
                "topic": "machine_learning",
            },
        ),
        Document(
            page_content="Supervised learning uses labeled data to train models for prediction tasks.",
            metadata={
                "source": "ml_basics.txt",
                "page_number": 2,
                "topic": "Supervised_learning",
            },
        ),
        Document(
            page_content="Unsupervised learning finds patterns in unlabled data without predefined categories",
            metadata={
                "source": "ml_basics.txt",
                "page_number": 4,
                "topic": "reinforcement_learning",
            },
        ),
        Document(
            page_content="Python is a high-level programming languange created by Guido van Rossum in 1991.",
            metadata={
                "source": "python_intro.txt",
                "page_number": 1,
                "topic": "python",
            },
        ),
    ]

    print(f" Created {len(documents)} documents")
    for i, doc in enumerate(documents, 1):
        print(f"    {i}. {doc.page_content[:60]}... ")


# ╔════════════════════════════════════════════╗ 
# ║          S2: GENERATE EMBEDDINGS           ║ 
# ╚════════════════════════════════════════════╝ 
    print("\n Step 2: Generating embeddings... ")

    embedder = EmbeddingManager()
    texts = [doc.page_content for doc in documents]
    embeddings = embedder.generate_embeddings(texts)

    print(f" Generated {embeddings.shape[0]} embeddings")
    print(f" Shape: {embeddings.shape}")
    print(f" Dimension: {embedder.get_dimension()}")

    
# ╔════════════════════════════════════════════╗ 
# ║           S3: STORE IN VECTORDB            ║ 
# ╚════════════════════════════════════════════╝ 
    print("\n Step 3: Storing in vector db...")

    store = VectorStore(
        persist_directory="./data/test_vector_store",
        collection_name="test_collection",
        clear_existing=True,
    )

    store.add_documents(documents, embeddings)

    print(f" Stored {store.count()} documents")


# ╔════════════════════════════════════════════╗ 
# ║           QUERY THE VECTOR STORE           ║ 
# ╚════════════════════════════════════════════╝ 
    print("\n Step 4: Querying vector store... ")

    test_queries = [
        "What is machine learning",
        "Who created Python ?",
        "What is reinforcement learning ?",
    ]

    for query in test_queries:
        print(f"\n ? Query: {query}")

        # embed the query, how we now embedder ?? we called it as embedder = EmbeddingManager()
        query_embedding = embedder.generate_embeddings([query])[0]

        # search, what does it mean bt .tolist()
        results = store.query(
            query_embedding=query_embedding.tolist(),
            top_k=2,
        )

        # display
        if results.get('documents'):
            documents_result = results['documents'][0]
            metadatas = results['metadatas'][0]
            distances = results['distances'][0]

            for i, (doc, meta, dist) in enumerate(zip(documents_result, metadatas, distances), 1):
                similarity = 1 - dist
                print(f"    {i}. [Score: {similarity:.2%}] {doc[:80]}... ")
                print(f"    Source: {meta.get('source', 'unknown')}"
                      f"(page {meta.get('page_number', '?')}")
        else:
            print("     No results found mate :)")



# ╔════════════════════════════════════════════╗ 
# ║           S5: VERIFY PERSISTENCE           ║ 
# ╚════════════════════════════════════════════╝ 
    print("\n Step 5: Testing the persistence... ")

    # reload the store ... without clearing ....
    store2 = VectorStore(
        persist_directory="./data/test_vector_store",
        collection_name="test_collection",
        clear_existing=False,
    )

    print(f"    Reloaded store has {store2.count()} documents")

    if store2.count() == store.count():
        print(" Persistence works! Documents survived reload.")
    else:
        print(" Persistence failed! Documents lost. ")
# ╔════════════════════════════════════════════╗ 
# ║                   DONE !                   ║ 
# ╚════════════════════════════════════════════╝ 
    print("=" * 60)
    print(" All tests passed! ")
    print("=" * 60)

if __name__ == "__main__":
    main()


