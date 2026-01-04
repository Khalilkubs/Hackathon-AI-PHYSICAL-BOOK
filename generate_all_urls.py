#!/usr/bin/env python3
"""
Script to generate all possible URLs for the Physical AI book based on the observed structure
"""
import requests
from urllib.parse import urljoin

def generate_book_urls():
    base_url = "https://hackathon-ai-physical-book-1ojs.vercel.app"

    urls = []

    # Main intro pages
    urls.extend([
        f"{base_url}/docs",
        f"{base_url}/docs/intro",
    ])

    # Module intro pages
    for module in range(1, 5):
        urls.append(f"{base_url}/docs/module-{module}/intro")

    # Generate lesson URLs based on the pattern observed
    # From the existing files, we know there are lessons structured like:
    # /docs/module-X/chapter-Y/lesson-Z

    # Let's create a comprehensive list based on typical book structure
    module_chapters = {
        1: 3,  # Module 1 has 3 chapters
        2: 3,  # Module 2 has 3 chapters
        3: 3,  # Module 3 has 3 chapters
        4: 3   # Module 4 has 3 chapters
    }

    # Number of lessons per chapter (this is estimated based on typical structure)
    lessons_per_chapter = {
        (1, 1): 4,  # Module 1, Chapter 1 has 4 lessons
        (1, 2): 4,  # Module 1, Chapter 2 has 4 lessons
        (1, 3): 4,  # Module 1, Chapter 3 has 4 lessons
        (2, 1): 4,  # Module 2, Chapter 1 has 4 lessons
        (2, 2): 4,  # Module 2, Chapter 2 has 4 lessons
        (2, 3): 4,  # Module 2, Chapter 3 has 4 lessons
        (3, 1): 4,  # Module 3, Chapter 1 has 4 lessons
        (3, 2): 4,  # Module 3, Chapter 2 has 4 lessons
        (3, 3): 4,  # Module 3, Chapter 3 has 4 lessons
        (4, 1): 4,  # Module 4, Chapter 1 has 4 lessons
        (4, 2): 4,  # Module 4, Chapter 2 has 4 lessons
        (4, 3): 4,  # Module 4, Chapter 3 has 4 lessons
    }

    # Generate all lesson URLs
    for module in range(1, 5):
        for chapter in range(1, module_chapters[module] + 1):
            for lesson in range(1, lessons_per_chapter[(module, chapter)] + 1):
                urls.append(f"{base_url}/docs/module-{module}/chapter-{chapter}/lesson-{lesson}")

    # Add module-specific intro pages (these might be the same as the module intros)
    for module in range(1, 5):
        urls.append(f"{base_url}/docs/module-{module}/")

    # Remove duplicates while preserving order
    unique_urls = []
    seen = set()
    for url in urls:
        if url not in seen:
            unique_urls.append(url)
            seen.add(url)

    return unique_urls

def main():
    urls = generate_book_urls()

    print(f"Generated {len(urls)} URLs:")
    for i, url in enumerate(urls, 1):
        print(f"{i:3d}. {url}")

    # Write to file
    with open("all_book_urls.txt", "w") as f:
        for url in urls:
            f.write(f"{url}\n")

    print(f"\nURLs saved to all_book_urls.txt")

if __name__ == "__main__":
    main()