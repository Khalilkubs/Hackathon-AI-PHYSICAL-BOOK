"""
Document processor to orchestrate fetching and cleaning
Tasks T014: Implement document ingestion pipeline with error handling
Tasks T015: Create DocumentProcessor to orchestrate fetching and cleaning
"""

import uuid
from datetime import datetime
from typing import Dict, Any, List
import logging
from src.fetcher.url_fetcher import URLFetcher
from src.cleaner.html_cleaner import HTMLCleaner
from src.models.document_models import Document
from src.utils.config_manager import ConfigManager
from src.utils.validation import validate_url, validate_content
from src.utils.retry_mechanism import RetryHandler

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Document processor to orchestrate fetching and cleaning"""

    def __init__(self, config: dict = None):
        if config is None:
            self.config_manager = ConfigManager()
            self.config = self.config_manager.processing_config
        else:
            self.config = config
            self.config_manager = None

        self.url_fetcher = URLFetcher(
            timeout=self.config.get('request_timeout', 30),
            max_retries=self.config.get('max_retries', 3)
        )
        self.html_cleaner = HTMLCleaner()
        self.retry_handler = RetryHandler(
            max_retries=self.config.get('max_retries', 3),
            base_delay=1.0,
            max_delay=30.0
        )

    def process_document(self, url: str) -> Dict[str, Any]:
        """
        Process a single document: fetch, clean, and return as Document object
        """
        start_time = datetime.now()

        try:
            # Validate URL
            if not validate_url(url):
                logger.error(f"Invalid URL: {url}")
                return {
                    'status': 'failed',
                    'message': 'Invalid URL format',
                    'processing_time': (datetime.now() - start_time).total_seconds(),
                    'document_id': None
                }

            logger.info(f"Starting document processing for: {url}")

            # Fetch content
            fetch_result = self.url_fetcher.fetch_content(url)
            if not fetch_result or not fetch_result.get('content'):
                logger.error(f"Failed to fetch content from: {url}")
                return {
                    'status': 'failed',
                    'message': 'Failed to fetch content from URL',
                    'processing_time': (datetime.now() - start_time).total_seconds(),
                    'document_id': None
                }

            logger.info(f"Successfully fetched content from {url}")

            # Clean HTML content
            clean_result = self.html_cleaner.clean_html(
                fetch_result['content'],
                url
            )

            if not clean_result or not clean_result.get('processed_content'):
                logger.error(f"Failed to clean HTML content from: {url}")
                return {
                    'status': 'failed',
                    'message': 'Failed to clean HTML content',
                    'processing_time': (datetime.now() - start_time).total_seconds(),
                    'document_id': None
                }

            logger.info(f"Successfully cleaned HTML content from {url}")

            # Validate cleaned content
            if not validate_content(clean_result['processed_content']):
                logger.error(f"Content validation failed for: {url}")
                return {
                    'status': 'failed',
                    'message': 'Content validation failed',
                    'processing_time': (datetime.now() - start_time).total_seconds(),
                    'document_id': None
                }

            # Create document ID
            document_id = str(uuid.uuid4())

            # Create Document object
            document = Document(
                id=document_id,
                url=url,
                title=clean_result['title'],
                content=fetch_result['content'],  # Raw content
                processed_content=clean_result['processed_content'],  # Cleaned content
                created_at=datetime.now(),
                updated_at=datetime.now(),
                metadata=clean_result['metadata']
            )

            # Validate the document
            if not document.validate():
                logger.error(f"Document validation failed for: {url}")
                return {
                    'status': 'failed',
                    'message': 'Document validation failed',
                    'processing_time': (datetime.now() - start_time).total_seconds(),
                    'document_id': document_id
                }

            processing_time = (datetime.now() - start_time).total_seconds()

            logger.info(f"Successfully processed document {document_id} from {url}")

            return {
                'status': 'success',
                'message': 'Document processed successfully',
                'document': document,
                'processing_time': processing_time,
                'document_id': document_id,
                'title': document.title,
                'content_length': len(document.processed_content)
            }

        except Exception as e:
            logger.error(f"Error processing document from {url}: {e}")
            return {
                'status': 'failed',
                'message': f'Error processing document: {str(e)}',
                'processing_time': (datetime.now() - start_time).total_seconds(),
                'document_id': None
            }

    def process_multiple_urls(self, urls: List[str]) -> Dict[str, Any]:
        """
        Process multiple URLs and return aggregated results
        """
        start_time = datetime.now()

        results = {
            'total_urls': len(urls),
            'successful': 0,
            'failed': 0,
            'results': [],
            'total_processing_time': 0,
            'documents': []
        }

        for url in urls:
            result = self.process_document(url)
            results['results'].append(result)

            if result['status'] == 'success':
                results['successful'] += 1
                if 'document' in result:
                    results['documents'].append(result['document'])
            else:
                results['failed'] += 1

        results['total_processing_time'] = (datetime.now() - start_time).total_seconds()

        logger.info(f"Processed {len(urls)} URLs: {results['successful']} successful, {results['failed']} failed")

        return results

    def validate_document(self, document: Document) -> bool:
        """
        Validate a document object
        """
        if not document:
            return False

        return document.validate()

    def add_logging_and_status(self, url: str, status: str, message: str = ""):
        """
        Add logging and status reporting for ingestion process
        Task T016: Add logging and status reporting for ingestion process
        """
        if status == 'success':
            logger.info(f"Document processing SUCCESS for {url}: {message}")
        elif status == 'failed':
            logger.error(f"Document processing FAILED for {url}: {message}")
        elif status == 'in_progress':
            logger.info(f"Document processing IN PROGRESS for {url}: {message}")
        else:
            logger.info(f"Document processing {status.upper()} for {url}: {message}")

    def test_document_processing(self, url: str) -> bool:
        """
        Test to verify Docusaurus URL content is successfully crawled and cleaned
        Task T017: Create test to verify Docusaurus URL content is successfully crawled and cleaned
        """
        result = self.process_document(url)

        if result['status'] == 'success':
            doc = result.get('document')
            if doc and doc.processed_content.strip():
                logger.info(f"Test successful: Document from {url} was processed successfully")
                logger.info(f"Title: {doc.title}")
                logger.info(f"Content length: {len(doc.processed_content)} characters")
                return True
            else:
                logger.error(f"Test failed: Document from {url} has no content after processing")
                return False
        else:
            logger.error(f"Test failed: Could not process document from {url}. Error: {result['message']}")
            return False

    def implement_site_crawling(self, base_url: str, max_pages: int = 10) -> List[str]:
        """
        Implement site crawling to process multiple pages from a Docusaurus site
        Task T018: Implement site crawling to process multiple pages from a Docusaurus site
        """
        # This is a basic implementation - in a real scenario, you'd implement
        # proper web crawling with respect to robots.txt and rate limiting
        try:
            from urllib.parse import urljoin, urlparse
            import requests
            from bs4 import BeautifulSoup

            urls_to_process = set()
            urls_to_process.add(base_url)
            processed_urls = set()

            session = requests.Session()
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (compatible; DocumentProcessor/1.0)'
            })

            while urls_to_process and len(processed_urls) < max_pages:
                current_url = urls_to_process.pop()

                if current_url in processed_urls:
                    continue

                try:
                    response = session.get(current_url, timeout=10)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')

                        # Find all links that are relative to the base URL
                        for link in soup.find_all('a', href=True):
                            href = link['href']
                            full_url = urljoin(base_url, href)

                            # Only add URLs from the same domain
                            if urlparse(full_url).netloc == urlparse(base_url).netloc:
                                # Only add URLs that look like documentation pages
                                if any(ext not in full_url for ext in ['.pdf', '.jpg', '.png', '.zip']):
                                    urls_to_process.add(full_url)

                        processed_urls.add(current_url)
                        logger.info(f"Discovered {len(urls_to_process)} new URLs, processed {len(processed_urls)} so far")

                except Exception as e:
                    logger.error(f"Error crawling {current_url}: {e}")
                    continue

            logger.info(f"Site crawling completed. Found {len(processed_urls)} URLs to process")
            return list(processed_urls)

        except Exception as e:
            logger.error(f"Error during site crawling: {e}")
            return [base_url]  # Return the base URL as fallback

    def add_content_validation(self, document: Document) -> Dict[str, Any]:
        """
        Add content validation and integrity checks for processed documents
        Task T019: Add content validation and integrity checks for processed documents
        """
        validation_results = {
            'document_id': document.id,
            'url': document.url,
            'title_valid': bool(document.title.strip()),
            'content_length': len(document.content),
            'processed_content_length': len(document.processed_content),
            'metadata_count': len(document.metadata),
            'content_quality_score': 0.0,
            'valid': True,
            'issues': []
        }

        # Check if content is too short
        if len(document.processed_content.strip()) < 50:
            validation_results['issues'].append('Content too short (< 50 characters)')
            validation_results['valid'] = False

        # Check if title is meaningful
        if not document.title.strip() or len(document.title.strip()) < 3:
            validation_results['issues'].append('Title too short or missing')

        # Check content quality (simple heuristic)
        content = document.processed_content.lower()
        meaningful_words = len([word for word in content.split() if len(word) > 2])
        total_chars = len(content)
        if total_chars > 0:
            content_quality = meaningful_words / (total_chars / 100)  # Words per 100 characters
            validation_results['content_quality_score'] = min(content_quality, 1.0)

        # Check for potential issues
        if '404' in document.content or 'not found' in content:
            validation_results['issues'].append('Content may contain error message (404/Not Found)')
            validation_results['valid'] = False

        if 'access denied' in content or 'forbidden' in content:
            validation_results['issues'].append('Content may be access restricted')
            validation_results['valid'] = False

        logger.info(f"Content validation for {document.id}: {'Valid' if validation_results['valid'] else 'Invalid'}")
        if validation_results['issues']:
            logger.info(f"Issues: {', '.join(validation_results['issues'])}")

        return validation_results