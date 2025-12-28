"""
Data model classes for Document Ingestion and Vector Storage System
Task T005: Create data model classes (Document, TextChunk, Embedding) with validation
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime


@dataclass
class Document:
    """Represents a document that has been fetched and processed"""
    id: str  # Unique identifier for the document
    url: str  # Source URL of the document
    title: str  # Title of the document
    content: str  # Raw text content of the document
    processed_content: str  # Cleaned and processed text content
    created_at: datetime  # Timestamp when the document was created
    updated_at: datetime  # Timestamp when the document was last updated
    metadata: Dict[str, str]  # Additional metadata about the document

    def validate(self) -> bool:
        """Validate the document"""
        if not self.id or not self.url or not self.content:
            return False
        if len(self.content.strip()) == 0:
            return False
        return True


@dataclass
class TextChunk:
    """Represents a chunk of text that will be embedded"""
    id: str  # Unique identifier for the chunk
    document_id: str  # ID of the parent document
    content: str  # The actual text content of the chunk
    chunk_index: int  # Position of the chunk in the original document
    token_count: int  # Number of tokens in the chunk
    source_url: str  # Source URL of the original document
    document_title: str  # Title of the original document

    def validate(self) -> bool:
        """Validate the text chunk"""
        if not self.id or not self.document_id or not self.content:
            return False
        if len(self.content.strip()) == 0:
            return False
        if self.token_count < 0:
            return False
        return True


@dataclass
class Embedding:
    """Represents an embedding vector for a text chunk"""
    id: str  # Unique identifier for the embedding
    chunk_id: str  # ID of the text chunk that was embedded
    vector: List[float]  # The embedding vector (list of floats)
    model: str  # Name of the model used to generate the embedding
    created_at: datetime  # Timestamp when the embedding was created
    source_url: str  # Source URL of the original document
    document_title: str  # Title of the original document
    chunk_index: int  # Position of the chunk in the original document

    def validate(self) -> bool:
        """Validate the embedding"""
        if not self.id or not self.chunk_id or not self.vector:
            return False
        if len(self.vector) == 0:
            return False
        if not self.model:
            return False
        return True