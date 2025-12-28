"""
Utility functions for Document Ingestion and Vector Storage System
"""

import re
import time
from typing import Optional, Callable, Any
import logging

logger = logging.getLogger(__name__)


def count_tokens(text: str) -> int:
    """
    Count approximate number of tokens in text
    Note: This is a simple approximation. For accurate token counting,
    you would use a tokenizer like tiktoken.

    Args:
        text: The text to count tokens for

    Returns:
        Approximate number of tokens
    """
    if not text:
        return 0

    # Split by whitespace and common punctuation to get a more accurate count
    # This is more accurate than just splitting by spaces
    tokens = re.findall(r'\b\w+\b|[^\w\s]', text)
    return len(tokens)


def validate_url(url: str) -> bool:
    """
    Validate if the URL is properly formatted

    Args:
        url: The URL to validate

    Returns:
        True if the URL is valid, False otherwise
    """
    from urllib.parse import urlparse

    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def sanitize_text(text: str) -> str:
    """
    Sanitize text by removing potentially problematic characters

    Args:
        text: The text to sanitize

    Returns:
        Sanitized text
    """
    if not text:
        return text

    # Remove null bytes and other potentially problematic characters
    sanitized = text.replace('\x00', '')  # Remove null bytes
    sanitized = sanitized.replace('\r\n', '\n')  # Normalize line endings
    sanitized = sanitized.replace('\r', '\n')  # Normalize line endings

    # Remove extra whitespace while preserving sentence structure
    sanitized = re.sub(r'[ \t]+', ' ', sanitized)  # Multiple spaces/tabs to single space
    sanitized = re.sub(r'\n\s*\n', '\n\n', sanitized)  # Multiple newlines to max 2

    return sanitized.strip()


def extract_urls_from_text(text: str) -> list:
    """
    Extract URLs from text using regex

    Args:
        text: The text to extract URLs from

    Returns:
        List of URLs found in the text
    """
    # Regex pattern to match URLs
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    urls = re.findall(url_pattern, text)
    return urls


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length

    Args:
        text: The text to truncate
        max_length: Maximum length of the text
        suffix: Suffix to add to truncated text

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text

    # Make sure we don't cut in the middle of a word if possible
    truncated = text[:max_length - len(suffix)]
    last_space = truncated.rfind(' ')

    if last_space > max_length * 0.8:  # Only if the last space is reasonably close
        truncated = truncated[:last_space]

    return truncated + suffix


def retry_with_exponential_backoff(
    func: Callable,
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exceptions: tuple = (Exception,)
) -> Any:
    """
    Execute a function with exponential backoff retry logic

    Args:
        func: Function to execute
        max_retries: Maximum number of retry attempts
        base_delay: Base delay in seconds (will be multiplied by 2^attempt)
        max_delay: Maximum delay in seconds
        exceptions: Tuple of exceptions to catch for retries

    Returns:
        Result of the function call

    Raises:
        The last exception if all retries fail
    """
    for attempt in range(max_retries + 1):
        try:
            return func()
        except exceptions as e:
            if attempt == max_retries:
                logger.error(f"Function failed after {max_retries} retries: {e}")
                raise e

            # Calculate delay with exponential backoff
            delay = min(base_delay * (2 ** attempt), max_delay)
            logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay:.2f}s...")
            time.sleep(delay)

    # This line should never be reached due to the return in the loop
    # but added for type checker
    raise Exception("Retry logic error")