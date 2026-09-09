"""DOCUMENT PROCESSING WITH DEDUPLICATION AND CHUNKING"""
import hashlib
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

from langchain_community.document_loaders import PyMuPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from PersonalRAG.utils.preprocessing import preprocess
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
            try:
                loader = PyMuPDFLoader(str(pdf_file))
                docs = loader.load()
                logger.debug(f"Loaded {len(docs)} pages from {pdf_file.name}")

                for doc in docs:
                    # preprocessing happen here
                    result = preprocess(
                        doc.page_content,
                        existing_metadata={
                            'source': pdf_file.name,
                            'source_path': str(pdf_file),
                        }
                    )
                    
                    if not result.is_valid:
                        logger.debug(f"skipping page too short mate ")
                        continue

                    # update document
                    doc.page_content = result.content
                    doc.metadata.update(result.metadata)

                    # this is also very crucial in order to give the exact place of the documentation
                    content_hash = hashlib.md5(
                        doc.page_content.encode()
                    ).hexdigest()

                    if content_hash in self.seen_hashes:
                        self.stats['duplicates_skipped'] += 1
                        continue

                    self.seen_hashes.add(content_hash)
                    doc.metadata['content_hash'] = content_hash
                    self.documents.append(doc)
                    self.stats['pages_processed'] += 1

            except Exception as e:
                logger.error(f"Error processing {pdf_file.name}: {e}")

        logger.info(f"Loaded {self.stats['pages_processed']} unique pages")

        return self.documents

    # FOR CSV DOCUMENT READING
    def load_csv(self, csv_dir: Optional[str] = None ) -> List[Document]:
        dir_path = Path(csv_dir) if csv_dir else self.data_dir / "csv"

        if not dir_path.exists():
            logger.error(f"data path {dir_path} doesnt exist")
            return []

        import pandas as pd

        csv_files = list(dir_path.glob("**/*.csv"))
        logger.info(f" found the {len(csv_files)} CSV files")

        for csv_file in csv_files:
            try:
                df = pd.read_csv(csv_file)

                for idx, row in df.iterrows():
                    # converting row to text
                    row_text = f"Row {idx + 1}:\n"
                    for col in df.columns:
                        row_text += f"  {col}: {row[col]}\n"

                    result = preprocess(
                        row_text,
                        existing_metadata={
                            'source': csv_file.name,
                            'source_path': str(csv_file),
                            'row_index': idx,
                        }
                    )

                    if not result.is_valid:
                        continue

                    # create document
                    doc = Document(
                        page_content=result.content,
                        metadata=result.metadata 
                    )

                    content_hash = hashlib.md5(
                        doc.page_content.encode()
                    ).hexdigest()

                    if content_hash in self.seen_hashes:
                        self.stats['duplicates_skipped'] += 1
                        continue

                    self.seen_hashes.add(content_hash)
                    doc.metadata['content_hash'] = content_hash
                    self.document.append(doc)
                    self.stats['pages_processed'] += 1

            except Exception as e:
                loggger.error(f"Erro processing {csv_file.name}: {e}")

        return self.documents

    def load_text_files(self, text_dir: Optional[str] = None) -> List[Document]:
        """Load text files."""
        dir_path = Path(text_dir) if text_dir else self.data_dir / "txt"
        
        if not dir_path.exists():
            return []
        
        text_files = list(dir_path.glob("**/*.txt"))
        logger.info(f"Found {len(text_files)} text files")
        
        for text_file in text_files:
            try:
                loader = TextLoader(str(text_file), encoding="utf-8")
                docs = loader.load()
                
                for doc in docs:
                    # 🔥 PREPROCESS HERE
                    result = preprocess(
                        doc.page_content,
                        existing_metadata={
                            'source': text_file.name,
                            'source_path': str(text_file),
                        }
                    )
                    
                    if not result.is_valid:
                        continue
                    
                    doc.page_content = result.content
                    doc.metadata.update(result.metadata)
                    
                    content_hash = hashlib.md5(
                        doc.page_content.encode()
                    ).hexdigest()
                    
                    if content_hash in self.seen_hashes:
                        self.stats['duplicates_skipped'] += 1
                        continue
                    
                    self.seen_hashes.add(content_hash)
                    doc.metadata['content_hash'] = content_hash
                    self.documents.append(doc)
                    self.stats['pages_processed'] += 1
                    
            except Exception as e:
                logger.error(f"Error processing {text_file.name}: {e}")
        
        return self.documents

    # chunking document

