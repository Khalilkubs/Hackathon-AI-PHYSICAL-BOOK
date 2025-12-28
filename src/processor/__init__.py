"""
Document Processor Module for Document Ingestion and Vector Storage System
Orchestrates the full ingestion pipeline: Fetch → Clean → Chunk → Embed → Store
"""

from src.fetcher import URLFetcher
from src.cleaner import HTMLCleaner
from src.chunker import TextChunker
from src.embedder import EmbeddingGenerator
from src.storage import VectorStorage
from src.models import Document
import logging
import time
from datetime import datetime
from typing import List, Optional

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """
    Class to orchestrate the full document ingestion pipeline
    """

    def __init__(self, config: dict):
        """
        Initialize the document processor with configuration

        Args:
            config: Configuration dictionary with API keys and settings
        """
        self.config = config

        # Initialize components
        self.fetcher = URLFetcher(
            timeout=config['request_timeout'],
            max_retries=config['max_retries'],
            use_selenium=True  # Enable Selenium for JavaScript rendering
        )
        self.cleaner = HTMLCleaner()
        self.chunker = TextChunker(
            max_chunk_size=config['chunk_size'],
            overlap_size=config['chunk_overlap']
        )
        self.embedder = EmbeddingGenerator(api_key=config['cohere_api_key'])
        self.storage = VectorStorage(
            url=config['qdrant_url'],
            api_key=config['qdrant_api_key']
        )

        # Create collection if it doesn't exist - using default size for now, will update as needed
        self.storage.create_collection()

    def process_document(self, url: str) -> dict:
        """
        Process a single document through the full pipeline

        Args:
            url: The URL to process

        Returns:
            Dictionary with processing results
        """
        start_time = time.time()
        logger.info(f"Starting processing for URL: {url}")

        try:
            # Step 1: Fetch content
            html_content = self.fetcher.fetch_url(url)
            if not html_content:
                logger.error(f"Failed to fetch content from {url}")
                return {
                    "status": "failed",
                    "message": f"Failed to fetch content from {url}",
                    "url": url,
                    "processing_time": time.time() - start_time
                }

            # Step 2: Extract title
            title = self.cleaner.extract_title(html_content)

            # Step 3: Clean HTML content
            cleaned_content = self.cleaner.clean_html(html_content, url)
            if not cleaned_content:
                logger.error(f"Failed to clean HTML content from {url}")
                return {
                    "status": "failed",
                    "message": f"Failed to clean HTML content from {url}",
                    "url": url,
                    "processing_time": time.time() - start_time
                }

            # Step 4: Create document object
            document = Document(
                id="",
                url=url,
                title=title,
                content=cleaned_content,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                metadata={"source": "docusaurus", "processed_at": datetime.now().isoformat()}
            )
            document.validate()

            # Step 5: Chunk the text
            chunks = self.chunker.chunk_text(cleaned_content, document.id)
            if not chunks:
                logger.error(f"No chunks created for {url}")
                return {
                    "status": "failed",
                    "message": f"No text chunks created from content at {url}",
                    "url": url,
                    "processing_time": time.time() - start_time
                }

            logger.info(f"Created {len(chunks)} text chunks for {url}")

            # Step 6: Generate embeddings
            embeddings = self.embedder.generate_embeddings(chunks, document.url, document.title)
            if not embeddings:
                logger.error(f"No embeddings generated for {url}")
                return {
                    "status": "failed",
                    "message": f"No embeddings generated for content at {url}",
                    "url": url,
                    "processing_time": time.time() - start_time,
                    "chunks_processed": len(chunks)
                }

            logger.info(f"Generated {len(embeddings)} embeddings for {url}")

            # Step 7: Store embeddings
            storage_success = self.storage.store_embeddings(embeddings)
            if not storage_success:
                # If storage failed due to dimension mismatch, try to recreate the collection
                first_embedding_size = len(embeddings[0].vector) if embeddings else 0
                if first_embedding_size > 0:
                    logger.info(f"Attempting to recreate collection with {first_embedding_size}-dimension vectors")
                    if self.storage.recreate_collection(vector_size=first_embedding_size):
                        # Try storing again with the new collection
                        storage_success = self.storage.store_embeddings(embeddings)

                if not storage_success:
                    logger.error(f"Failed to store embeddings for {url}")
                    return {
                        "status": "failed",
                        "message": f"Failed to store embeddings in vector database for {url}",
                        "url": url,
                        "processing_time": time.time() - start_time,
                        "chunks_processed": len(chunks),
                        "embeddings_generated": len(embeddings)
                    }

            # Success case
            processing_time = time.time() - start_time
            logger.info(f"Successfully processed {url} in {processing_time:.2f}s")
            return {
                "status": "success",
                "message": f"Successfully processed and stored embeddings for {url}",
                "url": url,
                "processing_time": processing_time,
                "chunks_processed": len(chunks),
                "embeddings_generated": len(embeddings),
                "document_id": document.id,
                "title": title
            }

        except Exception as e:
            logger.error(f"Error processing document {url}: {str(e)}")
            return {
                "status": "failed",
                "message": f"Error processing document {url}: {str(e)}",
                "url": url,
                "processing_time": time.time() - start_time
            }

    def process_multiple_urls(self, urls: List[str]) -> dict:
        """
        Process multiple URLs through the pipeline

        Args:
            urls: List of URLs to process

        Returns:
            Dictionary with results for each URL
        """
        results = {}
        start_time = time.time()

        logger.info(f"Starting batch processing of {len(urls)} URLs")

        for i, url in enumerate(urls, 1):
            logger.info(f"Processing URL {i}/{len(urls)}: {url}")
            result = self.process_document(url)
            results[url] = result

            # Log progress
            if result['status'] == 'success':
                logger.info(f"+ Completed {url} successfully")
            else:
                logger.warning(f"- Failed {url}: {result['message']}")

        total_time = time.time() - start_time
        logger.info(f"Completed batch processing of {len(urls)} URLs in {total_time:.2f}s")

        return {
            "batch_results": results,
            "total_processing_time": total_time,
            "total_urls": len(urls),
            "successful": sum(1 for r in results.values() if r['status'] == 'success'),
            "failed": sum(1 for r in results.values() if r['status'] == 'failed')
        }