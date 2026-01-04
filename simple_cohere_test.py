#!/usr/bin/env python3
"""
Simple test file to test Cohere API connectivity directly
"""
import os
import cohere
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Cohere API key from environment
api_key = os.getenv('COHERE_API_KEY')
if not api_key:
    print("ERROR: COHERE_API_KEY not found in environment variables")
    print("Please make sure your .env file contains the COHERE_API_KEY")
    exit(1)

print("Testing Cohere API connection...")

try:
    # Create Cohere client
    co = cohere.Client(api_key)
    print("✓ Cohere client created successfully")

    # Test embedding generation with a simple query
    print("\nTesting embedding generation...")
    response = co.embed(
        texts=["test query for physical AI"],
        model="embed-multilingual-v2.0",
        input_type="search_query"
    )

    if response.embeddings and len(response.embeddings) > 0:
        embedding = response.embeddings[0]
        print(f"✓ Embedding generated successfully!")
        print(f"✓ Embedding dimensions: {len(embedding)}")
        print(f"✓ Sample values: {embedding[:5]}...")  # Show first 5 values
    else:
        print("✗ No embeddings returned from API")

    print("\n✓ Cohere API test completed successfully!")
    print("The issue might not be with the API key itself, but with other factors like rate limits or account restrictions.")

except cohere.CohereError as e:
    print(f"✗ Cohere API Error: {e}")
    print(f"✗ Error type: {type(e).__name__}")
    print(f"✗ Error message: {str(e)}")

    # Check if it's a 429 error
    if "429" in str(e) or "Too Many Requests" in str(e):
        print("\n⚠️  This is a 429 error - but it might not be rate limiting!")
        print("Possible causes for 429 on new account:")
        print("  - Trial account has low limits")
        print("  - Account needs verification")
        print("  - Geographic restrictions")
        print("  - Account suspended for any reason")
        print("  - Using deprecated model")

except Exception as e:
    print(f"✗ Unexpected error: {e}")
    print(f"✗ Error type: {type(e).__name__}")
    print(f"✗ Error message: {str(e)}")

    # Check if it's a 429 error
    error_str = str(e)
    if "429" in error_str or "Too Many Requests" in error_str:
        print("\n⚠️  This is a 429 error - but it might not be rate limiting!")
        print("Possible causes for 429 on new account:")
        print("  - Trial account has low limits")
        print("  - Account needs verification")
        print("  - Geographic restrictions")
        print("  - Account suspended for any reason")
        print("  - Using deprecated model")