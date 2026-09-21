"""
Textual TUI for PersonalRAG
A beautiful terminal interface for chatting with your documents.

"""
import asyncio
import logging
from typing import Optional
# ╔════════════════════════════════════════════╗ 
# ║             TEXTUAL LIBRARIES              ║ 
# ╚════════════════════════════════════════════╝ 
from textual.app import App, ComposeResult
from textual.widgets import (
    Header,
    Footer,
    Input,
    Button,
    RichLog,
    Static,
    DataTable,
    Tree,
    Tabs,
)
from textual.containers import Container, Vertical, Horizontal
from textual.reactive import reactive
from textual import events
# ╔════════════════════════════════════════════╗ 
# ║               RICH LIBRARIES               ║ 
# ╚════════════════════════════════════════════╝ 
from rich.text import Text
from rich.panel import Panel
from rich.markdown import Markdown
# ╔════════════════════════════════════════════╗ 
# ║       PersonalRAG OUR DEFINED METHOD       ║ 
# ╚════════════════════════════════════════════╝ 
from PersonalRAG.config.settings import settings
from PersonalRAG.pipeline.rag_pipeline import RAGPipeline
from PersonalRAG.core.retriever import RAGRetriever
from PersonalRAG.core.embedding_manager import EmbeddingManager
from PersonalRAG.core.vector_store import VectorStore
from PersonalRAG.llm.groq_provider import GroqProvider

logger = logging.getLogger(__name__)

class StatusBar(Static):
    """Status bar showing current state. """

    status = reactive("Ready")
    confidence = reactive(0.0)
    sources = reactive(0)

    def render(self) -> Text:
        """Render the status bar."""
        text = Text()
        text.append(" ", style="dim")
        text.append(self.status, style="bold")

        if self.confidence > 0:
            text.append(f"  | {self.confidence:0.%}", style="dim")

        if self.sources > 0:
            text.append(f"  | {self.sources} sources", style="dim")

        return text

class AnswerPanel(Static):
    """Panel showing the current answer."""
    def update_answer(self, answer: str, confidence: float, sources: int) -> None:
        """Update the answer panel."""
        text = Text()
        text.append(" Assistant\n\n", style="bold green")
        text.append(answer)
        text.append("\n\n")
        text.append(" confidence {confidence:.2%}", style="dim")
        text.append(f"  | Sources: {sources}", style="dim")
        self.update(text)

class RAGChatApp(App):
    """
    RAG Chat TUI Application

    """

    CSS = """
    Screen {
        background: $surface;
    }

    /* Chat history - top, scrollable */
    #chat-history {
        height: 1fr;
        border: solid $primary;
        margin: 1 1 0 1;
        padding: 1;
    }

    /* Current answer - prominent, fixed height */
    #answer-panel {
        height: auto;
        min-height: 5;
        max-height: 15;
        border: solid $success;
        margin: 1 1 0 1;
        padding: 1;
        background: $surface;
    }

    /* Input area */
    #input-container {
        height: 3;
        margin: 1 1 0 1;
    }

    #input-area {
        width: 1fr;
    }

    #status-bar{
        height: 1;
        background: $panel;
        color: $text;
        padding: 0 1;
        margin: 0 1;
    }

    .user-message {
        color: $text;
        margin: 1 0;
    }

    .assistant-message {
        color: $success;
        margin: 0 1;
    }

    .error-message {
        color: $error;
        margin: 1 0;
    }

    .info-message {
        color: $warning;
        margin: 1 0;
    }
    """

    # DECLARE THE SET OF BINDINGS
    BINDINGS = [
        ("ctrl+c", "quit", "Quit"),
        ("ctrl+l", "clear", "Clear"),
        ("ctrl+s", "show_sources", "Sources"),
        ("ctrl+h", "show_help", "Help"),
    ]

    TITLE = "PersonalRAG"
    SUB_TTILE = "Chat with your documents"

# ╔════════════════════════════════════════════╗ 
# ║                   STEP 0                   ║ 
# ╚════════════════════════════════════════════╝ 
    def __init__(self):
        super().__init__()
        self.pipeline: Optional[RAGPipeline] = None
        self.last_sources: list = []
        self.ready = False

# ╔════════════════════════════════════════════╗ 
# ║                   STEP 1                   ║ 
# ╚════════════════════════════════════════════╝ 
    def compose(self) -> ComposeResult:
        """Create child widgets"""
        yield Header()
        yield Container(
            RichLog(id="chat-container", highlight=True, markup=True),
            id="chat-wrapper",
        )
        yield Horizontal(
            Input(
                placeholder="Ask a question... (type /help for commands)",
                id="input-area",
            ),
            id="input-container",
        )
        yield AnswerPanel(id="answer-panel")

        yield StatusBar(
            id="status-bar"
        )
        yield Footer()

