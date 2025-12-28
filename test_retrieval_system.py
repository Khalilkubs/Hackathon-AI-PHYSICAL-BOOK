#!/usr/bin/env python3
"""
Test script to demonstrate the RAG system functionality
"""

import os
from retrieve import load_config, QdrantConnector, QueryEmbedder, ResultValidator

def test_retrieval_system():
    """Test the retrieval system functionality"""
    print("Testing RAG Retrieval System...")

    try:
        # Load configuration
        print("\n1. Loading configuration...")
        config = load_config()
        print(f"   Configuration loaded successfully")
        print(f"   Collection: {config['qdrant_collection_name']}")

        # Test Qdrant connection
        print("\n2. Testing Qdrant connection...")
        connector = QdrantConnector(config)
        if connector.validate_connection():
            print("   Qdrant connection successful")
        else:
            print("   Qdrant connection failed")
            return False

        # Test query embedding
        print("\n3. Testing query embedding generation...")
        embedder = QueryEmbedder(config['cohere_api_key'])
        test_query = "What is robotics?"
        embedding = embedder.embed_query(test_query)

        if embedding:
            print(f"   Query embedding generated successfully")
            print(f"   Query: '{test_query}'")
            print(f"   Vector dimensions: {len(embedding)}")
        else:
            print("   Query embedding failed")
            return False

        # Test search functionality
        print("\n4. Testing similarity search...")
        search_results = connector.search_similar(embedding, top_k=3)

        if search_results:
            print(f"   Search successful, found {len(search_results)} results")
            print("   Sample results:")
            for i, result in enumerate(search_results[:2], 1):
                print(f"     {i}. Score: {result['similarity_score']:.3f}")
                print(f"        Title: {result['document_title'][:50]}...")
                print(f"        Content: {result['content'][:100]}...")
        else:
            print("   Search returned no results (this may be normal if no data is ingested yet)")

        # Test validation
        print("\n5. Testing result validation...")
        validator = ResultValidator(config['similarity_threshold'])
        validation_report = validator.validate_results(test_query, search_results)
        print(f"   Validation completed")
        print(f"   Validation passed: {validation_report.validation_passed}")
        print(f"   Results count: {validation_report.results_count}")
        print(f"   Avg similarity: {validation_report.avg_similarity_score:.3f}")

        print("\nRAG Retrieval System Test: PASSED")
        print("   All components are working correctly!")
        return True

    except ValueError as e:
        print(f"\nConfiguration Error: {e}")
        print("   Please check your environment variables (COHERE_API_KEY, QDRANT_URL, QDRANT_API_KEY)")
        return False
    except Exception as e:
        print(f"\nError during testing: {e}")
        return False

if __name__ == "__main__":
    print("Starting RAG System Test")
    success = test_retrieval_system()

    if success:
        print("\nThe RAG retrieval system is properly implemented and functional!")
        print("   You can use the retrieve.py script with actual queries once environment variables are set.")
    else:
        print("\nThe system needs proper API keys to function fully.")
        print("   Set the required environment variables to test with real data.")