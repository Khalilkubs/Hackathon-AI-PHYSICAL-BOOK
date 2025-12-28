#!/usr/bin/env python3
"""
Check if content is loaded dynamically with JavaScript
"""
import requests
from bs4 import BeautifulSoup

def check_dynamic_content():
    urls = [
        "https://hackathon-ai-physical-book-1ojs.vercel.app/docs/module-1/chapter-1/lesson-1",
        "https://hackathon-ai-physical-book-1ojs.vercel.app/docs/module-1/chapter-2/lesson-1",
        "https://hackathon-ai-physical-book-1ojs.vercel.app/docs/module-2/chapter-1/lesson-1"
    ]

    for i, url in enumerate(urls, 1):
        print(f"\n--- Analyzing {url} ---")

        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch: {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')

        # Look for script tags that might contain dynamic content
        scripts = soup.find_all('script')
        print(f"Found {len(scripts)} script tags")

        # Check for any JSON or data in script tags
        for j, script in enumerate(scripts):
            if script.string and ('{"' in script.string or '[{' in script.string):
                print(f"Script {j+1} contains JSON data")
                json_preview = script.string[:200].encode('ascii', errors='ignore').decode('ascii')
                print(f"Preview: {json_preview}...")

        # Look for any content that might be in data attributes or hidden divs
        all_divs = soup.find_all('div')
        for div in all_divs:
            content = div.get_text(strip=True)
            if len(content) > 50 and 'lesson' in content.lower():
                print(f"Found lesson-related content: {content[:100]}...")

        # Check for specific attributes that might indicate dynamic loading
        data_attrs = soup.find_all(attrs=lambda x: x and any(k.startswith('data-') for k in x.keys()))
        if data_attrs:
            print(f"Found {len(data_attrs)} elements with data attributes")
            for attr_elem in data_attrs[:5]:  # First 5
                elem_content = attr_elem.get_text(strip=True)
                if elem_content and len(elem_content) > 50:
                    safe_content = elem_content.encode('ascii', errors='ignore').decode('ascii')
                    print(f"Data attr element content: {safe_content[:100]}...")

        # Look for content in noscript tags (fallback content)
        noscripts = soup.find_all('noscript')
        for noscript in noscripts:
            noscript_content = noscript.get_text(strip=True)
            if noscript_content:
                safe_content = noscript_content.encode('ascii', errors='ignore').decode('ascii')
                print(f"Noscript content: {safe_content[:200]}...")

if __name__ == "__main__":
    check_dynamic_content()