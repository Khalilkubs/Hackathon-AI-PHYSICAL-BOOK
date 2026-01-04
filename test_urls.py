#!/usr/bin/env python3
"""
Test script to check which URLs are accessible
"""
import requests
from urllib.parse import urljoin, urlparse

# Load URLs from file
with open('correct_book_urls.txt', 'r', encoding='utf-8') as f:
    urls = [line.strip() for line in f if line.strip()]

print(f"Testing {len(urls)} URLs...")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

accessible_urls = []
not_found_urls = []

for i, url in enumerate(urls[:10], 1):  # Test first 10 URLs
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            print(f"✅ {response.status_code}: {url}")
            accessible_urls.append(url)
        else:
            print(f"❌ {response.status_code}: {url}")
            not_found_urls.append(url)
    except Exception as e:
        print(f"❌ Error: {url} - {str(e)}")
        not_found_urls.append(url)

print(f"\nSummary:")
print(f"Accessible URLs: {len(accessible_urls)}")
print(f"Not Found/Errors: {len(not_found_urls)}")

if accessible_urls:
    print(f"\nFirst few accessible URLs:")
    for url in accessible_urls[:5]:
        print(f"  {url}")