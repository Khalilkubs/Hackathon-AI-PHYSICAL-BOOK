"""
Data models for the Document Ingestion and Vector Storage System
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional
from uuid import uuid4


@dataclass
class Document:
    """
    Represents a source document from a Docusaurus URL

    Fields:
    - id: string (unique identifier, auto-generated)
    - url: string (source URL of the document)
    - title: string (document title extracted from HTML)
    - content: string (full cleaned text content)
    - created_at: datetime (timestamp of ingestion)
    - updated_at: datetime (timestamp of last update)
    - metadata: dict (additional page metadata like author, tags, etc.)
    """
    id: str
    url: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, any]

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid4())
        if not self.created_at:
            self.created_at = datetime.now()
        if not self.updated_at:
            self.updated_at = datetime.now()

    def validate(self):
        """Validate the document according to business rules"""
        errors = []

        if not self.url or not isinstance(self.url, str):
            errors.append("URL must be a valid string")

        if not self.title or not isinstance(self.title, str):
            errors.append("Title must be a valid string")

        if not self.content or not isinstance(self.content, str):
            errors.append("Content must be a non-empty string")

        if errors:
            raise ValueError(f"Document validation failed: {', '.join(errors)}")


@dataclass
class TextChunk:
    """
    Represents a segment of processed text that will be converted to an embedding

    Fields:
    - id: string (unique identifier, auto-generated)
    - document_id: string (foreign key reference to Document.id)
    - content: string (chunked text content)
    - chunk_index: integer (sequential position in document)
    - token_count: integer (number of tokens in chunk)
    - start_pos: integer (starting position in original document)
    - end_pos: integer (ending position in original document)
    """
    id: str
    document_id: str
    content: str
    chunk_index: int
    token_count: int
    start_pos: int
    end_pos: int

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid4())

    def validate(self):
        """Validate the text chunk according to business rules"""
        errors = []

        if not self.content or not isinstance(self.content, str):
            errors.append("Content must be a non-empty string")

        if self.chunk_index < 0:
            errors.append("Chunk index must be non-negative")

        if self.token_count < 0:
            errors.append("Token count must be non-negative")

        if self.start_pos < 0 or self.end_pos < 0 or self.start_pos > self.end_pos:
            errors.append("Invalid position range")

        # Chunk size validation (max 512 tokens as per plan)
        if self.token_count > 512:
            errors.append(f"Chunk token count ({self.token_count}) exceeds maximum limit of 512")

        if errors:
            raise ValueError(f"TextChunk validation failed: {', '.join(errors)}")


@dataclass
class Embedding:
    """
    Vector representation of a text chunk, stored with metadata in the vector database

    Fields:
    - id: string (unique identifier, auto-generated)
    - chunk_id: string (foreign key reference to Text Chunk.id)
    - vector: list[float] (embedding vector, 1024-dimensional for Cohere)
    - metadata: dict (additional metadata including source URL, document title, chunk index)
    - created_at: datetime (timestamp of embedding generation)
    """
    id: str
    chunk_id: str
    vector: List[float]
    metadata: Dict[str, any]
    created_at: datetime

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid4())
        if not self.created_at:
            self.created_at = datetime.now()

    def validate(self):
        """Validate the embedding according to business rules"""
        errors = []

        if not self.chunk_id:
            errors.append("Chunk ID is required")

        if not self.vector or not isinstance(self.vector, list):
            errors.append("Vector must be a valid list")
        elif len(self.vector) == 0:
            errors.append("Vector must have at least 1 dimension")

        if not all(isinstance(v, (int, float)) and not (v != v) for v in self.vector):  # Check for NaN values
            errors.append("Vector must contain only valid numbers (no NaN or infinity)")

        if errors:
            raise ValueError(f"Embedding validation failed: {', '.join(errors)}")