#!/usr/bin/env python3
"""
Test script to check what content is actually being extracted from different URLs
"""
import requests
from bs4 import BeautifulSoup
import re

def extract_content_with_selectors(html_content):
    """Extract content using the same selectors we implemented"""
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove unwanted elements first
    elements_to_remove = [
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

    for selector in elements_to_remove:
        for element in soup.select(selector):
            element.decompose()

    # Try to find content using our specific selectors
    content_selectors = [
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

    text_content = ""
    content_found = False

    for selector in content_selectors:
        content_elements = soup.select(selector)
        if content_elements:
            # Extract text from the specific content areas
            content_parts = []
            for element in content_elements:
                # Remove any remaining unwanted elements within the content
                for unwanted in elements_to_remove:
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
        text_content = soup.get_text(separator=' ', strip=True)

    # Clean up excessive whitespace
    text_content = re.sub(r'\s+', ' ', text_content)

    # Remove very short text fragments that are likely noise
    if len(text_content) < 100:
        text_content = soup.get_text(separator=' ', strip=True)
        text_content = re.sub(r'\s+', ' ', text_content)

    return text_content

def test_content_extraction():
    # Test different types of pages
    urls_to_test = [
        "https://hackathon-ai-physical-book-1ojs.vercel.app/docs/module-1/chapter-1/lesson-1",
        "https://hackathon-ai-physical-book-1ojs.vercel.app/docs/module-1/chapter-2/lesson-1",
        "https://hackathon-ai-physical-book-1ojs.vercel.app/docs/module-2/chapter-1/lesson-1",
        "https://hackathon-ai-physical-book-1ojs.vercel.app/docs/intro",
        "https://hackathon-ai-physical-book-1ojs.vercel.app/docs/module-1/intro"
    ]

    print("Testing content extraction from different pages:\n")

    for i, url in enumerate(urls_to_test, 1):
        print(f"URL {i}: {url}")
        try:
            response = requests.get(url)
            if response.status_code == 200:
                content = extract_content_with_selectors(response.text)
                print(f"Extracted content length: {len(content)} characters")
                print(f"First 200 chars: {content[:200]}...")
                print(f"Last 200 chars: {content[-200:] if len(content) > 200 else content}...")
                print("-" * 80)
            else:
                print(f"Failed to fetch: {response.status_code}")
                print("-" * 80)
        except Exception as e:
            print(f"Error processing {url}: {str(e)}")
            print("-" * 80)

if __name__ == "__main__":
    test_content_extraction()