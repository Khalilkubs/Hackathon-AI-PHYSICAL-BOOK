"""
Implement utility functions for token counting and text processing
Task T007: Implement utility functions for token counting and text processing
"""

import tiktoken
from typing import List
import re


def count_tokens(text: str, model_name: str = "gpt-3.5-turbo") -> int:
    """
    Count the number of tokens in a text using tiktoken
    """
    try:
        encoding = tiktoken.encoding_for_model(model_name)
        tokens = encoding.encode(text)
        return len(tokens)
    except KeyError:
        # Fallback to cl100k_base encoding if model is not recognized
        encoding = tiktoken.get_encoding("cl100k_base")
        tokens = encoding.encode(text)
        return len(tokens)


def estimate_tokens(text: str) -> int:
    """
    Rough estimation of token count (approximately 1 token = 4 characters)
    """
    # A rough estimation: 1 token is approximately 4 characters
    # This is less accurate but doesn't require tiktoken
    return max(1, len(text) // 4)


def clean_text(text: str) -> str:
    """
    Clean text by removing extra whitespace and normalizing
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove leading/trailing whitespace
    text = text.strip()
    return text


def split_text(text: str, chunk_size: int = 512, overlap: int = 50) -> List[str]:
    """
    Split text into chunks of specified size with overlap
    """
    if not text:
        return []

    # Use a simple approach to split text into chunks
    words = text.split()
    chunks = []
    start_idx = 0

    while start_idx < len(words):
        # Determine the end index for the current chunk
        end_idx = start_idx + chunk_size

        # If this is not the first chunk, include overlap
        if start_idx > 0 and overlap > 0:
            start_overlap = max(0, start_idx - overlap)
            current_chunk_words = words[start_overlap:end_idx]
        else:
            current_chunk_words = words[start_idx:end_idx]

        # Join the words back into a string
        chunk_text = ' '.join(current_chunk_words)
        chunks.append(chunk_text)

        # Move to the next chunk, accounting for overlap
        start_idx = end_idx - overlap if overlap > 0 else end_idx

        # If we've reached the end, break
        if end_idx >= len(words):
            break

    return chunks


def truncate_text(text: str, max_length: int = 1000) -> str:
    """
    Truncate text to a maximum length while preserving sentences
    """
    if len(text) <= max_length:
        return text

    # Try to find a sentence boundary near the max length
    truncated = text[:max_length]

    # Find the last sentence ending
    last_sentence = max(
        truncated.rfind('.'),
        truncated.rfind('!'),
        truncated.rfind('?')
    )

    if last_sentence > max_length * 0.8:  # Only truncate at sentence if it's reasonably close
        truncated = truncated[:last_sentence + 1]

    return truncated


def normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace in text (convert various whitespace chars to single spaces)
    """
    # Replace various whitespace characters with single spaces
    text = re.sub(r'\s+', ' ', text)
    return text.strip()