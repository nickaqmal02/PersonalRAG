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

        

