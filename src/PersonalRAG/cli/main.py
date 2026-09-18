"""
RAG Agent CLI - Main entry point
this is where 
Commands: ingest, chat, status, version """
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
        PersonalRAG ingest --path ~/Documents/xxx.pdf
        PersonalRAG ingest --path ./data/ --chunk-size 500

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
# stating to our application saying that ok this is one of our command
@cli.command()
@click.option('--query', '-q', help='Ask as single question')
@click.option('--interactive', '-i', is_flag=True, help='Interactive chat mode')
@click.option('--top-k', type=int, default=5, help='Number of results (default: 5)')
def chat(query: Optional[str], interactive: bool, top_k: int):
    """
    always note that all argument that we state for click.option must be pass in this main method

    examples:
        PersonalRAG chat -q "What is machine learning"
        PersonalRAG chat -i

    """
    # first thing first we need to really check wether LLM is configured or not
    from PersonalRAG.config.settings import settings

    if not settings.is_llm_configured:
        logger.error(" GROQ_API_KEY not set in .env")
        logger.info(" Get your key: https://console.groq.com/")
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
        click.echo(' PersonalRAG chat -q "your question" ')
        click.echo(' PersonalRAG chat -i ')

# ╔════════════════════════════════════════════╗ 
# ║ALL METHOD THAT ASSOCIATE WITH MAIN CHAT QUE║ 
# ╚════════════════════════════════════════════╝ 
# always ensure that everything that u pass, must exactly same as you declare in the method
def _handle_single_query(query: str, top_k: int):
    """ Handle a single query"""
    from PersonalRAG.pipeline.rag_pipeline import RAGPipeline
    from PersonalRAG.core.retriever import RAGRetriever
    from PersonalRAG.core.embedding_manager import EmbeddingManager
    from PersonalRAG.core.vector_store import VectorStore
    from PersonalRAG.llm.groq_provider import GroqProvider
    from PersonalRAG.config.settings import settings

    try:
        # Build the whole pipeline
        logger.info(" Building the RAG pipeline...")
        # 2. Build components
        embedder = EmbeddingManager()
        store = VectorStore(clear_existing=False)
        # retriever means ?? we retrieve the binary from vector db
        retriever = RAGRetriever(store, embedder)
        
        llm = GroqProvider(
            api_key=settings.groq_api_key,
            model=settings.default_model,
        )
        # 3. Create pipeline (holds retriever + llm)
        pipeline = RAGPipeline(retriever, llm, top_k=top_k)

        logger.info(f"  Question: {query}")
        # 4. ask the pipeline 
        result = pipeline.query(query, return_context=True)

        click.echo("\n" + "=" * 60)
        click.echo(" Answer ")
        click.echo("=" * 60)
        click.echo(result.answer)
        click.echo("\n" + "-" * 60)
        click.echo(f" Confidence: {result.confidence:.2%}")
        click.echo(f" Sources: {len(result.sources)}")

        if result.sources:
            click.echo("\n References")
            for i, source in enumerate(result.sources, 1):
            click.echo(f"   {i}. {source['source']} (score: {source['score']:.2%})")
        
        click.echo("=" * 60)

    except Exception as e:
        logger.error(f" Query failed: {e}")
        raise click.Abort()

 def _handle_interactive(top_k: int) -> None:
    """Handle interactive chat mode."""
    from rich.console import Console
    from rich.prompt import Prompt
    from rich.panel import Panel
    from rich.markdown import Markdown

    from PersonalRAG.pipeline.rag_pipeline import RAGPipeline
    from PersonalRAG.core.retriever import RAGRetriever
    from PersonalRAG.core.embedding_manager import EmbeddingManager
    from PersonalRAG.core.vector_store import VectorStore
    from PersonalRAG.llm.groq_provider import GroqProvider
    from PersonalRAG.config.settings import settings

    console = Console()
    console.print("[bold yellow] Building RAG pipeline... [/bold yellow]")

    try:
        embedder = EmbeddingManager()
        store = VectorStore(clear_existing_False)
        retriever = RAGRetriever(store, embedder)
        llm = GroqProvider(
            api_key=settings.groq_api_key,
            model=settings.default_model
        )
        pipeline = RAGPipeline(retriever, llm, top_k=top_k)
    except Exception as e:
        console.print(f"[red] Failed to build pipeline: {e}[/red]")
        return

    console.print(Panel.fit(
        "[bold green] RAG Agent - Interactive Mode[/bold green]\n\n"
        "Commands:\n"
        " [cyan]/help[/cyan] - Show this help \n"
        " [cyan]/sources[/cyan] - Show sources for last answer \n"
        " [cyan]/clear[/cyan] - Clear screen \n"
        " Ask me anything about your documents"
        border_style="green"
    ))

    last_sources: list = []

    while True:
        try:
            query = Prompt.ask("\n[bold cyan]You[/bold cyan]")
        except (KeyboardInterrupt, EOFError):
            console.print("\n[yellow] Goooodbye !! [/yellow]")
            break

        query = query.strip()
        if not query:
            continue

        # handle commands
        if query.startswith("/"):
            cmd = query.lower()

            if cmd in ("/quit", "/exit", "/q")
                console.print("[yellow] Goodbye Mate [/yellow]")
                break

            elif cmd == "/help":
                console.print(Panel(
                    "[bold]Commands[/bold]\n"
                    " /help - Show help \n"
                    " /sources - Show sources for last answer\n"
                    " /clear - Clear screen\n"
                    " /quit - Exit",
                title="Help",
                border_style="cyan"
                ))
                continue

            elif cmd == "/clear":
                console.clear()
                continue

            elif cmd == "/sources":
                if not last_sources:
                    console.print("[yellow] No sources available yet. [/yellow]")

                else:
                    for i, source in enumerate(last_sources, 1):
                        console.print(f"    [cyan]{i}.[/cyan] {source['source']}")
                continue

            else:
                console.print(f"[red] Unknown command: {query} [/red]")
                continue

        # we process the query 
        with console.status("[bold yellow] Retrieving and generating.... [/bold yellow]")

            try:
                result = pipeline.query(query, return_context=True)
                last_sources = result.sources
            except Exception as e:
                console.print(f" [red] Error: {e} [/red]")
                continue

        # show answer
        console.print("[bold green] Assistant: [/bold green]")
        console.print(Markdown(result.answer))

        console.print(
            f"\n[dim] Confidence: {result.confidence:.2%} | "
            f" Sources: {len(result.sources)}"
        )

        if result.sources:
            console.print("[dim] Type /sources to see references [/dim]")

