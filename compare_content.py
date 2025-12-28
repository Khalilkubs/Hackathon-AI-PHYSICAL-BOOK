#!/usr/bin/env python3
"""
Compare content from different lesson pages to see if they're actually different
"""
import requests
from bs4 import BeautifulSoup

def compare_content():
    urls = [
        "https://hackathon-ai-physical-book-1ojs.vercel.app/docs/module-1/chapter-1/lesson-1",
        "https://hackathon-ai-physical-book-1ojs.vercel.app/docs/module-1/chapter-2/lesson-1",
        "https://hackathon-ai-physical-book-1ojs.vercel.app/docs/module-2/chapter-1/lesson-1"
    ]

    for i, url in enumerate(urls, 1):
        print(f"\n--- Page {i}: {url} ---")

        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch: {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the main content area
        main_element = soup.find('main')
        if main_element:
            # Look for the div with 'container' class (from our previous discovery)
            container_div = main_element.find('div', class_='container')
            if container_div:
                content = container_div.get_text(strip=True)
                safe_content = content.encode('ascii', errors='ignore').decode('ascii')
                print(f"Container div content: {len(content)} chars")
                print(f"Preview: {safe_content[:200]}...")
            else:
                content = main_element.get_text(strip=True)
                safe_content = content.encode('ascii', errors='ignore').decode('ascii')
                print(f"Main element content: {len(content)} chars")
                print(f"Preview: {safe_content[:200]}...")

        # Also check for any article tags which might contain the actual lesson content
        articles = soup.find_all('article')
        for j, article in enumerate(articles):
            article_content = article.get_text(strip=True)
            if len(article_content) > 100:
                safe_article_content = article_content.encode('ascii', errors='ignore').decode('ascii')
                print(f"Article {j+1} content: {len(article_content)} chars")
                print(f"Preview: {safe_article_content[:200]}...")

if __name__ == "__main__":
    compare_content()