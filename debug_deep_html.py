#!/usr/bin/env python3
"""
Deep debug script to examine the HTML structure and find the real content containers
"""
import requests
from bs4 import BeautifulSoup

def deep_debug_html_structure():
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

    # Look for all divs with data components or specific attributes that might contain content
    print("\n--- Looking for divs with data attributes ---")
    data_divs = soup.find_all('div', attrs={'data-testid': True})
    for i, div in enumerate(data_divs):
        content = div.get_text(strip=True)
        if content and len(content) > 50:
            print(f"Data testid div {i+1}: {div.get('data-testid')} - {len(content)} chars")
            print(f"Content preview: {content[:150]}...")

    print("\n--- Looking for divs with specific class patterns ---")
    # Look for divs with classes that might contain content
    content_divs = soup.find_all('div')
    for i, div in enumerate(content_divs):
        classes = div.get('class', [])
        if classes:
            class_str = ' '.join(classes)
            # Look for classes that might indicate content areas
            if any(keyword in class_str.lower() for keyword in ['doc', 'content', 'main', 'container', 'wrapper', 'layout']):
                content = div.get_text(strip=True)
                if content and len(content) > 100:
                    print(f"Div class '{class_str}' - {len(content)} chars")
                    try:
                        print(f"Content preview: {content[:150]}...")
                    except UnicodeEncodeError:
                        print(f"Content preview: {repr(content[:150])}...")

    print("\n--- Looking for content in article tags ---")
    articles = soup.find_all('article')
    for i, article in enumerate(articles):
        content = article.get_text(strip=True)
        print(f"Article {i+1} - {len(content)} chars")
        if len(content) > 50:
            try:
                print(f"Content preview: {content[:200]}...")
            except UnicodeEncodeError:
                print(f"Content preview: {repr(content[:200])}...")

    print("\n--- Looking for content in main tag ---")
    main_tags = soup.find_all('main')
    for i, main_tag in enumerate(main_tags):
        content = main_tag.get_text(strip=True)
        print(f"Main tag {i+1} - {len(content)} chars")
        if len(content) > 50:
            try:
                print(f"Content preview: {content[:200]}...")
            except UnicodeEncodeError:
                print(f"Content preview: {repr(content[:200])}...")

    print("\n--- Looking for content in specific IDs ---")
    specific_ids = ['__docusaurus', '__docusaurus_skipToContent_fallback', 'content', 'main-content']
    for id_val in specific_ids:
        element = soup.find(id=id_val)
        if element:
            content = element.get_text(strip=True)
            print(f"Element with ID '{id_val}' - {len(content)} chars")
            if len(content) > 50:
                try:
                    print(f"Content preview: {content[:200]}...")
                except UnicodeEncodeError:
                    print(f"Content preview: {repr(content[:200])}...")

    print("\n--- Looking for content in sections ---")
    sections = soup.find_all('section')
    for i, section in enumerate(sections):
        content = section.get_text(strip=True)
        if content and len(content) > 100:
            try:
                print(f"Section {i+1} - {len(content)} chars")
                print(f"Content preview: {content[:200]}...")
            except UnicodeEncodeError:
                print(f"Section {i+1} - {len(content)} chars")
                print(f"Content preview: {repr(content[:200])}...")

    print("\n--- Looking for content in divs with aria attributes ---")
    aria_divs = soup.find_all('div', attrs={'aria-labelledby': True})
    for i, div in enumerate(aria_divs):
        content = div.get_text(strip=True)
        if content and len(content) > 50:
            try:
                print(f"Aria-labeled div {i+1}: {div.get('aria-labelledby')} - {len(content)} chars")
                print(f"Content preview: {content[:150]}...")
            except UnicodeEncodeError:
                print(f"Aria-labeled div {i+1}: {div.get('aria-labelledby')} - {len(content)} chars")
                print(f"Content preview: {repr(content[:150])}...")

    # Let's also look at the structure more systematically
    print("\n--- Analyzing the HTML structure depth ---")
    # Look for deeply nested content that might be in the actual lesson area
    # Usually lesson content is within nested divs inside main containers
    main_element = soup.find('main')
    if main_element:
        print("Found main element, looking for nested content...")
        # Look for the deepest content within main
        all_descendants = list(main_element.descendants)
        content_candidates = []

        for descendant in all_descendants:
            if descendant.name in ['div', 'article', 'section', 'main'] and hasattr(descendant, 'get_text'):
                text_content = descendant.get_text(strip=True)
                if len(text_content) > 200:  # Significant content
                    classes = descendant.get('class', [])
                    class_info = ' '.join(classes) if classes else 'no-classes'
                    content_candidates.append((text_content, class_info, descendant.name))

        # Sort by content length to find the most substantial content
        content_candidates.sort(key=lambda x: len(x[0]), reverse=True)

        print(f"Found {len(content_candidates)} potential content containers")
        for i, (content, classes, tag) in enumerate(content_candidates[:5]):  # Show top 5
            print(f"\nCandidate {i+1} ({tag}, classes: {classes}): {len(content)} chars")
            try:
                print(f"Content: {content[:300]}...")
            except UnicodeEncodeError:
                print(f"Content: {repr(content[:300])}...")

if __name__ == "__main__":
    deep_debug_html_structure()