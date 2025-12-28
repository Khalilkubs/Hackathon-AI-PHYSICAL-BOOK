"""
Create URL fetcher module to retrieve content from Docusaurus URLs
Task T011: Create URL fetcher module to retrieve content from Docusaurus URLs
"""

import requests
from typing import Optional, Dict, Any
from urllib.parse import urljoin, urlparse
import time
import logging
from src.utils.retry_mechanism import retry_on_network_errors
from src.utils.validation import validate_url, sanitize_url

logger = logging.getLogger(__name__)


class URLFetcher:
    """URL fetcher module to retrieve content from Docusaurus URLs"""

    def __init__(self, timeout: int = 30, max_retries: int = 3):
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()

        # Set a user agent to avoid being blocked by some servers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    @retry_on_network_errors
    def fetch_content(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Fetch content from a URL with retry logic
        """
        # Validate and sanitize the URL first
        if not validate_url(url):
            logger.error(f"Invalid URL provided: {url}")
            return None

        sanitized_url = sanitize_url(url)
        if not sanitized_url:
            logger.error(f"Could not sanitize URL: {url}")
            return None

        try:
            logger.info(f"Fetching content from: {sanitized_url}")

            response = self.session.get(
                sanitized_url,
                timeout=self.timeout
            )

            # Check if the request was successful
            if response.status_code == 200:
                # Try to extract title from HTML
                title = self._extract_title(response.text)

                logger.info(f"Successfully fetched content from {sanitized_url}, length: {len(response.text)} chars")

                return {
                    'url': sanitized_url,
                    'content': response.text,
                    'status_code': response.status_code,
                    'title': title or urlparse(sanitized_url).path.split('/')[-1] or 'Untitled',
                    'headers': dict(response.headers),
                    'encoding': response.encoding
                }
            else:
                logger.error(f"Failed to fetch content from {sanitized_url}, status code: {response.status_code}")
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Request exception when fetching {sanitized_url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error when fetching {sanitized_url}: {e}")
            return None

    def _extract_title(self, html_content: str) -> Optional[str]:
        """
        Extract title from HTML content
        """
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Try to find title in various places
            title_tag = soup.find('title')
            if title_tag:
                return title_tag.get_text().strip()

            # Look for h1 tags which might contain the main title
            h1_tag = soup.find('h1')
            if h1_tag:
                return h1_tag.get_text().strip()

            # Look for specific Docusaurus title elements
            title_elem = soup.find('meta', attrs={'name': 'docsearch:doctitle'})
            if title_elem and title_elem.get('content'):
                return title_elem.get('content').strip()

            # If no title found, return None
            return None
        except Exception as e:
            logger.warning(f"Could not extract title from HTML: {e}")
            return None

    def fetch_multiple_urls(self, urls: list) -> Dict[str, Any]:
        """
        Fetch content from multiple URLs
        """
        results = {
            'successful': 0,
            'failed': 0,
            'total': len(urls),
            'results': []
        }

        for url in urls:
            result = self.fetch_content(url)
            if result:
                results['successful'] += 1
                results['results'].append(result)
            else:
                results['failed'] += 1
                results['results'].append({
                    'url': url,
                    'content': None,
                    'status_code': None,
                    'title': 'Failed to fetch',
                    'headers': {},
                    'encoding': None
                })

        return results

    def check_url_reachable(self, url: str) -> bool:
        """
        Check if a URL is reachable without fetching the full content
        """
        if not validate_url(url):
            return False

        sanitized_url = sanitize_url(url)
        if not sanitized_url:
            return False

        try:
            response = self.session.head(
                sanitized_url,
                timeout=self.timeout,
                allow_redirects=True
            )
            return response.status_code == 200
        except:
            return False

    def get_content_length(self, url: str) -> Optional[int]:
        """
        Get the content length of a URL without downloading the content
        """
        if not validate_url(url):
            return None

        sanitized_url = sanitize_url(url)
        if not sanitized_url:
            return None

        try:
            response = self.session.head(
                sanitized_url,
                timeout=self.timeout,
                allow_redirects=True
            )

            content_length = response.headers.get('content-length')
            if content_length:
                return int(content_length)
            return None
        except:
            return None