# ╔════════════════════════════════════════════╗ 
# ║               STATUS COMMAND               ║ 
# ╚════════════════════════════════════════════╝ 
#
# TELLING THIS TO OUR APPLICATION THAT CLI
@cli.command()
def status() -> None:
    """show the status of our RAG Agent"""
    from PersonalRAG.config.settings import settings

    click.echo("\n RAG Agent Status")
    click.echo("=" * 50)

    if settings.is_llm_configured:
        click.echo(f" LLM: Configured ({settings.default_model})")

    else:
        click.echo(" LLM: Not Configured (GROQ_API_KEY missing)")

    click.echo(f" Embedding: {settings.embedding_model}")

    data_path = Path(settings.data_dir)

    if data_path.exists():
        click.echo(f" Vector DB: {count} documents")
    except Exception as e:
        click.echo(f" Vector DB: Not initialized ({e})")

    click.echo("=" * 50 + "\n")



# ╔════════════════════════════════════════════╗ 
# ║              VERSION COMMAND               ║ 
# ╚════════════════════════════════════════════╝ 
#
@cli.command()
def version() -> None:
    """Show version information"""
    try:
        from PersonalRAG import __version__
        click.echo(f"RAG Agent v{__version__}")
    except ImportError:
        click.echo("RAG Agent v0.1.0")
# ╔════════════════════════════════════════════╗ 
# ║                TUI COMMAND                 ║ 
# ╚════════════════════════════════════════════╝ 
#
@cli.command()
def tui() -> None:
    """Launch the textual TUI interface."""
    logger.info(" Launching Terminal User Interface TUI... ")
    
    try:
        from PersonalRAG.tui.app import RAGChatApp
        app = RAGChatApp()
        app.run()
    except ImportError as e:
        logger.error(f"TUI not available yet.. {e}")
        logger.info(f" TUI WILL BE IMPLEMENTED SOON. HOPE YOU WILL ALWAYS BE PATIENT... .Instead just use PersonalRAG -i ....")

# ainur
# ╔════════════════════════════════════════════╗ 
# ║THE MAIN ENTRY POINT : this is wwhy all our ║ 
# ╚════════════════════════════════════════════╝ 
#
if __name__ = "__main__":
    cli()

