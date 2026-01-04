#!/usr/bin/env python3
"""
Fast Ingestion Script for Physical AI & Humanoid Robotics Book
This script uses requests and BeautifulSoup instead of Selenium for faster processing
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

class FastBookIngestor:
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

        # Verify connections
        self._verify_connections()

    def _verify_connections(self):
        """Verify that all required services are accessible"""
        logger.info("Verifying connections...")

        # Test Qdrant connection
        try:
            self.qdrant_client.get_collection(self.collection_name)
            logger.info("✅ Qdrant connection verified")
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
            for script in soup(["script", "style", "nav", "header", "footer"]):
                script.decompose()

            # Try to find the main content area (Docusaurus specific selectors)
            content_selectors = [
                'article',  # Main content area
                '.theme-doc-markdown',  # Docusaurus content
                '.markdown',  # Markdown content
                '.main-wrapper',  # Main wrapper
                'main',  # Main tag
                '.container',  # Container
                '.content',  # Content class
            ]

            content = ""
            title = ""

            # Get title
            title_elem = soup.find('title')
            if title_elem:
                title = title_elem.get_text().strip()
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

            # Fallback to body if no specific content found
            if not content:
                body_elem = soup.find('body')
                if body_elem:
                    content = body_elem.get_text(separator=' ', strip=True)

            # Clean up content
            content = re.sub(r'\s+', ' ', content).strip()

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

    def _create_chunks(self, text: str, chunk_size: int = 1024, overlap: int = 50) -> List[str]:
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
                wait_time = min(30, 2 ** attempt)  # Exponential backoff, max 30 seconds
                logger.warning(f"Cohere rate limit hit (attempt {attempt + 1}): {e}. Waiting {wait_time}s...")
                time.sleep(wait_time)
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = min(10, 2 ** attempt)  # Exponential backoff, max 10 seconds
                    logger.warning(f"Embedding generation failed (attempt {attempt + 1}): {e}. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Embedding generation failed after {max_retries} attempts: {e}")
                    return None

    def _create_collection_if_not_exists(self):
        """Create Qdrant collection if it doesn't exist"""
        try:
            self.qdrant_client.get_collection(self.collection_name)
            logger.info(f"Collection {self.collection_name} already exists")
        except:
            logger.info(f"Creating collection {self.collection_name}")
            self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE)
            )
            logger.info(f"Collection {self.collection_name} created successfully")

    def ingest_urls(self, urls: List[str], chunk_size: int = 512, overlap: int = 25):
        """Ingest multiple URLs into Qdrant with aggressive rate limiting"""
        logger.info(f"Starting ingestion of {len(urls)} URLs with rate limiting...")

        # Create collection if needed
        self._create_collection_if_not_exists()

        successful_ingests = 0
        failed_ingests = 0

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
                except Exception as e:
                    logger.error(f"Failed to insert chunks to Qdrant for {url}: {e}")
                    failed_ingests += 1
            else:
                logger.error(f"No valid chunks to insert for {url}")
                failed_ingests += 1

            # Longer delay between URLs to respect rate limits
            time.sleep(2)

        logger.info(f"Ingestion completed! Success: {successful_ingests}, Failed: {failed_ingests}")

        # Print collection info
        collection_info = self.qdrant_client.get_collection(self.collection_name)
        logger.info(f"Total points in collection: {collection_info.points_count}")

def main():
    # Load URLs from file
    import sys
    if len(sys.argv) < 2:
        print("Usage: python fast_ingest.py <urls_file.txt>")
        sys.exit(1)

    urls_file = sys.argv[1]

    with open(urls_file, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip()]

    logger.info(f"Loaded {len(urls)} URLs from {urls_file}")

    # Initialize and run ingester
    ingester = FastBookIngestor()
    ingester.ingest_urls(urls)

if __name__ == "__main__":
    main()