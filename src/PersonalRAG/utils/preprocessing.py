
import re
import unicodedata
import typing
from typing import List, Optional, Callable, Dict, Any
import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)
# data class is like a really good container
#dataclass is python decorator that automatically generates common methods
@dataclass
class ProcessedText:
    """
    container for processed text with extracted metadata
    
    Attributes:
        content: Cleaned text 
    """
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    is_valid: bool = True

def clean_text(text: str) -> str:
    """
    Clean text: fix OCR, remove noise, normalize.

    Args:
        text: Raw text from PDF/CSV/TXT

    Returns:
        Cleaned text ready for chunking
    """
    if not text:
        return ""

    # 1. Fix common OCR
    ocr_fixes = {
        'ﬁ': 'fi',
        'ﬂ': 'fl',
        'ﬃ': 'ffi',
        'ﬄ': 'ffl',
        '—': '-',
        '–': '-',
        '…': '...',
        '\u2018': "'",  # Left single quote
        '\u2019': "'",  # Right single quote
        '\u201c': '"',  # Left double quote
        '\u201d': '"',  # Right double quote
        '\u2026': '...',
        '\u00a0': ' ',  # Non-breaking space
        '\x0c': '',     # Form feed / page break
    }
    for old, new in ocr_fixes.items():
        text = text.replace(old, new)

# 2. remove page number lines
        # 2. Remove page number lines (they become metadata)
    text = re.sub(r'(?i)^\s*page\s+\d+\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'(?i)^\s*p\.?\s*\d+\s*$', '', text, flags=re.MULTILINE)
        
# 3. remove extra white space
    text = re.sub(r'\s+', ' ', text).strip()

# what does strip() actually means ?? 
# strip() means that we cut that off
# 4. Normalize unicode 
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('utf-8')

    return text

def extract_metadata(text:str) -> Dict[str, Any]:
    """
    Extract useful metadata from text

    Args:
        text: Raw text (before cleaning)

    Returns:
        Dictionary of extracted metadata

    """
    metadata = {}

    # extract page number
    page_match = re.search(r'(?i)(?:page|p\.?)\s*(\d+)', text)

    # if we have page_match only take the integer sectio
    if page_match:
        metadata['page_number'] = int(page_match.group(1))

    chapter_match = re.search(r'(?i)(?:chapter|section)\s+(\d+|[IVXLCDM]+)\s*[:.]?\s*(.+)?$', text, re.MULTILINE)
    
    if chapter_match:
        metadata['chapter_number'] = chapter_match.group(1)
        if chapter_match.group(2):
            metadata['chapter_title'] = chapter_match.group(2).strip()

    return metadata
    # what is group 0 1 2 
    # group 0 means the entire , group 1 are the chapter number, group 2 means final one chapter title (.+)
    # but why chapter|section is not assigned as because we already stated at fron (?:chapter|section) means that ok this we paring with them but we not saving this

# what does this actuallly means we accept text must be string and also existing metadata if in dict. style or None then we return a ProcessedText object
def preprocess(text: str, existing_metadata: Optional[Dict] = None) -> ProcessedText:

    if not text or not text.strip():
        return ProcessedText(
            content="",
            metadata=existing_metadata or {},
            is_valid=False
        )

    # extract metadata from the raw text
    extracted_metadata = extract_metadata(text)

    # clean the text 
    cleaned = clean_text(text)

    # combine the metadata
    metadata = existing_metadata or {}
    metadata.update(extracted_metadata)

    # check if valid and meaningful conent
    is_valid = len(cleaned) >= 10

    return ProcessedText(
        content=cleaned,
        metadata=metadata,
        is_valid=is_valid
    )

def preprocess_batch(texts: list, metadatas: Optional[list] = None) -> list:
    """Preprocess multiple texts."""
    results = []
    for i, text in enumerate(texts):
        meta = metadatas[i] if metadatas and i < len(metadatas) else None
        results.append(preprocess(text, meta))
    return results
    




