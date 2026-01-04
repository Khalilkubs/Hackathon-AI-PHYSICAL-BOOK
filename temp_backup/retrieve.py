import os
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class RAGSystem:
    def __init__(self):
        # Initialize Cohere client
        self.cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))

        # Initialize Qdrant client
        self.qdrant_client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY")
        )
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME", "book_content")

    def retrieve(self, query: str, top_k: int = 5):
        """
        Retrieve relevant documents from the Qdrant database based on the query
        """
        try:
            # Generate embedding for the query
            response = self.cohere_client.embed(
                texts=[query],
                model="embed-english-v3.0",
                input_type="search_query"
            )
            query_embedding = response.embeddings[0]

            # Search in Qdrant
            search_results = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k
            )

            # Extract relevant information
            results = []
            for result in search_results:
                results.append({
                    "content": result.payload.get("content", ""),
                    "url": result.payload.get("url", ""),
                    "score": result.score
                })

            return results
        except Exception as e:
            print(f"Error during retrieval: {e}")
            return []

    def generate_response(self, query: str, context: str):
        """
        Generate a response using Cohere based on the query and retrieved context
        """
        try:
            prompt = f"""
            Based on the following context, answer the user's question. If the context doesn't contain the information needed to answer the question, please say so.

            Context: {context}

            Question: {query}

            Answer:
            """

            response = self.cohere_client.generate(
                model="command-r-plus",
                prompt=prompt,
                max_tokens=500,
                temperature=0.3
            )

            return response.generations[0].text.strip()
        except Exception as e:
            print(f"Error during generation: {e}")
            return "Sorry, I encountered an error while generating a response."

    def query(self, query: str, top_k: int = 5):
        """
        Main query method that retrieves relevant content and generates a response
        """
        # Retrieve relevant documents
        retrieved_docs = self.retrieve(query, top_k)

        if not retrieved_docs:
            return "Sorry, I couldn't find any relevant information in the book for your query."

        # Combine the content from retrieved documents
        context = "\n\n".join([doc["content"] for doc in retrieved_docs])

        # Generate response based on context
        response = self.generate_response(query, context)

        return response

# For backward compatibility
def retrieve_answer(query: str) -> str:
    rag_system = RAGSystem()
    return rag_system.query(query)