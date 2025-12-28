"""
Implement input validation and sanitization for URLs and content
Task T009: Implement input validation and sanitization for URLs and content
"""

import re
from typing import Optional, Union
from urllib.parse import urlparse
import html
import bleach


def validate_url(url: str) -> bool:
    """
    Validate if a string is a properly formatted URL
    """
    if not url or not isinstance(url, str):
        return False

    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def sanitize_url(url: str) -> Optional[str]:
    """
    Sanitize a URL by removing potentially harmful components
    """
    if not url:
        return None

    # Remove any fragments and query parameters that might contain malicious content
    parsed = urlparse(url)

    # Only allow http and https schemes
    if parsed.scheme not in ['http', 'https']:
        return None

    # Reconstruct the URL without fragments that might contain scripts
    sanitized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

    # Additional sanitization to prevent potential injection
    sanitized = sanitized.replace(' ', '%20')  # Encode spaces
    sanitized = sanitized.replace('<', '%3C')  # Encode potential script tags
    sanitized = sanitized.replace('>', '%3E')

    return sanitized


def validate_content(content: str, max_length: int = 1000000) -> bool:
    """
    Validate content length and basic format
    """
    if not content or not isinstance(content, str):
        return False

    if len(content) > max_length:
        return False

    # Check for basic text content (not just whitespace)
    if not content.strip():
        return False

    return True


def sanitize_content(content: str, allowed_tags: Optional[list] = None) -> str:
    """
    Sanitize content by removing potentially harmful HTML tags and attributes
    """
    if not content:
        return ""

    if allowed_tags is None:
        allowed_tags = []  # No HTML tags allowed by default

    # First, decode any HTML entities
    content = html.unescape(content)

    # Use bleach to sanitize HTML content
    sanitized = bleach.clean(
        content,
        tags=allowed_tags,
        attributes={},
        strip=True
    )

    return sanitized


def validate_document_id(doc_id: str) -> bool:
    """
    Validate document ID format (alphanumeric with hyphens and underscores)
    """
    if not doc_id or not isinstance(doc_id, str):
        return False

    # Allow alphanumeric, hyphens, and underscores only
    pattern = r'^[a-zA-Z0-9_-]+$'
    return bool(re.match(pattern, doc_id))


def sanitize_text(text: str) -> str:
    """
    Sanitize plain text by removing potentially harmful characters
    """
    if not text:
        return ""

    # Remove control characters except common whitespace
    sanitized = ''.join(char for char in text if ord(char) >= 32 or char in '\n\r\t')

    # Remove potential script tags or other harmful patterns
    sanitized = re.sub(r'<script[^>]*>.*?</script>', '', sanitized, flags=re.IGNORECASE | re.DOTALL)
    sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r'vbscript:', '', sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r'on\w+\s*=', '', sanitized, flags=re.IGNORECASE)

    return sanitized.strip()


def validate_chunk_size(chunk_size: Union[int, str]) -> bool:
    """
    Validate chunk size is within acceptable range
    """
    try:
        size = int(chunk_size)
        return 1 <= size <= 10000  # Reasonable range for text chunks
    except (ValueError, TypeError):
        return False


def validate_overlap(overlap: Union[int, str]) -> bool:
    """
    Validate overlap size is within acceptable range
    """
    try:
        size = int(overlap)
        return 0 <= size <= 1000  # Reasonable range for overlap
    except (ValueError, TypeError):
        return False


def validate_similarity_threshold(threshold: Union[float, str]) -> bool:
    """
    Validate similarity threshold is between 0 and 1
    """
    try:
        value = float(threshold)
        return 0.0 <= value <= 1.0
    except (ValueError, TypeError):
        return False


def is_safe_filename(filename: str) -> bool:
    """
    Check if a filename is safe to use
    """
    if not filename:
        return False

    # Check for dangerous patterns
    dangerous_patterns = [
        r'\.\./',  # Directory traversal
        r'\.\.\\',  # Directory traversal (Windows)
        r'[<>:"/\\|?*]',  # Invalid filename characters
    ]

    for pattern in dangerous_patterns:
        if re.search(pattern, filename):
            return False

    return True


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing dangerous characters
    """
    if not filename:
        return ""

    # Remove dangerous characters and replace with underscore
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)

    # Remove directory traversal attempts
    sanitized = sanitized.replace('../', '_')
    sanitized = sanitized.replace('..\\', '_')

    return sanitized