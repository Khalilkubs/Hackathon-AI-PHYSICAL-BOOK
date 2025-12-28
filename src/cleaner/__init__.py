"""
HTML Cleaner Module for Document Ingestion and Vector Storage System
Extracts relevant text content from HTML and removes navigation and UI elements
"""

from bs4 import BeautifulSoup
from typing import Optional
import re
import logging

logger = logging.getLogger(__name__)


class HTMLCleaner:
    """
    Class to clean HTML content and extract relevant text
    """

    def __init__(self):
        # CSS selectors for elements to remove - be more specific to avoid removing content
        self.elements_to_remove = [
            'nav', 'header', 'footer', 'aside', 'script', 'style', 'noscript',
            '[class*="nav-"]', '[class*="navbar"]', '[class*="header"]', '[class*="footer"]',
            '[class*="sidebar"]', '[class*="menu"]', '[class*="toc"]', '[class*="table-of-contents"]',
            '[id*="nav"]', '[id*="header"]', '[id*="footer"]',
            '[id*="sidebar"]', '[id*="menu"]', '[id*="toc"]', '[id*="table-of-contents"]',
            # Docusaurus specific elements to remove
            '[class*="doc-sidebar"]', '[class*="doc-toc"]', '[class*="theme-doc-sidebar"]',
            '[class*="navbar"]', '[class*="footer"]', '[class*="search"]', '[class*="pagination"]',
            '[class*="theme-edit-this-page"]', '[class*="theme-last-updated"]', '[class*="table-of-contents"]'
        ]

        # CSS selectors for content areas to preserve (Docusaurus specific)
        # These are more specific to Docusaurus markdown content areas
        self.content_selectors = [
            '#__docusaurus_skipToContent_fallback',  # Main Docusaurus content fallback
            'main',  # Main content area
            '[class*="docItem"] [class*="markdown"]',
            '[class*="theme-doc-markdown"]',
            '[class*="markdown"]',
            '[class*="doc-content"]',
            '[class*="theme-doc-content"]',
            'article',
            '.markdown',
            '.theme-content',
            '.doc-markdown',
            '.theme-doc-markdown'
        ]

    def clean_html(self, html_content: str, url: str = "") -> Optional[str]:
        """
        Clean HTML content and extract relevant text content

        Args:
            html_content: Raw HTML content to clean
            url: Source URL (optional, for logging)

        Returns:
            Cleaned text content, or None if cleaning failed
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            # First, try to find content using our specific selectors
            content_found = False
            text_content = ""

            for selector in self.content_selectors:
                content_elements = soup.select(selector)
                if content_elements:
                    # Extract text from the specific content areas
                    content_parts = []
                    for element in content_elements:
                        # Remove any remaining unwanted elements within the content
                        for unwanted in self.elements_to_remove:
                            for unwanted_element in element.select(unwanted):
                                unwanted_element.decompose()

                        part_text = element.get_text(separator=' ', strip=True)
                        if part_text:
                            content_parts.append(part_text)

                    if content_parts:
                        text_content = ' '.join(content_parts)
                        content_found = True
                        break

            # If no specific content was found using selectors, fall back to general extraction
            if not content_found:
                # Remove unwanted elements first
                for selector in self.elements_to_remove:
                    for element in soup.select(selector):
                        element.decompose()

                # Get text content, preserving paragraph structure
                text_content = soup.get_text(separator=' ', strip=True)

            # Clean up excessive whitespace
            text_content = re.sub(r'\s+', ' ', text_content)

            # Remove very short text fragments that are likely noise
            text_content = self._remove_noise(text_content)

            logger.info(f"Cleaned HTML content from {url}, extracted {len(text_content)} characters")
            return text_content

        except Exception as e:
            logger.error(f"Error cleaning HTML content from {url}: {str(e)}")
            return None

    def extract_title(self, html_content: str) -> Optional[str]:
        """
        Extract the title from HTML content

        Args:
            html_content: Raw HTML content

        Returns:
            The page title, or None if not found
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            # Try to find the title in different ways
            title = None

            # First, try the <title> tag
            title_tag = soup.find('title')
            if title_tag:
                title = title_tag.get_text().strip()

            # If no title found, try h1 tags (common in documentation)
            if not title:
                h1_tag = soup.find('h1')
                if h1_tag:
                    title = h1_tag.get_text().strip()

            # If still no title, try to find any heading
            if not title:
                for heading in ['h1', 'h2', 'h3']:
                    heading_tag = soup.find(heading)
                    if heading_tag:
                        title = heading_tag.get_text().strip()
                        break

            return title if title else "Untitled Document"

        except Exception as e:
            logger.error(f"Error extracting title from HTML: {str(e)}")
            return "Untitled Document"

    def _remove_noise(self, text: str) -> str:
        """
        Remove noise from extracted text

        Args:
            text: Raw extracted text

        Returns:
            Cleaned text with noise removed
        """
        if not text:
            return text

        # Remove very short fragments that are likely noise
        # Split by common sentence separators and filter out short fragments
        sentences = re.split(r'[.!?]+', text)
        cleaned_sentences = []

        for sentence in sentences:
            sentence = sentence.strip()
            # Only keep sentences that are reasonably long and have actual content
            if len(sentence) > 10 and len(sentence.split()) > 2:
                cleaned_sentences.append(sentence)

        return '. '.join(cleaned_sentences)