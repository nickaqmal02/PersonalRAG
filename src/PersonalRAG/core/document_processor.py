"""DOCUMENT PROCESSING WITH DEDUPLICATION AND CHUNKING"""
import hashlib
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

from langchain_community.document_loaders import PyMuPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# declaring our logger
# but we use another approach which is declaring 
# logger in one file which is configuration file
logger = logging.getLogger(__name__)

class DocumentProcessor:

    def __init__(
        self,
        data_dir: str = "./data",
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    );
        self.data_dir = Path(data_dir)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.seen_hashes: set = set()
        self.documents: List[Document] = []
        self.stats = {
            'files_processed': 0,
            'pages_processed': 0,
            'duplicates_skipped': 0,
            'chunks_created': 0,
        }

    def load_pdfs(self, pdf_dir: Optional[str] = None) -> List[Document]:
        """load and process all pdfs files"""
        dir_path = Path(pdf_dir) if pdf_dir else self.data_dir / "pdf"

        if not dir_path.exists():
            logger.warning(f"PDF directory not found: {dir_path}")
            return []

        pdf_files = list (dir_path.glob("**/*.pdf"))

        if not pdf_files:
            logger.warning(f"No PDF FILES found in {dir_path}")
            return []

        logger.info(f"Found {len(pdf_files)} PDF files")
        self.stats['files_processed'] = len(pdf_files)

        for pdf_file in pdf_files:

