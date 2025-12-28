#!/usr/bin/env python3
"""
Test script to see the actual information retrieved by the agent
"""
import os
from dotenv import load_dotenv
from agent import retrieve_content_wrapper

# Load environment variables
load_dotenv()

def test_retrieval():
    """Test the retrieval function directly to see what information is retrieved"""
    print("Testing retrieval function directly...")

    # Test query
    query = "What are the fundamentals of ROS 2?"

    # Call the retrieval function directly
    result = retrieve_content_wrapper(query, top_k=3, threshold=0.3)

    print(f"\nQuery: {query}")
    print(f"Total results: {result.get('total_results', 0)}")
    print(f"Search performed: {result.get('search_performed', False)}")

    if 'error' in result:
        print(f"Error: {result['error']}")
        print(f"Message: {result['message']}")
        return

    results = result.get('results', [])
    for i, res in enumerate(results):
        print(f"\n--- Result {i+1} ---")
        print(f"Chunk ID: {res.get('chunk_id', 'N/A')}")
        print(f"Similarity Score: {res.get('similarity_score', 'N/A')}")
        print(f"Source URL: {res.get('source_url', 'N/A')}")
        print(f"Document Title: {res.get('document_title', 'N/A')}")
        print(f"Chunk Index: {res.get('chunk_index', 'N/A')}")
        content_preview = res.get('content', '')[:500]
        # Handle Unicode characters properly
        try:
            print(f"Content Preview: {content_preview}...")
        except UnicodeEncodeError:
            print(f"Content Preview: {content_preview.encode('utf-8', errors='ignore').decode('utf-8', errors='replace')}...")
        print("-" * 50)

if __name__ == "__main__":
    test_retrieval()