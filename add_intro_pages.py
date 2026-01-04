#!/usr/bin/env python3
"""
Script to add missing intro pages to the vector database
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
import openai
import logging
import uuid
from urllib.parse import urljoin, urlparse
import re
import json

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Qdrant client
qdrant_client = QdrantClient(
    url=os.getenv('QDRANT_URL'),
    api_key=os.getenv('QDRANT_API_KEY'),
    https=True
)

collection_name = os.getenv('QDRANT_COLLECTION_NAME', 'document_embeddings')

# Configure OpenAI to use OpenRouter's API
openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
if not openrouter_api_key:
    raise ValueError('OPENROUTER_API_KEY is required for OpenRouter embeddings')

openai.api_key = openrouter_api_key
openai.base_url = 'https://openrouter.ai/api/v1'

# Use OpenRouter embedding model
embedding_model = 'text-embedding-3-small'
embedding_dimensions = 1536

# Create headers to mimic a real browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Authorization': f'Bearer {openrouter_api_key}',
    'HTTP-Referer': 'https://your-app.com',  # Optional, for including usage in metrics
    'X-Title': 'Physical AI Book RAG System'  # Optional, for including usage in metrics
}

def _extract_content_from_url(url: str) -> Optional[Dict]:
    """Extract content from a URL using requests and BeautifulSoup"""
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script and style elements
        for script in soup(['script', 'style', 'nav', 'header', 'footer', '.theme-edit-this-page', '.theme-last-updated']):
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

        content = ''
        title = ''

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
            logger.warning(f'Content too short for {url}')
            return None

        return {
            'title': title or 'Untitled',
            'content': content,
            'url': url
        }

    except Exception as e:
        logger.error(f'Error extracting content from {url}: {e}')
        return None

def _generate_embedding(text: str) -> Optional[List[float]]:
    """Generate embedding for text using OpenRouter's API"""
    max_retries = 5
    for attempt in range(max_retries):
        try:
            # Use OpenRouter's embedding API with proper HTTP request
            headers = {
                'Authorization': f'Bearer {openrouter_api_key}',
                'Content-Type': 'application/json'
            }

            data = {
                'model': embedding_model,
                'input': text
            }

            response = requests.post(
                'https://openrouter.ai/api/v1/embeddings',
                headers=headers,
                data=json.dumps(data),
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                embedding = result['data'][0]['embedding']
                return embedding
            elif response.status_code == 429:
                raise Exception('rate_limit_exceeded')
            else:
                raise Exception(f'HTTP {response.status_code}: {response.text}')

        except Exception as e:
            if 'rate_limit' in str(e).lower() or '429' in str(e):
                wait_time = min(60, 2 ** attempt)  # Exponential backoff, max 60 seconds
                logger.warning(f'OpenRouter rate limit hit (attempt {attempt + 1}): {e}. Waiting {wait_time}s...')
                time.sleep(wait_time)
            elif attempt < max_retries - 1:
                wait_time = min(10, 2 ** attempt)  # Exponential backoff, max 10 seconds
                logger.warning(f'Embedding generation failed (attempt {attempt + 1}): {e}. Retrying in {wait_time}s...')
                time.sleep(wait_time)
            else:
                logger.error(f'Embedding generation failed after {max_retries} attempts: {e}')
                return None

# List of intro URLs to add
intro_urls = [
    'https://hackathon-ai-physical-book-1ojs.vercel.app/docs',
    'https://hackathon-ai-physical-book-1ojs.vercel.app/docs/intro',
    'https://hackathon-ai-physical-book-1ojs.vercel.app/docs/module-1/intro',
    'https://hackathon-ai-physical-book-1ojs.vercel.app/docs/module-2/intro',
    'https://hackathon-ai-physical-book-1ojs.vercel.app/docs/module-3/intro',
    'https://hackathon-ai-physical-book-1ojs.vercel.app/docs/module-4/intro'
]

logger.info('Starting ingestion of intro pages...')

successful_ingests = 0
failed_ingests = 0

for i, url in enumerate(intro_urls, 1):
    logger.info(f'Processing {i}/{len(intro_urls)}: {url}')

    # Extract content
    content_data = _extract_content_from_url(url)
    if not content_data:
        logger.error(f'Failed to extract content from {url}')
        failed_ingests += 1
        continue

    # Generate embedding
    embedding = _generate_embedding(content_data['content'])
    if not embedding:
        logger.error(f'Failed to generate embedding for {url}')
        failed_ingests += 1
        continue

    # Create point
    point = PointStruct(
        id=str(uuid.uuid4()),
        vector=embedding,
        payload={
            'chunk_id': str(uuid.uuid4()),
            'content': content_data['content'],
            'source_url': url,
            'document_title': content_data['title'],
            'chunk_index': 0,
            'token_count': len(content_data['content'].split()),
            'created_at': time.strftime('%Y-%m-%dT%H:%M:%S')
        }
    )

    # Insert point to Qdrant
    try:
        qdrant_client.upsert(
            collection_name=collection_name,
            points=[point]
        )
        logger.info(f'Successfully ingested intro page from {url}')
        successful_ingests += 1
    except Exception as e:
        logger.error(f'Failed to insert intro page to Qdrant for {url}: {e}')
        failed_ingests += 1

    # Delay between URLs to respect rate limits
    time.sleep(1)

logger.info(f'Intro pages ingestion completed! Success: {successful_ingests}, Failed: {failed_ingests}')

# Print final collection info
collection_info = qdrant_client.get_collection(collection_name)
logger.info(f'Total points in collection: {collection_info.points_count}')