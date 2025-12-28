#!/usr/bin/env python3
"""
Sitemap Processor Script for Document Ingestion and Vector Storage System
Processes all URLs from a sitemap.xml file
"""

import os
import sys
from dotenv import load_dotenv
import logging
from typing import List

from src.sitemap_parser import SitemapParser
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


def process_sitemap_urls(sitemap_url: str, config: dict, max_urls: int = None):
    """
    Process all URLs from a sitemap

    Args:
        sitemap_url: URL of the sitemap.xml file
        config: Configuration dictionary
        max_urls: Maximum number of URLs to process (useful for testing)
    """
    logger.info(f"Starting sitemap processing for: {sitemap_url}")

    # Parse the sitemap to get all URLs
    parser = SitemapParser()
    urls = parser.parse_sitemap(sitemap_url)

    if not urls:
        logger.error("No URLs found in sitemap")
        return

    logger.info(f"Found {len(urls)} URLs in sitemap")

    # Limit the number of URLs if max_urls is specified
    if max_urls and max_urls > 0:
        urls = urls[:max_urls]
        logger.info(f"Limiting to first {len(urls)} URLs")

    # Create document processor
    processor = DocumentProcessor(config)

    # Process each URL
    successful = 0
    failed = 0

    for i, url in enumerate(urls, 1):
        logger.info(f"Processing URL {i}/{len(urls)}: {url}")

        try:
            result = processor.process_document(url)

            if result['status'] == 'success':
                logger.info(f"✓ Successfully processed {url}")
                successful += 1
            else:
                logger.error(f"✗ Failed to process {url}: {result['message']}")
                failed += 1

        except Exception as e:
            logger.error(f"✗ Error processing {url}: {str(e)}")
            failed += 1

    logger.info(f"Sitemap processing completed. Successful: {successful}, Failed: {failed}")

    return {
        'total': len(urls),
        'successful': successful,
        'failed': failed,
        'urls_processed': urls
    }


def main():
    """Main function to process sitemap URLs"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Process all URLs from a sitemap.xml file"
    )
    parser.add_argument(
        'sitemap_url',
        help='URL of the sitemap.xml file to process'
    )
    parser.add_argument(
        '--max-urls',
        type=int,
        help='Maximum number of URLs to process (useful for testing)'
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

        # Process the sitemap URLs
        result = process_sitemap_urls(args.sitemap_url, config, args.max_urls)

        print(f"\nSitemap Processing Summary:")
        print(f"Total URLs processed: {result['total']}")
        print(f"Successful: {result['successful']}")
        print(f"Failed: {result['failed']}")

        if result['failed'] == 0:
            logger.info("All URLs processed successfully!")
            sys.exit(0)
        else:
            logger.warning(f"{result['failed']} URLs failed to process")
            sys.exit(1)

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error during execution: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()