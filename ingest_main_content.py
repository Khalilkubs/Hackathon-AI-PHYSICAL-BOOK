#!/usr/bin/env python3
"""
Targeted Ingestion Script for Main Book Content
This script focuses only on the core lesson content to avoid duplication
"""
import os
import requests
from bs4 import BeautifulSoup
import time
from typing import List, Dict, Optional
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct
import cohere
import logging
import uuid
from urllib.parse import urljoin, urlparse
import re

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TargetedBookIngestor:
    def __init__(self):
        # Initialize Cohere client
        self.cohere_client = cohere.Client(os.getenv('COHERE_API_KEY'))

        # Initialize Qdrant client
        self.qdrant_client = QdrantClient(
            url=os.getenv('QDRANT_URL'),
            api_key=os.getenv('QDRANT_API_KEY'),
            https=True
        )

        self.collection_name = os.getenv('QDRANT_COLLECTION_NAME', 'document_embeddings')
        self.model = "embed-multilingual-v2.0"  # 768 dimensions to match existing

        # Create headers to mimic a real browser
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Verify Qdrant connection only
        self._verify_qdrant_connection()

    def _verify_qdrant_connection(self):
        """Verify that Qdrant is accessible"""
        logger.info("Verifying Qdrant connection...")
        try:
            # Try to access Qdrant - if collection doesn't exist, that's fine
            try:
                self.qdrant_client.get_collection(self.collection_name)
                logger.info("✅ Qdrant connection verified, collection exists")
            except:
                logger.info("✅ Qdrant connection verified, collection will be created")
        except Exception as e:
            logger.error(f"❌ Qdrant connection failed: {e}")
            raise

    def _extract_content_from_url(self, url: str) -> Optional[Dict]:
        """Extract content from a URL using requests and BeautifulSoup"""
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style", "nav", "header", "footer", ".theme-edit-this-page", ".theme-last-updated"]):
                script.decompose()

            # Focus on the main content area for Docusaurus
            content_selectors = [
                '.theme-doc-markdown article',  # Main article content
                '.theme-doc-markdown',  # Docusaurus markdown content
                '.markdown',  # Markdown content
                'article',  # Article tag
                '.main-wrapper',  # Main wrapper
                'main',  # Main tag
            ]

            content = ""
            title = ""

            # Get title
            title_elem = soup.find('title')
            if title_elem:
                title = title_elem.get_text().strip()
                # Clean up title
                title = re.sub(r'\s*\|\s*.*$', '', title)  # Remove site name after |
            else:
                h1_elem = soup.find('h1')
                if h1_elem:
                    title = h1_elem.get_text().strip()

            # Get content
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    content = content_elem.get_text(separator=' ', strip=True)
                    if content and len(content) > 100:  # Ensure substantial content
                        break

            # Clean up content
            content = re.sub(r'\s+', ' ', content).strip()

            # Remove common navigation text that might be duplicated
            content = re.sub(r'Next\s+\w+|\w+\s+Previous|Docs\s+Home', '', content)

            if not content or len(content) < 50:
                logger.warning(f"Content too short for {url}")
                return None

            return {
                'title': title or 'Untitled',
                'content': content,
                'url': url
            }

        except Exception as e:
            logger.error(f"Error extracting content from {url}: {e}")
            return None

    def _create_chunks(self, text: str, chunk_size: int = 512, overlap: int = 25) -> List[str]:
        """Create overlapping chunks from text"""
        if len(text) <= chunk_size:
            return [text]

        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)

            start += chunk_size - overlap
            if start >= len(text):
                break

        return chunks

    def _generate_embedding(self, text: str) -> Optional[List[float]]:
        """Generate embedding for text with aggressive retry logic for trial accounts"""
        max_retries = 10  # More retries for trial accounts
        for attempt in range(max_retries):
            try:
                response = self.cohere_client.embed(
                    texts=[text],
                    model=self.model,
                    input_type="search_query"
                )

                if response.embeddings and len(response.embeddings) > 0:
                    return response.embeddings[0]
                else:
                    logger.error("No embeddings returned from Cohere")
                    return None

            except cohere.errors.TooManyRequestsError as e:
                wait_time = min(60, 3 ** attempt)  # Aggressive backoff for trial accounts, max 60 seconds
                logger.warning(f"Cohere rate limit hit (attempt {attempt + 1}): {e}. Waiting {wait_time}s...")
                time.sleep(wait_time)
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = min(15, 2 ** attempt)  # Exponential backoff, max 15 seconds
                    logger.warning(f"Embedding generation failed (attempt {attempt + 1}): {e}. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Embedding generation failed after {max_retries} attempts: {e}")
                    return None

    def _create_collection_if_not_exists(self):
        """Create Qdrant collection, clearing if it exists"""
        try:
            # Try to get the collection to see if it exists
            self.qdrant_client.get_collection(self.collection_name)
            logger.info(f"Collection {self.collection_name} already exists, clearing it")
            # Clear existing collection to avoid duplication
            self.qdrant_client.delete_collection(self.collection_name)
            logger.info(f"Deleted existing collection {self.collection_name}")
        except:
            logger.info(f"Collection {self.collection_name} does not exist, will create new one")

        # Create collection
        self.qdrant_client.create_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE)
        )
        logger.info(f"Collection {self.collection_name} created successfully")

    def ingest_urls(self, urls: List[str], chunk_size: int = 512, overlap: int = 25):
        """Ingest multiple URLs into Qdrant with deduplication"""
        logger.info(f"Starting ingestion of {len(urls)} main lesson URLs...")

        # Create collection (clearing any existing content to avoid duplication)
        self._create_collection_if_not_exists()

        successful_ingests = 0
        failed_ingests = 0
        total_chunks = 0

        for i, url in enumerate(urls, 1):
            logger.info(f"Processing {i}/{len(urls)}: {url}")

            # Extract content
            content_data = self._extract_content_from_url(url)
            if not content_data:
                logger.error(f"Failed to extract content from {url}")
                failed_ingests += 1
                continue

            # Create smaller chunks to reduce API calls
            chunks = self._create_chunks(content_data['content'], chunk_size, overlap)

            points_to_insert = []

            for j, chunk in enumerate(chunks):
                # Generate embedding with aggressive rate limiting
                embedding = self._generate_embedding(chunk)
                if not embedding:
                    logger.error(f"Failed to generate embedding for chunk {j+1} of {url}")
                    continue

                # Create point
                point = PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload={
                        "chunk_id": str(uuid.uuid4()),
                        "content": chunk,
                        "source_url": url,
                        "document_title": content_data['title'],
                        "chunk_index": j,
                        "token_count": len(chunk.split()),
                        "created_at": time.strftime('%Y-%m-%dT%H:%M:%S')
                    }
                )
                points_to_insert.append(point)

            # Insert points to Qdrant
            if points_to_insert:
                try:
                    self.qdrant_client.upsert(
                        collection_name=self.collection_name,
                        points=points_to_insert
                    )
                    logger.info(f"Successfully ingested {len(points_to_insert)} chunks from {url}")
                    successful_ingests += 1
                    total_chunks += len(points_to_insert)
                except Exception as e:
                    logger.error(f"Failed to insert chunks to Qdrant for {url}: {e}")
                    failed_ingests += 1
            else:
                logger.error(f"No valid chunks to insert for {url}")
                failed_ingests += 1

            # Longer delay between URLs to respect rate limits for trial accounts
            time.sleep(3)

        logger.info(f"Ingestion completed! Success: {successful_ingests}, Failed: {failed_ingests}")
        logger.info(f"Total chunks ingested: {total_chunks}")

        # Print collection info
        collection_info = self.qdrant_client.get_collection(self.collection_name)
        logger.info(f"Total points in collection: {collection_info.points_count}")

def main():
    # Load only the main lesson URLs (avoiding category/intro pages that might duplicate content)
    import sys
    if len(sys.argv) < 2:
        print("Usage: python ingest_main_content.py <urls_file.txt>")
        sys.exit(1)

    urls_file = sys.argv[1]

    with open(urls_file, 'r', encoding='utf-8') as f:
        all_urls = [line.strip() for line in f if line.strip()]

    # Filter to only include lesson content (not category pages or intro pages)
    lesson_urls = [url for url in all_urls if
                   '/lesson-' in url or  # Main lesson pages
                   url.endswith('/lesson-1') or url.endswith('/lesson-2') or
                   url.endswith('/lesson-3') or url.endswith('/lesson-4')]

    logger.info(f"Filtered to {len(lesson_urls)} lesson URLs from {len(all_urls)} total URLs")

    if not lesson_urls:
        logger.warning("No lesson URLs found. Using all URLs instead.")
        lesson_urls = all_urls

    logger.info(f"Loaded {len(lesson_urls)} lesson URLs from {urls_file}")

    # Initialize and run ingester
    ingester = TargetedBookIngestor()
    ingester.ingest_urls(lesson_urls)

if __name__ == "__main__":
    main()