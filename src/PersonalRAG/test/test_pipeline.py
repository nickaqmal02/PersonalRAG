"""Test the full RAG pipeline"""

from PersonalRAG.core.embedding_manager import EmbeddingManager
from PersonalRAG.core.vector_store import VectorStore
from PersonalRAG.core.retriever import RAGRetriever
from PersonalRAG.llm.groq_provider import GroqProvider
from PersonalRAG.pipeline.rag_pipeline import RAGPipeline
from PersonalRAG.config.settings import settings

def main():
    if not settings.is_llm_configured:
        print(" GROQ_API_KEY not set in .env")
        return

    print(" Building pipeline... ")
    embedder = EmbeddingManager()
    store = VectorStore(clear_existing=False)
    retriever = RAGRetriever(store, embedder)
    llm = GroqProvider(
        api_key=settings.groq_api_key,
        model=settings.default_model,
    )
    # we saying to our application we use all method from ragpipeline 
    pipeline = RAGPipeline(retriever, llm, top_k=3)
    
    print(f" Vector DB: {store.count()} documents \n")

    if store.count() == 0:
        print(" No documents. Run 'PersonalRAG ingest' first.")
        return

    # lets do some query
    query = "What is machine learning ?"
    print(f" Question: {query}\n")

    result = pipeline.query(query, return_context=True)

    print("=" * 60)
    print(" Answer: ")
    print("=" * 60)
    print(result.answer)
    print("\n" + "-" * 60)
    print(f" Confidence: {result.confidence:.2%}")
    print(f" Sources: {len(result.sources)}")
    for i, source in enumerate(result.sources, 1):
        print(f"  {i}. {source['source']} (score: {source['score']:.2%})")
    print("*" * 60)

if __name__ == "__main__":
    main()

