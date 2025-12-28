#!/usr/bin/env python3
"""
Simple RAG Query Interface for Physical AI & Humanoid Robotics Book
Directly queries the Qdrant vector database without Docker
"""
import os
import sys
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict, Optional

# Load environment variables
load_dotenv()

class SimpleRAGQuery:
    """
    Simple RAG query system that directly accesses Qdrant without Docker
    """

    def __init__(self):
        """Initialize the RAG query system"""
        # Initialize Qdrant client using the same configuration as your system
        self.qdrant_url = os.getenv('QDRANT_URL')
        self.qdrant_api_key = os.getenv('QDRANT_API_KEY')

        if not self.qdrant_url or not self.qdrant_api_key:
            print("ERROR: QDRANT_URL and QDRANT_API_KEY must be set in .env file")
            sys.exit(1)

        self.client = QdrantClient(
            url=self.qdrant_url,
            api_key=self.qdrant_api_key,
            timeout=30
        )

        # Use the same collection name as your system
        self.collection_name = "document_embeddings"  # or "document_embeddings" based on your logs

        # Initialize embedding model (same as your system)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # or 'intfloat/e5-small-v2'

        print(f"Connected to Qdrant collection: {self.collection_name}")

    def query(self, question: str, top_k: int = 5, threshold: float = 0.3) -> List[Dict]:
        """
        Query the vector database for relevant content

        Args:
            question: The question to search for
            top_k: Number of top results to return
            threshold: Similarity threshold for results

        Returns:
            List of dictionaries with content and metadata
        """
        # Generate embedding for the question
        query_embedding = self.model.encode(question).tolist()

        # Search in Qdrant
        try:
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k,
                score_threshold=threshold
            )

            results = []
            for hit in search_results:
                result = {
                    'id': hit.id,
                    'content': hit.payload.get('content', '')[:500] + '...' if len(hit.payload.get('content', '')) > 500 else hit.payload.get('content', ''),
                    'source_url': hit.payload.get('source_url', 'Unknown'),
                    'score': hit.score,
                    'metadata': hit.payload.get('metadata', {})
                }
                results.append(result)

            return results

        except Exception as e:
            print(f"Error querying Qdrant: {e}")
            return []

    def print_query_results(self, question: str, results: List[Dict]):
        """
        Print query results in a readable format
        """
        print(f"\n❓ QUESTION: {question}")
        print(f"📊 FOUND {len(results)} relevant results")
        print("="*80)

        for i, result in enumerate(results, 1):
            print(f"\nResult {i} (Score: {result['score']:.3f}):")
            print(f"📄 Source: {result['source_url']}")
            print(f"📝 Content Preview: {result['content']}")
            if result['metadata']:
                print(f"📋 Metadata: {result['metadata']}")
            print("-" * 80)

def main():
    print("🚀 Starting Simple RAG Query System for Physical AI & Humanoid Robotics Book")
    print("📚 Query the complete Physical AI & Humanoid Robotics textbook content")
    print("   (All 64 lessons have been successfully ingested with unique content)")
    print()

    # Initialize the RAG system
    try:
        rag = SimpleRAGQuery()
    except Exception as e:
        print(f"❌ Failed to initialize RAG system: {e}")
        print("Make sure your Qdrant is accessible and credentials are correct in .env")
        return

    print("✅ RAG system initialized successfully!")
    print("💡 Enter questions about Physical AI, ROS 2, Humanoid Robotics, etc.")
    print("   Type 'quit' or 'exit' to stop\n")

    # Sample questions you can ask:
    sample_questions = [
        "What are the fundamentals of ROS 2?",
        "Explain computer vision for robotics",
        "What is NVIDIA Isaac platform?",
        "How do Vision-Language-Action models work?",
        "What are the key concepts of humanoid robotics?",
        "Explain Gazebo simulation for robotics"
    ]

    print("🎯 Sample questions you can ask:")
    for i, q in enumerate(sample_questions, 1):
        print(f"   {i}. {q}")
    print()

    while True:
        try:
            question = input("💬 Enter your question: ").strip()

            if question.lower() in ['quit', 'exit', 'stop', 'q']:
                print("👋 Goodbye! Thanks for using the Physical AI RAG system.")
                break

            if not question:
                continue

            # Query the RAG system
            results = rag.query(question, top_k=3, threshold=0.3)

            if results:
                rag.print_query_results(question, results)

                # Generate a summary response
                print(f"\n🤖 SUMMARY RESPONSE:")
                print(f"Based on the Physical AI & Humanoid Robotics book, here's what I found:")
                for i, result in enumerate(results[:2], 1):  # Show top 2
                    print(f"  • From {result['source_url'].split('/')[-3:][-1]}: {result['content'][:200]}...")
            else:
                print(f"\n❌ No relevant content found for: '{question}'")
                print("Try rephrasing your question or check if Qdrant connection is working.")

            print("\n" + "="*80 + "\n")

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thanks for using the Physical AI RAG system.")
            break
        except Exception as e:
            print(f"\n❌ Error processing query: {e}")
            continue

if __name__ == "__main__":
    main()