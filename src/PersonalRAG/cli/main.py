"""
RAG Agent CLI - Main entry point
this is where 
Commands: ingest, chat, status, version
"""
# what is sys
import click
import logging
import sys
from pathlib import Path

# setup logging once
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S',
    stream=sys.stdout,
)

logger = logging.getLogger(__name__)

@click.group()
def cli():
    """RAG Agent - Personal Assistant"""
    logger.info("RAG Agent started")


@cli.command()
@click.option(
    '--path', '-p',
    type=click.Path(exists=True, file_okay=True, dir_okay=True, readable=True),
    help='Path to file or directory (default: ./data)'
)
@click.option(
    '--chunk-size',
    type=int,
    default=1000,
    help='chunk size for splitting'
)
@click.option(
    '--chunk-overlap',
    type=int,
    default=200,
    help='Chunk overlap (default: 200)'
)
def ingestion(path: Optional[str] = None, chunk_size: int = 1000, chunk_overlap: int = 200):
    """
    Ingest documents into the vector store.

    how to use this method ??
    examples:
        rag-agent ingest --path ~/Documents/xxx.pdf
        rag-agent ingest --path ./data/ --chunk-size 500

    """
    try:
        from PersonalRAG.core.document_processor import DocumentProcessor
        from PersonalRAG.core.embedding_manager import EmbeddingManager
        from PersonalRAG.core.VectorStore import VectorStore
        
        # step 1: process documents
        logger.info("Step 1/3: Loading and processing documents...")
        processor = DocumentProcessor(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        source_path = path if path else processor.data.dir
        chunks = processor.process(source_path=source_path)

        if not chunks:
            logger.warning(" No documens found to process! ")
            logger.info(" Place files in ./data/ or use --path")
            return

        stats = processor.get_stats()
        logger.info(f" Loaded {len(chunks)} chunks from {stats['pages']} pages")

        # step 2: generate the embeddings
        logger.info("Step 2/3: Generating the embeddings...")
        embedder = EmbeddingManager()
        texts = [doc.page_content for doc in chunks]
        embeddings = embedder.generate_embeddings(texts)
        logger.info(f" Generated {embeddings.shape[0]} embeddings")

        # step 3: store the vector in database
        logger.info("Step 3/3: Storing those vector in database....")
        store = VectorStore()
        store.add_documents(chunks, embeddings)
        logger.info(f"Stored {store.count()} documents in vectorDB")

    except Exception as e:
        logger.error(f" Ingestion failed: {e}")
        raise click.Abort()


"""
CHAT COMMAND 
"""

@cli.command()
@click.option('--query', '-q', help='Ask as single question')
@click.option('--interactive', '-i', is_flag=True, help='Interactive chat mode')
@click.option('--top-k', type=int, default=5, help='Number of results (default: 5)')
def chat(query: Optional[str], interactive: bool, top_k: int):
    """
    always note that all argument that we state for click.option must be pass in this main method

    examples:
        rag-agent chat -q "What is machine learning"
        rag-agent chat -i

    """
    # first thing first we need to really check wether LLM is configured or not
    from PersonalRAG.config.settings import settings

    if not settings.is_llm_configured:
        logger.error(" GROQ_API_KEY not set in .env")
        logger.info(" Get ypur key: https://console.groq.com/")
        return

    if query:
        # single query mode
        _handle_single_query(query, top_k)

    elif interactive:
        # interactive mode
        _handle_interactive(top_k)

    else:
        logger.warning(" Please provide --query or --interactive")
        click.echo("\nUsage")
        click.echo(' rag-agent chat -q "your question" ')
        click.echo(' rag-agent chat -i ')

# define all method that needed for above operations
def _handle_single_query(query: str, top_k: int):
    """ Handle a single query"""
    from personalRAG.pipeline.rag_pipeline import RAGPipeline
    from personalRAG.core.retriever import RAGRetriever
    from personalRAG.core.embedding_manager import EmbeddingManager
    from personalRAG.core.vector_store import VectorStore
    from personalRAG.llm.groq_provider import GroqProvider
    from personalRAG.config.settings import settings

    try:
        # Build the whole pipeline
        logger.info(" Building the RAG pipeline...")
        embedder = EmbeddingManager()
        store = VectorStore(clear_existing=False)


#
#    
#


