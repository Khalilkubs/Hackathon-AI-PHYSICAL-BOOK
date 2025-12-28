#!/usr/bin/env python3
"""
Demo script for the Document Ingestion and Vector Storage System
Demonstrates the full pipeline functionality
"""

import os
import sys
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

from src.processor import DocumentProcessor

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def demo_single_document_processing():
    """Demo processing a single document"""
    print("\n" + "="*60)
    print("DEMO: Single Document Processing")
    print("="*60)

    # Use a sample documentation URL for the demo
    sample_url = os.getenv('DEPLOY_VERCEL_URL', 'https://httpbin.org/html')  # Fallback URL

    print(f"Processing URL: {sample_url}")

    try:
        # Load configuration
        config = {
            'cohere_api_key': os.getenv('COHERE_API_KEY'),
            'qdrant_url': os.getenv('QDRANT_URL'),
            'qdrant_api_key': os.getenv('QDRANT_API_KEY'),
            'chunk_size': int(os.getenv('CHUNK_SIZE', 512)),
            'chunk_overlap': int(os.getenv('CHUNK_OVERLAP', 50)),
            'request_timeout': int(os.getenv('REQUEST_TIMEOUT', 30)),
            'max_retries': int(os.getenv('MAX_RETRIES', 3)),
        }

        # Validate required environment variables
        required_vars = ['cohere_api_key', 'qdrant_url', 'qdrant_api_key']
        missing_vars = [var for var in required_vars if not config[var]]

        if missing_vars:
            print(f"Missing required environment variables: {', '.join(missing_vars)}")
            print("Please check your .env file.")
            return False

        # Create processor and process document
        processor = DocumentProcessor(config)
        result = processor.process_document(sample_url)

        print(f"\nProcessing result:")
        print(f"  Status: {result['status']}")
        print(f"  Message: {result['message']}")
        print(f"  Processing time: {result['processing_time']:.2f}s")

        if result['status'] == 'success':
            print(f"  Chunks processed: {result.get('chunks_processed', 0)}")
            print(f"  Embeddings generated: {result.get('embeddings_generated', 0)}")
            print(f"  Title: {result.get('title', 'N/A')}")
            print("\n✓ Document processing completed successfully!")
        else:
            print(f"\n⚠ Document processing failed: {result['message']}")

        return result['status'] == 'success'

    except Exception as e:
        print(f"Error during document processing: {e}")
        return False


def demo_multiple_documents_processing():
    """Demo processing multiple documents"""
    print("\n" + "="*60)
    print("DEMO: Multiple Document Processing")
    print("="*60)

    # Use sample URLs for the demo
    sample_urls = [
        os.getenv('DEPLOY_VERCEL_URL', 'https://httpbin.org/html'),
        'https://httpbin.org/json'  # Fallback second URL
    ]

    print(f"Processing URLs: {sample_urls}")

    try:
        # Load configuration
        config = {
            'cohere_api_key': os.getenv('COHERE_API_KEY'),
            'qdrant_url': os.getenv('QDRANT_URL'),
            'qdrant_api_key': os.getenv('QDRANT_API_KEY'),
            'chunk_size': int(os.getenv('CHUNK_SIZE', 512)),
            'chunk_overlap': int(os.getenv('CHUNK_OVERLAP', 50)),
            'request_timeout': int(os.getenv('REQUEST_TIMEOUT', 30)),
            'max_retries': int(os.getenv('MAX_RETRIES', 3)),
        }

        # Validate required environment variables
        required_vars = ['cohere_api_key', 'qdrant_url', 'qdrant_api_key']
        missing_vars = [var for var in required_vars if not config[var]]

        if missing_vars:
            print(f"Missing required environment variables: {', '.join(missing_vars)}")
            print("Please check your .env file.")
            return False

        # Create processor and process multiple documents
        processor = DocumentProcessor(config)
        results = processor.process_multiple_urls(sample_urls)

        print(f"\nBatch processing results:")
        print(f"  Total URLs: {results['total_urls']}")
        print(f"  Successful: {results['successful']}")
        print(f"  Failed: {results['failed']}")
        print(f"  Total processing time: {results['total_processing_time']:.2f}s")

        for url, result in results['batch_results'].items():
            status = "+" if result['status'] == 'success' else "-"
            print(f"  {status} {url}: {result['message'][:50]}...")

        if results['successful'] > 0:
            print("\n+ Multiple document processing completed!")
        else:
            print("\n- No documents were processed successfully.")

        return results['successful'] > 0

    except Exception as e:
        print(f"Error during multiple document processing: {e}")
        return False


def main():
    """Main function to run the demo"""
    print("Document Ingestion and Vector Storage System - Demo")
    print("This demo will showcase the full pipeline functionality.")

    success_count = 0
    total_demos = 2

    # Run single document processing demo
    if demo_single_document_processing():
        success_count += 1

    # Run multiple document processing demo
    if demo_multiple_documents_processing():
        success_count += 1

    print("\n" + "="*60)
    print("DEMO SUMMARY")
    print("="*60)
    print(f"Completed: {success_count}/{total_demos} demos successfully")

    if success_count > 0:
        print("+ Demo completed with some successes!")
        print("\nThe Document Ingestion and Vector Storage System is working correctly.")
        print("You can now use the system with your own URLs.")
    else:
        print("! Some demos failed, but the system components are properly installed.")
        print("Check your environment variables and internet connection.")

    return success_count > 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)