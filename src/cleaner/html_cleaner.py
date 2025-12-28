"""
Implement HTML cleaner using BeautifulSoup4 to extract text content
Task T012: Implement HTML cleaner using BeautifulSoup4 to extract text content
Task T013: Add removal of navigation, headers, footers, and UI elements
"""

from bs4 import BeautifulSoup, NavigableString
import re
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class HTMLCleaner:
    """HTML cleaner using BeautifulSoup4 to extract text content"""

    def __init__(self):
        # Define CSS selectors for elements to remove (common UI elements in documentation sites)
        self.elements_to_remove = [
            'nav', 'header', 'footer', 'aside', 'menu', 'script', 'style',
            'noscript', 'form', 'input', 'button', 'iframe', 'embed', 'object',
            '[role="navigation"]', '[role="banner"]', '[role="contentinfo"]',
            '.nav', '.navigation', '.sidebar', '.toc', '.table-of-contents',
            '.header', '.footer', '.advertisement', '.ads', '.cookie-consent',
            '.cookie-banner', '.modal', '.popup', '.overlay', '.skip-link',
            '[aria-label="table of contents"]', '[aria-label="main navigation"]',
            '.docusaurus-maintenance-mode', '.theme-edit-this-page', '.theme-last-updated',
            '.theme-doc-footer', '.theme-doc-sidebar', '.menu', '.navbar',
            '.footer--dark', '.footer--light', '.pagination-nav', '.theme-doc-breadcrumbs'
        ]

        # Define CSS selectors for elements that contain the main content
        # These are common in documentation sites like Docusaurus
        self.content_selectors = [
            'main', '.main', '.main-content', '.content', '.container',
            '.doc-content', '.theme-doc-markdown', '.markdown', '.docs-content',
            '.post', '.article', '.entry-content', '.content-body',
            '[role="main"]', '.main-article', '.post-content'
        ]

    def clean_html(self, html_content: str, url: str = "") -> Dict[str, str]:
        """
        Clean HTML content and extract main text content
        """
        if not html_content:
            return {
                'title': '',
                'content': '',
                'processed_content': '',
                'metadata': {}
            }

        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            # Extract title
            title = self._extract_title(soup)

            # Remove unwanted elements
            self._remove_unwanted_elements(soup)

            # Try to find main content container
            main_content = self._find_main_content(soup)

            if main_content:
                # Get text from main content
                content_text = main_content.get_text(separator=' ', strip=True)
            else:
                # If no main content found, get text from body
                body = soup.find('body')
                if body:
                    content_text = body.get_text(separator=' ', strip=True)
                else:
                    content_text = soup.get_text(separator=' ', strip=True)

            # Clean up the text
            processed_content = self._clean_text(content_text)

            # Extract metadata
            metadata = self._extract_metadata(soup, url)

            logger.info(f"Successfully cleaned HTML content. Original length: {len(html_content)}, Cleaned length: {len(processed_content)}")

            return {
                'title': title,
                'content': content_text,
                'processed_content': processed_content,
                'metadata': metadata
            }

        except Exception as e:
            logger.error(f"Error cleaning HTML content: {e}")
            return {
                'title': '',
                'content': '',
                'processed_content': '',
                'metadata': {}
            }

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """
        Extract title from the HTML soup
        """
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

        # Look for og:title meta tag
        og_title = soup.find('meta', property='og:title')
        if og_title and og_title.get('content'):
            return og_title.get('content').strip()

        # If no title found, return empty string
        return ""

    def _remove_unwanted_elements(self, soup: BeautifulSoup):
        """
        Remove unwanted elements from the soup
        """
        for selector in self.elements_to_remove:
            elements = soup.select(selector)
            for element in elements:
                element.decompose()  # Remove the element and its contents

    def _find_main_content(self, soup: BeautifulSoup) -> Optional[BeautifulSoup]:
        """
        Find the main content container in the HTML
        """
        # Try to find content using our predefined selectors
        for selector in self.content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                return content_elem

        # If no specific content container found, return the soup itself
        # (the unwanted elements have already been removed)
        return soup

    def _clean_text(self, text: str) -> str:
        """
        Clean up extracted text by removing extra whitespace and normalizing
        """
        if not text:
            return ""

        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)

        # Remove multiple consecutive newlines
        text = re.sub(r'\n\s*\n', '\n\n', text)

        # Remove leading/trailing whitespace
        text = text.strip()

        # Remove special characters that might be artifacts of HTML extraction
        text = re.sub(r'\u00a0', ' ', text)  # Non-breaking space to regular space
        text = re.sub(r'\u200b', '', text)  # Zero-width space removal

        return text

    def _extract_metadata(self, soup: BeautifulSoup, url: str) -> Dict[str, str]:
        """
        Extract metadata from the HTML
        """
        metadata = {
            'url': url,
            'description': '',
            'author': '',
            'keywords': '',
            'language': '',
            'generator': ''
        }

        # Extract description
        desc_tag = soup.find('meta', attrs={'name': 'description'})
        if desc_tag and desc_tag.get('content'):
            metadata['description'] = desc_tag.get('content').strip()

        # Look for og:description
        og_desc = soup.find('meta', property='og:description')
        if og_desc and og_desc.get('content'):
            metadata['description'] = og_desc.get('content').strip()

        # Extract author
        author_tag = soup.find('meta', attrs={'name': 'author'})
        if author_tag and author_tag.get('content'):
            metadata['author'] = author_tag.get('content').strip()

        # Extract keywords
        keywords_tag = soup.find('meta', attrs={'name': 'keywords'})
        if keywords_tag and keywords_tag.get('content'):
            metadata['keywords'] = keywords_tag.get('content').strip()

        # Extract language
        lang_tag = soup.find('html')
        if lang_tag and lang_tag.get('lang'):
            metadata['language'] = lang_tag.get('lang').strip()

        # Extract generator
        generator_tag = soup.find('meta', attrs={'name': 'generator'})
        if generator_tag and generator_tag.get('content'):
            metadata['generator'] = generator_tag.get('content').strip()

        return metadata

    def clean_multiple_html(self, html_contents: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Clean multiple HTML contents
        """
        cleaned_contents = []

        for item in html_contents:
            html_content = item.get('content', '')
            url = item.get('url', '')
            cleaned = self.clean_html(html_content, url)
            cleaned['original_url'] = url
            cleaned_contents.append(cleaned)

        return cleaned_contents

    def extract_text_from_element(self, element) -> str:
        """
        Extract text from a specific BeautifulSoup element
        """
        if element:
            return element.get_text(separator=' ', strip=True)
        return ""

    def remove_elements_by_class(self, soup: BeautifulSoup, class_names: List[str]):
        """
        Remove elements by specific class names
        """
        for class_name in class_names:
            elements = soup.find_all(class_=class_name)
            for element in elements:
                element.decompose()

    def remove_elements_by_tag(self, soup: BeautifulSoup, tag_names: List[str]):
        """
        Remove elements by specific tag names
        """
        for tag_name in tag_names:
            elements = soup.find_all(tag_name)
            for element in elements:
                element.decompose()