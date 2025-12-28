#!/usr/bin/env python3
"""
Document Ingestion and Vector Storage System
Main entry point for the application
"""

import os
import sys
import argparse
from dotenv import load_dotenv
import logging

from src.processor import DocumentProcessor

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_config():
    """Load and validate configuration from environment variables"""
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
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    return config


def process_single_url(url: str, config: dict):
    """Process a single URL"""
    processor = DocumentProcessor(config)
    result = processor.process_document(url)

    print(f"Processing result for {url}:")
    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")
    print(f"Processing time: {result['processing_time']:.2f}s")

    if result['status'] == 'success':
        print(f"Chunks processed: {result.get('chunks_processed', 0)}")
        print(f"Embeddings generated: {result.get('embeddings_generated', 0)}")
        print(f"Document ID: {result.get('document_id', 'N/A')}")
        print(f"Title: {result.get('title', 'N/A')}")

    return result


def process_multiple_urls(urls_file: str, config: dict):
    """Process multiple URLs from a file"""
    if not os.path.exists(urls_file):
        raise FileNotFoundError(f"URLs file not found: {urls_file}")

    with open(urls_file, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

    processor = DocumentProcessor(config)
    results = processor.process_multiple_urls(urls)

    print(f"Batch processing completed:")
    print(f"Total URLs: {results['total_urls']}")
    print(f"Successful: {results['successful']}")
    print(f"Failed: {results['failed']}")
    print(f"Total processing time: {results['total_processing_time']:.2f}s")

    return results


def main():
    """Main function with command-line interface"""
    parser = argparse.ArgumentParser(
        description="Document Ingestion and Vector Storage System"
    )
    parser.add_argument(
        'url',
        nargs='?',
        help='URL to process (or path to file with URLs if --urls-file is used)'
    )
    parser.add_argument(
        '--urls-file',
        action='store_true',
        help='Process URLs from a file instead of a single URL'
    )
    parser.add_argument(
        '--chunk-size',
        type=int,
        help='Maximum size of text chunks (default: 512)'
    )
    parser.add_argument(
        '--chunk-overlap',
        type=int,
        help='Overlap between consecutive chunks (default: 50)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        config = load_config()

        # Override config with command-line arguments if provided
        if args.chunk_size:
            config['chunk_size'] = args.chunk_size
        if args.chunk_overlap:
            config['chunk_overlap'] = args.chunk_overlap

        logger.info("Configuration loaded successfully")
        logger.info(f"Processing with chunk_size={config['chunk_size']}, chunk_overlap={config['chunk_overlap']}")

        if args.urls_file:
            # Process multiple URLs from file
            if not args.url:
                print("Error: URL argument must be provided when using --urls-file (should be path to URLs file)")
                sys.exit(1)
            result = process_multiple_urls(args.url, config)
        else:
            # Process single URL
            if not args.url:
                print("Error: URL argument is required")
                parser.print_help()
                sys.exit(1)
            result = process_single_url(args.url, config)

        # Exit with appropriate code based on results
        if isinstance(result, dict):
            if result.get('status') == 'failed' or result.get('failed', 0) > 0:
                sys.exit(1)

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error during execution: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()