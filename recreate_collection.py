#!/usr/bin/env python3
"""
Script to recreate Qdrant collection with correct vector dimensions
"""
import os
from dotenv import load_dotenv
from src.storage import VectorStorage

# Load environment variables
load_dotenv()

def main():
    # Load configuration
    qdrant_url = os.getenv('QDRANT_URL')
    qdrant_api_key = os.getenv('QDRANT_API_KEY')

    if not qdrant_url or not qdrant_api_key:
        print("Error: QDRANT_URL and QDRANT_API_KEY must be set in .env file")
        return

    # Create VectorStorage instance
    storage = VectorStorage(
        url=qdrant_url,
        api_key=qdrant_api_key,
        collection_name="document_embeddings"
    )

    print("Recreating collection with 1024-dimensional vectors...")

    # Recreate collection with 1024 dimensions (correct for Cohere embed-multilingual-v2.0)
    success = storage.recreate_collection(vector_size=1024)

    if success:
        print("✅ Collection successfully recreated with 1024-dimensional vectors!")
        print("Now you can run the ingestion process again.")
    else:
        print("❌ Failed to recreate collection. Check the logs above for details.")

if __name__ == "__main__":
    main()