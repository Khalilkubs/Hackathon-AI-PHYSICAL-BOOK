"""
Sitemap Parser Module for Document Ingestion and Vector Storage System
Parses XML sitemaps to extract URLs for processing
"""

import requests
from typing import List
from xml.etree import ElementTree as ET
import logging
from src.utils import validate_url

logger = logging.getLogger(__name__)


class SitemapParser:
    """
    Class to parse XML sitemaps and extract URLs for processing
    """

    def __init__(self, timeout: int = 30, max_retries: int = 3):
        """
        Initialize the sitemap parser

        Args:
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
        """
        self.timeout = timeout
        self.max_retries = max_retries

    def parse_sitemap(self, sitemap_url: str) -> List[str]:
        """
        Parse a sitemap URL and extract all URLs

        Args:
            sitemap_url: URL of the sitemap.xml file

        Returns:
            List of URLs extracted from the sitemap
        """
        logger.info(f"Parsing sitemap: {sitemap_url}")

        # Fetch the sitemap content
        response = None
        for attempt in range(self.max_retries):
            try:
                response = requests.get(sitemap_url, timeout=self.timeout)
                response.raise_for_status()
                break
            except requests.exceptions.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed to fetch sitemap: {e}")
                if attempt == self.max_retries - 1:
                    logger.error(f"Failed to fetch sitemap after {self.max_retries} attempts: {e}")
                    return []

        # Parse the XML content
        try:
            root = ET.fromstring(response.text)
        except ET.ParseError as e:
            logger.error(f"Failed to parse sitemap XML: {e}")
            return []

        # Extract URLs from the sitemap
        urls = []
        namespace = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

        # Look for <url><loc> elements (standard sitemap format)
        for url_elem in root.findall('sitemap:url', namespace):
            loc_elem = url_elem.find('sitemap:loc', namespace)
            if loc_elem is not None and loc_elem.text:
                url = loc_elem.text.strip()
                if validate_url(url):
                    urls.append(url)

        # Also look for URLs without namespace (in case the sitemap doesn't use namespaces)
        if not urls:
            for url_elem in root.findall('url'):
                loc_elem = url_elem.find('loc')
                if loc_elem is not None and loc_elem.text:
                    url = loc_elem.text.strip()
                    if validate_url(url):
                        urls.append(url)

        # Also check for sitemap references (sitemap index files)
        sitemap_namespace = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        for sitemap_elem in root.findall('sitemap:sitemap', sitemap_namespace):
            loc_elem = sitemap_elem.find('sitemap:loc', sitemap_namespace)
            if loc_elem is not None and loc_elem.text:
                sitemap_url = loc_elem.text.strip()
                if validate_url(sitemap_url):
                    # Recursively parse nested sitemaps
                    nested_urls = self.parse_sitemap(sitemap_url)
                    urls.extend(nested_urls)

        # Filter out blog URLs as requested
        filtered_urls = [url for url in urls if '/blog' not in url.lower()]

        # Fix domain issue - replace the domain in sitemap with the actual domain we're accessing
        # The sitemap may have a different domain than the one we're accessing
        actual_domain = sitemap_url.replace('/sitemap.xml', '').replace('https://', '').replace('http://', '')
        sitemap_domain = 'hackathon-ai-physical-book.vercel.app'  # Known domain from sitemap

        fixed_urls = []
        for url in filtered_urls:
            if sitemap_domain in url:
                # Replace the sitemap domain with the actual domain we're accessing
                fixed_url = url.replace(sitemap_domain, actual_domain)
                fixed_urls.append(fixed_url)
            else:
                fixed_urls.append(url)

        logger.info(f"Extracted {len(urls)} URLs from sitemap, filtered to {len(filtered_urls)} (excluding blog URLs), fixed to {len(fixed_urls)} domains")
        return fixed_urls

    def parse_sitemap_from_content(self, sitemap_content: str, base_url: str = None) -> List[str]:
        """
        Parse sitemap content directly from a string

        Args:
            sitemap_content: XML content of the sitemap
            base_url: Base URL to fix domain issues (optional)

        Returns:
            List of URLs extracted from the sitemap content
        """
        logger.info("Parsing sitemap from provided content")

        try:
            root = ET.fromstring(sitemap_content)
        except ET.ParseError as e:
            logger.error(f"Failed to parse sitemap XML: {e}")
            return []

        # Extract URLs from the sitemap
        urls = []
        namespace = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

        # Look for <url><loc> elements (standard sitemap format)
        for url_elem in root.findall('sitemap:url', namespace):
            loc_elem = url_elem.find('sitemap:loc', namespace)
            if loc_elem is not None and loc_elem.text:
                url = loc_elem.text.strip()
                if validate_url(url):
                    urls.append(url)

        # Also look for URLs without namespace (in case the sitemap doesn't use namespaces)
        if not urls:
            for url_elem in root.findall('url'):
                loc_elem = url_elem.find('loc')
                if loc_elem is not None and loc_elem.text:
                    url = loc_elem.text.strip()
                    if validate_url(url):
                        urls.append(url)

        # Filter out blog URLs as requested
        filtered_urls = [url for url in urls if '/blog' not in url.lower()]

        # Fix domain issue if base_url is provided
        if base_url:
            actual_domain = base_url.replace('/sitemap.xml', '').replace('https://', '').replace('http://', '')
            sitemap_domain = 'hackathon-ai-physical-book.vercel.app'  # Known domain from sitemap

            fixed_urls = []
            for url in filtered_urls:
                if sitemap_domain in url:
                    # Replace the sitemap domain with the actual domain we're accessing
                    fixed_url = url.replace(sitemap_domain, actual_domain)
                    fixed_urls.append(fixed_url)
                else:
                    fixed_urls.append(url)

            logger.info(f"Extracted {len(urls)} URLs from sitemap content, filtered to {len(filtered_urls)} (excluding blog URLs), fixed to {len(fixed_urls)} domains")
            return fixed_urls
        else:
            logger.info(f"Extracted {len(urls)} URLs from sitemap content, filtered to {len(filtered_urls)} (excluding blog URLs)")
            return filtered_urls


def extract_urls_from_sitemap(sitemap_url: str, timeout: int = 30, max_retries: int = 3) -> List[str]:
    """
    Convenience function to extract URLs from a sitemap

    Args:
        sitemap_url: URL of the sitemap.xml file
        timeout: Request timeout in seconds
        max_retries: Maximum number of retries for failed requests

    Returns:
        List of URLs extracted from the sitemap
    """
    parser = SitemapParser(timeout=timeout, max_retries=max_retries)
    return parser.parse_sitemap(sitemap_url)