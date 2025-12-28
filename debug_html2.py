#!/usr/bin/env python3
"""
Debug script to examine the HTML structure of a Docusaurus lesson page more thoroughly
"""
import requests
from bs4 import BeautifulSoup

def debug_html_structure():
    # Fetch a sample lesson page
    url = "https://hackathon-ai-physical-book-1ojs.vercel.app/docs/module-1/chapter-1/lesson-1"
    print(f"Fetching HTML from: {url}")

    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch URL: {response.status_code}")
        return

    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    print("\n=== DETAILED ANALYSIS OF MAIN CONTENT AREAS ===")

    # Look for main content containers
    main_content = soup.find('main')
    if main_content:
        print(f"Main tag found: {len(main_content.get_text(strip=True))} chars")
        print(f"Content preview: {main_content.get_text(strip=True)[:200]}...")

    # Look for the docusaurus content fallback
    docusaurus_content = soup.find(id='__docusaurus_skipToContent_fallback')
    if docusaurus_content:
        print(f"__docusaurus_skipToContent_fallback found: {len(docusaurus_content.get_text(strip=True))} chars")
        print(f"Content preview: {docusaurus_content.get_text(strip=True)[:200]}...")

    # Look for the main docusaurus container
    docusaurus_main = soup.find(id='__docusaurus')
    if docusaurus_main:
        print(f"__docusaurus found: {len(docusaurus_main.get_text(strip=True))} chars")
        print(f"Content preview: {docusaurus_main.get_text(strip=True)[:200]}...")

    # Look for specific docusaurus content classes
    theme_main = soup.find(class_='theme-layout-main')
    if theme_main:
        print(f"theme-layout-main found: {len(theme_main.get_text(strip=True))} chars")
        print(f"Content preview: {theme_main.get_text(strip=True)[:200]}...")

    # Look for any div with markdown content
    markdown_divs = soup.find_all('div', class_=lambda x: x and 'markdown' in x.lower())
    for i, div in enumerate(markdown_divs):
        print(f"Markdown div {i+1} (class: {div.get('class')}): {len(div.get_text(strip=True))} chars")
        print(f"Content preview: {div.get_text(strip=True)[:200]}...")

    # Look for article tags (though none were found in initial scan)
    articles = soup.find_all('article')
    for i, article in enumerate(articles):
        print(f"Article {i+1}: {len(article.get_text(strip=True))} chars")
        print(f"Content preview: {article.get_text(strip=True)[:200]}...")

    # Look for any content with doc-related classes
    doc_elements = soup.find_all(class_=lambda x: x and any(keyword in str(x).lower() for keyword in ['doc', 'content', 'theme-doc', 'markdown', 'doc-content']))
    for i, elem in enumerate(doc_elements):
        tag_name = elem.name
        class_name = elem.get('class')
        content_len = len(elem.get_text(strip=True))
        print(f"Doc-related element {i+1} ({tag_name}, class: {class_name}): {content_len} chars")
        print(f"Content preview: {elem.get_text(strip=True)[:200]}...")

    print("\n=== LOOKING FOR SPECIFIC CONTENT CONTAINERS ===")
    # Try to find the actual document content area
    selectors_to_try = [
        '[class*="docItem"]',
        '[class*="doc-content"]',
        '[class*="theme-doc"]',
        '[class*="docMainContainer"]',
        '[class*="container"]',
        '.markdown',
        '.theme-content',
        '#__docusaurus_skipToContent_fallback',
        'main div',
        '.container div'
    ]

    for selector in selectors_to_try:
        elements = soup.select(selector)
        if elements:
            print(f"\nSelector '{selector}' found {len(elements)} element(s):")
            for j, elem in enumerate(elements[:2]):  # Show first 2
                text_content = elem.get_text(strip=True)
                if len(text_content) > 50:  # Only show if it has substantial content
                    print(f"  Element {j+1}: {len(text_content)} chars")
                    print(f"  Content preview: {text_content[:200]}...")

if __name__ == "__main__":
    debug_html_structure()