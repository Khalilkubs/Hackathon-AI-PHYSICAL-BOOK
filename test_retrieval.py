#!/usr/bin/env python3
"""
Test script to verify the RAG system is working properly
"""
import os
from dotenv import load_dotenv
from retrieve import retrieve_content_wrapper

# Load environment
load_dotenv()

print("Testing RAG system with query: 'What are the fundamentals of ROS 2?'")
print("="*60)

try:
    # Test the retrieval function
    result = retrieve_content_wrapper("What are the fundamentals of ROS 2?", top_k=3, threshold=0.3)

    if result.get('error'):
        print(f"❌ Error: {result['error']}")
        print(f"   Message: {result['message']}")
    else:
        print(f"✅ Query successful!")
        print(f"   Found {result['total_results']} results")
        print()

        if result['results']:
            print("📊 Top results:")
            for i, res in enumerate(result['results'], 1):
                print(f"   {i}. Score: {res['similarity_score']:.3f}")
                print(f"      Source: {res['source_url']}")
                print(f"      Title: {res['document_title']}")
                print(f"      Content preview: {res['content'][:200]}...")
                print()
        else:
            print("   No relevant content found in the database")

except Exception as e:
    print(f"❌ Error during query: {e}")
    import traceback
    traceback.print_exc()

print("="*60)
print("Test completed!")