"""
This core of application settings - loads from environment variables
every config. lives here
"""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pathlib import Path

# get project root (2 levels up from config/settings.py)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
ENV_FILE = PROJECT_ROOT / ".env"


class Settings(BaseSettings):
    """
    Application settings loaded from .env file.

    All values can be overridden via environment variables.
    """

    # =========================================
    # LLM CONFIGURATION
    # =========================================
    groq_api_key: Optional[str] = Field(
        default=None,
        alias="GROQ_API_KEY",
        description="Groq API key for LLM access",
    )
    default_model: str = Field(
        "llama-3.3-70b-versatile",
        env="DEFAULT_MODEL",
        description="Default LLM model name",
    )
    temperature: float = Field(
        0.1,
        env="DEFAULT_MODEL",
        ge=0.0,
        le=1.0,
        description="LLM sampling temperature (0=deterministic, 1=creative",
    )
    max_tokens: int = Field(
        1024,
        env="MAX_TOKENS",
        ge=1,
        le=8192,
        description="Maximum response length in tokens",
    )
# ╔════════════════════════════════════════════╗ 
# ║             RAG CONFIGURATION              ║ 
# ╚════════════════════════════════════════════╝ 
# ge means greater than or equal to
# le means  less than or equal to
    chunk_size: int = Field(
        1000,
        env="CHUNK_SIZE",
        ge=100,
        le=4000,
        description="Size of document chunks"
    )
    chunk_overlap: int = Field(
        200,
        env="CHUNK_OVERLAP",
        ge=0,
        le=1000,
        description="Overlap between chunks",
    )
    top_k: int = Field(
        5,
        env="TOP_K",
        ge=1,
        le=20,
        description="Numer of documents to retrieve",
    )
    score_threshold: float = Field(
        0.2,
        env="SCORE_THRESHOLD",
        ge=0.0,
        le=1.0,
        description="Minimum similarity score for retrieval",
    )

# ╔════════════════════════════════════════════╗ 
# ║                   PATHS                    ║ 
# ╚════════════════════════════════════════════╝ 
    data_dir: str = Field(
        "./data",
        env="DATA_DIR",
        description="main directory for our storage",
    )
    vector_store_dir: str = Field(
        "./data/vector_store",
        env="VECTOR_STORE_DIR",
        description="Directory for ChromaDB storage",
    )


# ╔════════════════════════════════════════════╗ 
# ║                 EMBEDDDING                 ║ 
# ╚════════════════════════════════════════════╝ 
    embedding_model: str = Field(
        "all-MiniLM-L6-v2",
        env="EMBEDDDING_MODEL",
        description="SentenceTransformer model for embeddings",
    )


# ╔════════════════════════════════════════════╗ 
# ║                  LOGGING                   ║ 
# ╚════════════════════════════════════════════╝ 
    log_level: str = Field(
        "INFO",
        env="LOG_LEVEL",
        description="Logging level (DEBUG, INFO, WARNING, ERROR)",
    )


# ╔════════════════════════════════════════════╗ 
# ║              PYDANTIC CONFIG               ║ 
# ╚════════════════════════════════════════════╝ 
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

# ╔════════════════════════════════════════════╗ 
# ║             HELPER PROPERTIES              ║ 
# ╚════════════════════════════════════════════╝ 
    @property
    def is_llm_configured(self) -> bool:
        """check if llm is ready to use"""
        return bool(self.groq_api_key)

    @property
    def vector_store_path(self) -> str:
        """Get full vector store path"""
        return self.vector_store_dir

# ╔════════════════════════════════════════════╗ 
# ║              GLOBAL INSTANCE               ║ 
# ╚════════════════════════════════════════════╝ 
settings = Settings()

