#!/usr/bin/env python3
"""
Check the raw HTML source to understand the content structure
"""
import requests
from bs4 import BeautifulSoup

def check_source_content():
    # Let's check a specific lesson page and look for the actual content
    url = "https://hackathon-ai-physical-book-1ojs.vercel.app/docs/module-1/chapter-1/lesson-1"
    print(f"Checking source content for: {url}")

    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch: {response.status_code}")
        return

    html_text = response.text
    print(f"HTML size: {len(html_text)} characters")

    # Check if the HTML contains actual lesson-specific content
    # Let's look for any content that might be specific to this lesson
    soup = BeautifulSoup(html_text, 'html.parser')

    # Look for any elements that might have the actual lesson content
    # Check for elements with specific classes that Docusaurus uses for content
    possible_content_selectors = [
        'article',
        '[class*="docItem"]',
        '[class*="doc-content"]',
        '[class*="markdown"]',
        '[class*="theme-doc-markdown"]',
        '[class*="theme-content"]',
        '[class*="content"]',
        'main div'
    ]

    print("\n--- Checking different selectors ---")
    for selector in possible_content_selectors:
        elements = soup.select(selector)
        for i, element in enumerate(elements):
            content = element.get_text(strip=True)
            if len(content) > 100:  # Only show substantial content
                tag_name = element.name
                classes = element.get('class', [])
                class_str = ' '.join(classes) if classes else 'no-classes'

                print(f"\nSelector '{selector}', Element {i+1}:")
                print(f"  Tag: {tag_name}, Classes: {class_str}")
                print(f"  Content length: {len(content)} chars")

                # Show first 150 and last 150 characters to see if there's lesson-specific content
                start_content = content[:150].encode('ascii', errors='ignore').decode('ascii')
                end_content = content[-150:].encode('ascii', errors='ignore').decode('ascii') if len(content) > 150 else content.encode('ascii', errors='ignore').decode('ascii')

                print(f"  Start: {start_content}...")
                print(f"  End: ...{end_content}")

                # If this looks like it might have lesson content, break down further
                if 'chapter' in content.lower() or 'lesson' in content.lower() or len(content) > 300:
                    break

    # Let's also check the entire HTML for any lesson-specific keywords
    print("\n--- Searching for lesson-specific content in entire HTML ---")
    lesson_keywords = [
        'introduction to robotics',
        'ros 2',
        'architecture',
        'nodes',
        'topics',
        'services',
        'actions',
        'gazebo',
        'simulation',
        'isaac',
        'vision-language-action',
        'vla'
    ]

    lower_html = html_text.lower()
    found_keywords = []
    for keyword in lesson_keywords:
        if keyword in lower_html:
            found_keywords.append(keyword)
            # Find context around the keyword
            start_idx = lower_html.find(keyword)
            context_start = max(0, start_idx - 100)
            context_end = min(len(html_text), start_idx + len(keyword) + 100)
            context = html_text[context_start:context_end].encode('ascii', errors='ignore').decode('ascii')
            print(f"Found '{keyword}': ...{context}...")

    if not found_keywords:
        print("No specific lesson keywords found in HTML - may be dynamically loaded")
    else:
        print(f"Found keywords: {found_keywords}")

if __name__ == "__main__":
    check_source_content()