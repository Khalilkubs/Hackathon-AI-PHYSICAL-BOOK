#!/usr/bin/env python3
"""
Debug script to examine the HTML structure of a Docusaurus lesson page
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

    print("\n=== PAGE TITLE ===")
    title_tag = soup.find('title')
    if title_tag:
        print(f"Title: {title_tag.get_text().strip()}")

    print("\n=== H1 TAGS ===")
    h1_tags = soup.find_all('h1')
    for i, h1 in enumerate(h1_tags):
        print(f"H1 {i+1}: {h1.get_text().strip()}")

    print("\n=== H2 TAGS ===")
    h2_tags = soup.find_all('h2')
    for i, h2 in enumerate(h2_tags[:5]):  # Show first 5
        print(f"H2 {i+1}: {h2.get_text().strip()}")

    print("\n=== ALL CLASSES CONTAINING 'doc', 'content', 'markdown', or 'theme' ===")
    all_elements = soup.find_all()
    relevant_classes = set()

    for element in all_elements:
        classes = element.get('class', [])
        if classes:
            for cls in classes:
                if any(keyword in cls.lower() for keyword in ['doc', 'content', 'markdown', 'theme', 'main', 'article']):
                    relevant_classes.add(cls)

    for cls in sorted(relevant_classes):
        elements = soup.find_all(class_=cls)
        print(f"Class '{cls}': {len(elements)} elements")

        # Show first element's content length for key classes
        if elements and any(keyword in cls.lower() for keyword in ['doc', 'content', 'markdown', 'theme']):
            text_content = elements[0].get_text(strip=True)
            print(f"  -> First element text length: {len(text_content)} chars")
            print(f"  -> First 100 chars: {text_content[:100]}...")

    print("\n=== ALL ID ATTRIBUTES CONTAINING RELEVANT TERMS ===")
    relevant_ids = set()
    for element in all_elements:
        id_attr = element.get('id')
        if id_attr and any(keyword in id_attr.lower() for keyword in ['doc', 'content', 'main', 'article']):
            relevant_ids.add(id_attr)

    for id_val in sorted(relevant_ids):
        element = soup.find(id=id_val)
        if element:
            text_content = element.get_text(strip=True)
            print(f"ID '{id_val}': {len(text_content)} chars")

    print("\n=== ARTICLE TAGS ===")
    article_tags = soup.find_all('article')
    for i, article in enumerate(article_tags):
        text_content = article.get_text(strip=True)
        print(f"Article {i+1}: {len(text_content)} chars")
        print(f"  -> First 100 chars: {text_content[:100]}...")

    print("\n=== MAIN TAGS ===")
    main_tags = soup.find_all('main')
    for i, main in enumerate(main_tags):
        text_content = main.get_text(strip=True)
        print(f"Main {i+1}: {len(text_content)} chars")
        print(f"  -> First 100 chars: {text_content[:100]}...")

if __name__ == "__main__":
    debug_html_structure()