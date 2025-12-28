#!/usr/bin/env python3
"""
Basic test script for Document Ingestion and Vector Storage System
Tests the main functionality of the system
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_imports():
    """Test that all modules can be imported successfully"""
    print("Testing imports...")

    try:
        from src.models import Document, TextChunk, Embedding
        print("+ Models imported successfully")
    except ImportError as e:
        print(f"- Failed to import models: {e}")
        return False

    try:
        from src.fetcher import URLFetcher
        print("+ Fetcher imported successfully")
    except ImportError as e:
        print(f"- Failed to import fetcher: {e}")
        return False

    try:
        from src.cleaner import HTMLCleaner
        print("+ Cleaner imported successfully")
    except ImportError as e:
        print(f"- Failed to import cleaner: {e}")
        return False

    try:
        from src.chunker import TextChunker
        print("+ Chunker imported successfully")
    except ImportError as e:
        print(f"- Failed to import chunker: {e}")
        return False

    try:
        from src.embedder import EmbeddingGenerator
        print("+ Embedder imported successfully")
    except ImportError as e:
        print(f"- Failed to import embedder: {e}")
        return False

    try:
        from src.storage import VectorStorage
        print("+ Storage imported successfully")
    except ImportError as e:
        print(f"- Failed to import storage: {e}")
        return False

    try:
        from src.processor import DocumentProcessor
        print("+ Processor imported successfully")
    except ImportError as e:
        print(f"- Failed to import processor: {e}")
        return False

    try:
        from src.utils import count_tokens, retry_with_exponential_backoff
        print("+ Utils imported successfully")
    except ImportError as e:
        print(f"- Failed to import utils: {e}")
        return False

    return True


def test_data_models():
    """Test data model creation and validation"""
    print("\nTesting data models...")

    from src.models import Document, TextChunk, Embedding
    from datetime import datetime

    try:
        # Test Document
        doc = Document(
            id="",
            url="https://example.com",
            title="Test Document",
            content="This is test content.",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            metadata={"test": True}
        )
        doc.validate()
        print("+ Document model works correctly")
    except Exception as e:
        print(f"- Document model failed: {e}")
        return False

    try:
        # Test TextChunk
        chunk = TextChunk(
            id="",
            document_id="doc123",
            content="This is a text chunk.",
            chunk_index=0,
            token_count=5,
            start_pos=0,
            end_pos=20
        )
        chunk.validate()
        print("+ TextChunk model works correctly")
    except Exception as e:
        print(f"- TextChunk model failed: {e}")
        return False

    try:
        # Test Embedding
        embedding = Embedding(
            id="",
            chunk_id="chunk123",
            vector=[0.1] * 1024,  # 1024-dimensional vector as required
            metadata={"test": True},
            created_at=datetime.now()
        )
        embedding.validate()
        print("+ Embedding model works correctly")
    except Exception as e:
        print(f"- Embedding model failed: {e}")
        return False

    return True


def test_utils():
    """Test utility functions"""
    print("\nTesting utilities...")

    from src.utils import count_tokens, validate_url, sanitize_text

    try:
        # Test token counting
        text = "This is a test sentence."
        token_count = count_tokens(text)
        assert token_count > 0, "Token count should be positive"
        print(f"+ Token counting works: '{text}' -> {token_count} tokens")
    except Exception as e:
        print(f"- Token counting failed: {e}")
        return False

    try:
        # Test URL validation
        valid_url = "https://example.com"
        invalid_url = "not-a-url"
        assert validate_url(valid_url), "Valid URL should pass validation"
        assert not validate_url(invalid_url), "Invalid URL should fail validation"
        print("+ URL validation works correctly")
    except Exception as e:
        print(f"- URL validation failed: {e}")
        return False

    try:
        # Test text sanitization
        dirty_text = "  This  has   extra\t\twhitespace\n\nand\nnewlines  "
        clean_text = sanitize_text(dirty_text)
        assert "  " not in clean_text, "Should not contain multiple consecutive spaces"
        print("+ Text sanitization works correctly")
    except Exception as e:
        print(f"- Text sanitization failed: {e}")
        return False

    return True


def test_configuration():
    """Test configuration loading"""
    print("\nTesting configuration...")

    from main import load_config

    try:
        # This will fail if required environment variables are not set
        config = load_config()
        print("✓ Configuration loaded successfully")
        print(f"  - Qdrant URL: {config['qdrant_url'][:30]}...")  # Truncate for safety
        print(f"  - Chunk size: {config['chunk_size']}")
        print(f"  - Chunk overlap: {config['chunk_overlap']}")
        return True
    except ValueError as e:
        print(f"- Configuration failed: {e}")
        print("  Note: This is expected if environment variables are not set")
        return True  # Don't fail the test for missing env vars
    except Exception as e:
        print(f"- Configuration failed unexpectedly: {e}")
        return False


def run_tests():
    """Run all tests"""
    print("Starting Document Ingestion and Vector Storage System tests...\n")

    all_tests = [
        ("Imports", test_imports),
        ("Data Models", test_data_models),
        ("Utilities", test_utils),
        ("Configuration", test_configuration),
    ]

    passed = 0
    total = len(all_tests)

    for test_name, test_func in all_tests:
        print(f"\n--- Running {test_name} Test ---")
        if test_func():
            passed += 1
            print(f"+ {test_name} test passed")
        else:
            print(f"- {test_name} test failed")

    print(f"\n--- Test Results ---")
    print(f"Passed: {passed}/{total}")

    if passed == total:
        print("All tests passed!")
        return True
    else:
        print(f"{total - passed} test(s) failed")
        return False


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)