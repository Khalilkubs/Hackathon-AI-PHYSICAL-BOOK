#!/usr/bin/env python3
"""
Create the final URL list with the correct domain based on your original successful test
"""

# Based on your original successful command, the correct domain should be:
# https://hackathon-ai-physical-book-1ojs.vercel.app/docs/

base_url = "https://hackathon-ai-physical-book-1ojs.vercel.app"

# Main book structure URLs
urls = [
    f"{base_url}/docs",
    f"{base_url}/docs/intro",
    f"{base_url}/docs/module-1/intro",
    f"{base_url}/docs/module-1/chapter-1/lesson-1",
    f"{base_url}/docs/module-1/chapter-1/lesson-2",
    f"{base_url}/docs/module-1/chapter-1/lesson-3",
    f"{base_url}/docs/module-1/chapter-1/lesson-4",
    f"{base_url}/docs/module-1/chapter-2/lesson-1",
    f"{base_url}/docs/module-1/chapter-2/lesson-2",
    f"{base_url}/docs/module-1/chapter-2/lesson-3",
    f"{base_url}/docs/module-1/chapter-2/lesson-4",
    f"{base_url}/docs/module-1/chapter-3/lesson-1",
    f"{base_url}/docs/module-1/chapter-3/lesson-2",
    f"{base_url}/docs/module-1/chapter-3/lesson-3",
    f"{base_url}/docs/module-1/chapter-3/lesson-4",
    f"{base_url}/docs/module-2/intro",
    f"{base_url}/docs/module-2/chapter-1/lesson-1",
    f"{base_url}/docs/module-2/chapter-1/lesson-2",
    f"{base_url}/docs/module-2/chapter-1/lesson-3",
    f"{base_url}/docs/module-2/chapter-1/lesson-4",
    f"{base_url}/docs/module-2/chapter-2/lesson-1",
    f"{base_url}/docs/module-2/chapter-2/lesson-2",
    f"{base_url}/docs/module-2/chapter-2/lesson-3",
    f"{base_url}/docs/module-2/chapter-2/lesson-4",
    f"{base_url}/docs/module-2/chapter-3/lesson-1",
    f"{base_url}/docs/module-2/chapter-3/lesson-2",
    f"{base_url}/docs/module-2/chapter-3/lesson-3",
    f"{base_url}/docs/module-2/chapter-3/lesson-4",
    f"{base_url}/docs/module-3/intro",
    f"{base_url}/docs/module-3/chapter-1/lesson-1",
    f"{base_url}/docs/module-3/chapter-1/lesson-2",
    f"{base_url}/docs/module-3/chapter-1/lesson-3",
    f"{base_url}/docs/module-3/chapter-1/lesson-4",
    f"{base_url}/docs/module-3/chapter-2/lesson-1",
    f"{base_url}/docs/module-3/chapter-2/lesson-2",
    f"{base_url}/docs/module-3/chapter-2/lesson-3",
    f"{base_url}/docs/module-3/chapter-2/lesson-4",
    f"{base_url}/docs/module-3/chapter-3/lesson-1",
    f"{base_url}/docs/module-3/chapter-3/lesson-2",
    f"{base_url}/docs/module-3/chapter-3/lesson-3",
    f"{base_url}/docs/module-3/chapter-3/lesson-4",
    f"{base_url}/docs/module-4/intro",
    f"{base_url}/docs/module-4/chapter-1/lesson-1",
    f"{base_url}/docs/module-4/chapter-1/lesson-2",
    f"{base_url}/docs/module-4/chapter-1/lesson-3",
    f"{base_url}/docs/module-4/chapter-1/lesson-4",
    f"{base_url}/docs/module-4/chapter-2/lesson-1",
    f"{base_url}/docs/module-4/chapter-2/lesson-2",
    f"{base_url}/docs/module-4/chapter-2/lesson-3",
    f"{base_url}/docs/module-4/chapter-2/lesson-4",
    f"{base_url}/docs/module-4/chapter-3/lesson-1",
    f"{base_url}/docs/module-4/chapter-3/lesson-2",
    f"{base_url}/docs/module-4/chapter-3/lesson-3",
    f"{base_url}/docs/module-4/chapter-3/lesson-4",
]

# Write to file
with open('final_book_urls.txt', 'w', encoding='utf-8') as f:
    for url in urls:
        f.write(url + '\n')

print(f"Created final_book_urls.txt with {len(urls)} URLs")
print("These use the domain that worked with your original command:")
print("https://hackathon-ai-physical-book-1ojs.vercel.app")