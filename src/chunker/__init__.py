"""
Text Chunker Module for Document Ingestion and Vector Storage System
Splits cleaned text into appropriately sized chunks with overlap functionality
"""

import re
from typing import List, Tuple
from src.models import TextChunk
from uuid import uuid4
import logging

logger = logging.getLogger(__name__)


class TextChunker:
    """
    Class to split text into appropriately sized chunks with overlap functionality
    """

    def __init__(self, max_chunk_size: int = 512, overlap_size: int = 50):
        """
        Initialize the text chunker

        Args:
            max_chunk_size: Maximum size of text chunks (default: 512 tokens)
            overlap_size: Overlap between consecutive chunks (default: 50 tokens)
        """
        self.max_chunk_size = max_chunk_size
        self.overlap_size = overlap_size

    def chunk_text(self, text: str, document_id: str) -> List[TextChunk]:
        """
        Split text into chunks with overlap functionality

        Args:
            text: The text to chunk
            document_id: ID of the parent document

        Returns:
            List of TextChunk objects
        """
        if not text:
            return []

        # For simplicity, we'll split by sentences first, then by max chunk size
        # In a real implementation, we'd use tokenization to count actual tokens
        sentences = self._split_into_sentences(text)
        chunks = []
        current_chunk = ""
        start_pos = 0
        chunk_index = 0

        for i, sentence in enumerate(sentences):
            # Check if adding this sentence would exceed the chunk size
            test_chunk = current_chunk + " " + sentence if current_chunk else sentence

            if self._count_tokens(test_chunk) <= self.max_chunk_size:
                current_chunk = test_chunk
            else:
                # If the current chunk is empty but the sentence is too long,
                # we need to split the sentence
                if not current_chunk:
                    # Split the long sentence into smaller parts
                    sentence_chunks = self._split_long_sentence(sentence)
                    for part in sentence_chunks[:-1]:  # Add all but the last part as complete chunks
                        chunk_text = part.strip()
                        if chunk_text:
                            chunk = self._create_text_chunk(
                                chunk_text, document_id, chunk_index, start_pos
                            )
                            chunks.append(chunk)
                            start_pos += len(chunk_text)
                            chunk_index += 1
                    # The last part becomes the current chunk
                    current_chunk = sentence_chunks[-1].strip()
                else:
                    # Current chunk is not empty and adding the sentence would exceed limits
                    # Save the current chunk
                    chunk = self._create_text_chunk(
                        current_chunk, document_id, chunk_index, start_pos
                    )
                    chunks.append(chunk)
                    start_pos += len(current_chunk)

                    # Handle overlap
                    overlap_text = self._get_overlap_text(current_chunk, self.overlap_size)
                    current_chunk = overlap_text + " " + sentence if overlap_text else sentence
                    chunk_index += 1

        # Add the last chunk if it's not empty
        if current_chunk.strip():
            chunk = self._create_text_chunk(
                current_chunk.strip(), document_id, chunk_index, start_pos
            )
            chunks.append(chunk)

        logger.info(f"Text chunked into {len(chunks)} chunks")
        return chunks

    def _split_into_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences

        Args:
            text: The text to split

        Returns:
            List of sentences
        """
        # Split text into sentences using common sentence terminators
        # This is a simple approach - in practice, you might want to use a more sophisticated NLP library
        sentences = re.split(r'[.!?]+\s+', text)
        # Clean up the sentences
        sentences = [s.strip() for s in sentences if s.strip()]
        return sentences

    def _split_long_sentence(self, sentence: str) -> List[str]:
        """
        Split a sentence that's too long into smaller chunks

        Args:
            sentence: The long sentence to split

        Returns:
            List of sentence parts
        """
        words = sentence.split()
        parts = []
        current_part = []

        for word in words:
            test_part = " ".join(current_part + [word])
            if self._count_tokens(test_part) <= self.max_chunk_size:
                current_part.append(word)
            else:
                if current_part:  # If there are words in the current part, save it
                    parts.append(" ".join(current_part))
                    current_part = [word]  # Start new part with current word
                else:
                    # If even a single word is too long, we'll include it anyway
                    # This shouldn't happen in practice with reasonable settings
                    parts.append(word)
                    current_part = []

        if current_part:  # Add the last part if there are words left
            parts.append(" ".join(current_part))

        return parts

    def _get_overlap_text(self, text: str, overlap_size: int) -> str:
        """
        Get the last few tokens from text for overlap

        Args:
            text: The text to get overlap from
            overlap_size: Number of tokens for overlap

        Returns:
            Overlap text
        """
        words = text.split()
        if len(words) <= overlap_size:
            return text

        # Take the last overlap_size words
        overlap_words = words[-overlap_size:]
        overlap_text = " ".join(overlap_words)

        return overlap_text

    def _count_tokens(self, text: str) -> int:
        """
        Count approximate number of tokens in text
        Note: This is a simple approximation. For accurate token counting,
        you would use a tokenizer like tiktoken.

        Args:
            text: The text to count tokens for

        Returns:
            Approximate number of tokens
        """
        # Simple approximation: count words
        # In a real implementation, use tiktoken for accurate token counting
        if not text:
            return 0
        # Split by whitespace and punctuation to get a more accurate count
        tokens = re.findall(r'\b\w+\b|[^\w\s]', text)
        return len(tokens)

    def _create_text_chunk(self, content: str, document_id: str, chunk_index: int, start_pos: int) -> TextChunk:
        """
        Create a TextChunk object

        Args:
            content: The chunk content
            document_id: ID of the parent document
            chunk_index: Index of this chunk in the document
            start_pos: Starting position of this chunk in the original document

        Returns:
            TextChunk object
        """
        token_count = self._count_tokens(content)
        end_pos = start_pos + len(content)

        chunk = TextChunk(
            id=str(uuid4()),
            document_id=document_id,
            content=content,
            chunk_index=chunk_index,
            token_count=token_count,
            start_pos=start_pos,
            end_pos=end_pos
        )

        # Validate the chunk
        try:
            chunk.validate()
        except ValueError as e:
            logger.warning(f"Chunk validation failed: {e}")
            # In a real implementation, you might want to handle this differently
            # For now, we'll still return the chunk but log the warning

        return chunk