# ╔════════════════════════════════════════════╗ 
# ║                   STEP 2                   ║ 
# ╚════════════════════════════════════════════╝ 
    def on_mount(self) -> None:
        """Initialize when app starts."""
        self.set_status(" Building RAG pipeline... ")
        self.build_pipeline()
        self.show_welcome()
        self.focus_input()

    def build_pipeline(self) -> None:
        """Build the RAG pipeline."""
        try:
            # check API key
            if not settings.is_llm_configured:
                self.write_error("😡 GROQ_API_KEY not set in .env")
                self.write_info(" Get your key: https://console.groq.com/")
                return

            # Build the components
            embedder = EmbeddingManager()
            store = VectorStore(clear_existing=False)
            retriever = RAGRetriever(store, embedder)
            llm = GroqProvider(
                api_key=settings.groq_api_key,
                model=settings.default_model,
            )

            # create pipeline
            self.pipeline = RAGPipeline(
                retriever=retriever,
                llm=llm,
                top_k=settings.top_k,
                score_threshold=settings.score_threshold,
            )

            # check if documents exist
            doc_count = store.count()

            if doc_count == 0:
                self.write_warning(" No documents in vector store !")
                self.write_info(" Run: PersonalRAG ingestion")
                self.set_status(" No documents")
            else:
                self.ready = True
                self.set_status(f" Ready ({doc_count} documents)")
                self.write_success(f" Loaded {doc_count} documents")

        except Exception as e:
            self.write_error(f" Failed to build pipeline: {e}")
            self.set_status(" Error")

    def show_welcome(self) -> None:
        """Show welcome message."""
        welcome = Panel(
            "[bold green] PersonalRAG [/bold green] \n\n"
            "Chat with your documents using AI. \n\n"
            "[bold]Commands:[/bold]\n"
            "   [cyan]/help[/cyan] - Show this help\n"
            "   [cyan]/sources[/cyan] - Show sources for last answer \n"
            "   [cyan]/clear[/cyan] - Clear the chat \n"
            "   [cyan]/status[/cyan] - Show system status \n"
            "   [bold]Keyboard shortcuts:[/bold] \n"
            "   [cyan]Ctrl+L[/cyan] - Clear\n"
            "   [cyan]Ctrl+S[/cyan] - Show sources\n"
            "   [cyan]Ctrl+H[/cyan] - Help\n"
            "   [cyan]Ctrl+C[/cyan] - Quit",
            title="Welcome",
            border_style="green",
        )
        # this is really compulsory for displayin it
        self.write_panel(welcome)

    def focus_input(self) -> None:
        """just like dom manipulation"""
        self.query_one("#input-area", Input).focus()
    
    def set_status(self, status: str) -> None:
        """Update the status bar."""
        status_bar = self.query_one("#status-bar", StatusBar)
        status_bar.status = status

    def set_confidence(self, confidence: float) -> None:
        """Update confidence in status bar. """
        status_bar = self.query_one("#status-bar", StatusBar)
        status_bar.sources = confidence

    def set_sources(self, count: int) -> None:
        """Update sources count in status bar"""
        status_bar = self.query_one("#status-bar", StatusBar)
        status_bar.sources = count

    def write(self, message: str, style: str = "") -> None:
        """Write a message to the chat display."""
        chat = self.query_one("#chat-container", RichLog)
        if style:
            chat.write(f"[{style}]{message}[/{style}]")
        else:
            chat.write(message)

    def write_success(self, message: str) -> None:
        """Write a success message"""
        self.write(f" {message}", "green")

    def write_error(self, message: str ) -> None:
        """Write an error message."""
        self.write(f" {message}", "red")

    def write_warning(self, message: str) -> None:
        """Write a warning message"""
        self.write(f" {message}", "yellow")

    def write_info(self, message: str) -> None:
        """Write an info message."""
        self.write(f" {message}", "cyan")

    def write_panel(self, panel: Panel) -> None:
        chat = self.query_one("#chat-container", RichLog)
        chat.write(panel)

    def update_answer_panel(self, answer: str, confidence: float, sources: int) -> None:
        """Update the answer panel"""
        panel = self.query_one("#answer-panel", AnswerPanel)
        panel.update_answer(answer, confidence, sources)

    def on_input_submitted(self, event: Input):
        """Handle user input"""
        query = event.value.strip()
        if not query:
            return

        event.input.value = ""

        # handle commands
        if query.startswith("/"):
            self.handle_command(query)
            return

        # process query
        if not self.ready:
            self.write_warning(" Not ready. No documents loaded.")
            self.write_info(" Run: PersonalRAG ingestion")
            self.focus_input()
            return

        self.write(f"[bold cyan]You: [/bold cyan] {query}")
        self.run_worker(self.process_query(query))
            
    def handle_command(self, command: str) -> None:
        """handle slash commands"""
        cmd = command.lower().strip()

        if cmd in ("/quit", "/exit", "/q"):
            self.exit()

        elif cmd == "/help":
            self.action_show_help()

        elif cmd == "/clear":
            self.action_clear()

        elif cmd == "/sources":
            self.action_show_sources()

        elif cmd == "/status":
            self.show_status()

        else:
            self.write_warning(f"Uknown command: {command}")
            self.write_info("Type /help for available commands")

        self.focus_input()

    async def process_query(self, query: str) -> None:
        """
        Process a query in the background
        
        Why async ?
        - Textual's event loop must keep running
        - pipeline.query() is blocking (CPU + network)
        - asyncio.to_thread runs it back ground thread
        - UI stays responsive
        """
        # asyncronously
        
        try:
            self.set_status(" Retrieving and generating...")

            # run pipeline in thread pool
            result = await asyncio.to_thread(
                self.pipeline.query, 
                query,
            )
            # write answer
            self.write("")
            self.write("[bold green] Assistant: [/bold green]")
            self.write(f"{result.answer}")

            # update the answer panel
            self.update_answer_panel(
                result.answer,
                result.confidence,
                len(result.sources),
            )

            # update metadata
                    # Update metadata
            self.set_confidence(result.confidence)
            
            self.set_sources(len(result.sources))
            
            self.last_sources = result.sources
            
            self.set_status("✅ Ready")
            
            # Summary
            self.write_info(
                f"Confidence: {result.confidence:.0%} | "
                f"Sources: {len(result.sources)}"
            )

            if result.sources:
                self.write_info("Type /sources to see references")
        
        except Exception as e:
            import traceback

            self.write_error(f"Error: {e}")
            self.write_error(f"[red]{traceback.format_exc()} [/red]")
            self.set_status("Error")

        self.focus_input()



    def show_status(self) -> None:
        """Show system status"""
        from pathlib import Path

        lines = []
        lines.append("[bold] System Status [/bold]")
        lines.append("")

        # LLM
        if settings.is_llm_configured:
            lines.append(f" LLM: {settings.default_model}")
        else:
            lines.append(" LLM: Not configured")

        # Embedding
        lines.append(f" Embedding: {settings.embedding_model}")

        # Data dir
        data_path = Path(settings.data_dir)
        if data_path.exists():
            lines.append(f" Data dir: {data_path}")
        else:
            lines.append(f" Data dir: {data_path} (not found)")

        # Vector store
        try:
            store = VectorStore(clear_existing=False)
            lines.append(f" Vector  DB: {store.count()} documents")
        except Exception as e:
            lines.append(f" Vector DB:  {e}")

        self.write_panel(Panel("\n".join(lines), title="Status", border_style="cyan"))

    # defining what will happen if action clear
    def action_clear(self) -> None:
        """Clear the chat"""
        chat = self.query_one("#chat-container", RichLog)
        chat.clear()
        self.show_welcome()
        self.set_confidence(0.0)
        self.set_sources(0)
        self.focus_input()

    def action_show_sources(self) -> None:
        """Show sources for the last answer."""
        if not self.last_sources:
            self.write_warning(" No sources available yet")
            self.focus_input()
            return

        lines = ["[bold] Sources [/bold]", ""]
        for i, source in enumerate(self.last_sources, 1):
            lines.append(f"[cyan]{i}.[/cyan] {source['source']}")
            lines.append(f"     Score: {source['score']:.2%}")
            lines.append(f"     [dim]{source['preview']}[/dim]")
            lines.append("")

        self.write_panel(Panel("\n".join(lines), title="Sources", border_style="cyan"))
        self.focus_input()

    def action_show_help(self) -> None:
        """Show help"""
        help_text = Panel(
            "[bold]Commands:[/bold]\n"
            "   [cyan]/help[/cyan] -- Show this help \n"
            "   [cyan]/sources[/cyan] -- Show sources for last answer \n"
            "   [cyan]/clear[/cyan] -- Clear the chat\n"
            "   [cyan]/status[/cyan] -- Show the system status\n"
            "   [cyan]/quit[/cyan] -- Exit the app\n\n"
            "[bold]Keyboard shortcuts:[/bold]\n"
            "   [cyan]Ctrl+L[/cyan] - Clear\n"
            "   [cyan]Ctrl+S[/cyan] - Show sources\n"
            "   [cyan]Ctrl+H[/cyan] - Help\n"
            "   [cyan]Ctrl+C[/cyan] - Quit",
            title="Help",
            border_style="cyan",
        )
        self.write_panel(help_text)
        self.focus_input()






