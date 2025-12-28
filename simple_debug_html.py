#!/usr/bin/env python3
"""
Simple debug script to examine the HTML structure and find the real content containers
"""
import requests
from bs4 import BeautifulSoup

def simple_debug_html_structure():
    # Fetch a specific lesson page
    url = "https://hackathon-ai-physical-book-1ojs.vercel.app/docs/module-1/chapter-1/lesson-1"
    print(f"Fetching HTML from: {url}")

    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch URL: {response.status_code}")
        return

    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    print("\n=== ANALYZING HTML STRUCTURE ===")

    # Look for the main content area specifically
    main_element = soup.find('main')
    if main_element:
        print(f"\nFound main element with {len(main_element.get_text(strip=True))} chars of content")

        # Look for nested divs within main that might contain the actual lesson content
        nested_divs = main_element.find_all('div', recursive=True)
        content_candidates = []

        for div in nested_divs:
            text_content = div.get_text(strip=True)
            if len(text_content) > 200:  # Only consider substantial content
                classes = div.get('class', [])
                class_str = ' '.join(classes) if classes else 'no-classes'
                content_candidates.append((text_content, class_str, len(text_content)))

        # Sort by content length
        content_candidates.sort(key=lambda x: x[2], reverse=True)

        print(f"\nFound {len(content_candidates)} potential content containers in main element")
        for i, (content, classes, length) in enumerate(content_candidates[:5]):  # Top 5
            print(f"\nCandidate {i+1}: {length} chars")
            print(f"Classes: {classes}")
            # Print without unicode characters
            safe_content = content[:200].encode('ascii', errors='ignore').decode('ascii')
            print(f"Content preview: {safe_content}...")

    # Also check for the docusaurus specific element
    docusaurus_element = soup.find(id='__docusaurus_skipToContent_fallback')
    if docusaurus_element:
        content = docusaurus_element.get_text(strip=True)
        print(f"\nDocusaurus fallback element has {len(content)} chars of content")
        safe_content = content.encode('ascii', errors='ignore').decode('ascii')
        print(f"Content preview: {safe_content[:200]}...")

    # Check for any article tags
    articles = soup.find_all('article')
    for i, article in enumerate(articles):
        content = article.get_text(strip=True)
        print(f"\nArticle {i+1} has {len(content)} chars of content")
        safe_content = content.encode('ascii', errors='ignore').decode('ascii')
        print(f"Content preview: {safe_content[:200]}...")

    # Check for divs with markdown-related classes
    markdown_divs = soup.find_all('div', class_=lambda x: x and 'markdown' in str(x).lower())
    for i, div in enumerate(markdown_divs):
        content = div.get_text(strip=True)
        if len(content) > 100:
            print(f"\nMarkdown div {i+1} has {len(content)} chars of content")
            print(f"Classes: {' '.join(div.get('class', []))}")
            safe_content = content.encode('ascii', errors='ignore').decode('ascii')
            print(f"Content preview: {safe_content[:200]}...")

if __name__ == "__main__":
    simple_debug_html_structure()