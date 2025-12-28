"""
Embedding Generator Module for Document Ingestion and Vector Storage System
Generates embeddings using Cohere Python SDK with error handling
"""

import cohere
from typing import List, Optional
from src.models import TextChunk, Embedding
from uuid import uuid4
import time
import logging

logger = logging.getLogger(__name__)


class EmbeddingGenerator:
    """
    Class to generate embeddings using Cohere API with proper error handling
    """

    def __init__(self, api_key: str, model: str = "embed-multilingual-v2.0"):
        """
        Initialize the embedding generator

        Args:
            api_key: Cohere API key
            model: The embedding model to use (default: embed-multilingual-v2.0)
        """
        self.client = cohere.Client(api_key)
        self.model = model

    def generate_embeddings(self, chunks: List[TextChunk], document_url: str = "", document_title: str = "", batch_size: int = 96) -> List[Embedding]:
        """
        Generate embeddings for a list of text chunks

        Args:
            chunks: List of TextChunk objects to generate embeddings for
            document_url: URL of the source document
            document_title: Title of the source document
            batch_size: Number of chunks to process in each batch (Cohere has limits)

        Returns:
            List of Embedding objects
        """
        if not chunks:
            return []

        embeddings = []

        # Process chunks in batches to respect API limits
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            batch_texts = [chunk.content for chunk in batch]

            try:
                # Generate embeddings for the batch
                response = self.client.embed(
                    texts=batch_texts,
                    model=self.model,
                    input_type="search_document"  # Appropriate for document search
                )

                # Create Embedding objects from the response
                for idx, (chunk, embedding_vector) in enumerate(zip(batch, response.embeddings)):
                    # Update the model to handle different vector dimensions
                    # Create a new embedding with the correct dimensions
                    embedding = Embedding(
                        id=str(uuid4()),
                        chunk_id=chunk.id,
                        vector=embedding_vector,
                        metadata={
                            "content": chunk.content,  # Include the actual content
                            "source_url": document_url,  # Use document URL
                            "document_title": document_title,  # Use document title
                            "chunk_index": chunk.chunk_index,
                            "token_count": chunk.token_count,
                            "vector_dimension": len(embedding_vector)  # Store actual dimension
                        },
                        created_at=None  # Will be set by dataclass
                    )

                    # Validate the embedding - allow different dimensions
                    try:
                        # Temporarily modify validation to allow different dimensions
                        # since the model might return different sizes
                        if not embedding_vector or not isinstance(embedding_vector, list):
                            raise ValueError("Vector must be a valid list")

                        if not all(isinstance(v, (int, float)) and not (v != v) for v in embedding_vector):  # Check for NaN values
                            raise ValueError("Vector must contain only valid numbers (no NaN or infinity)")

                        embeddings.append(embedding)
                    except ValueError as e:
                        logger.error(f"Embedding validation failed for chunk {chunk.id}: {e}")
                        continue

                logger.info(f"Generated embeddings for batch {i//batch_size + 1}/{(len(chunks)-1)//batch_size + 1}")

            except Exception as e:
                # Handle both old and new Cohere API error types
                error_msg = str(e)
                if "401" in error_msg or "Unauthorized" in error_msg:
                    logger.error(f"Authentication error with Cohere API (check your API key): {e}")
                else:
                    logger.error(f"Cohere API error when processing batch {i//batch_size + 1}: {e}")
                # In a production system, you might want to implement more sophisticated retry logic
                continue

        logger.info(f"Generated {len(embeddings)} embeddings from {len(chunks)} text chunks")
        return embeddings

    def generate_single_embedding(self, text: str) -> Optional[List[float]]:
        """
        Generate a single embedding for a piece of text

        Args:
            text: The text to generate an embedding for

        Returns:
            The embedding vector as a list of floats, or None if failed
        """
        try:
            response = self.client.embed(
                texts=[text],
                model=self.model,
                input_type="search_query"  # Appropriate for search queries
            )

            if response.embeddings and len(response.embeddings) > 0:
                return response.embeddings[0]
            else:
                logger.error("No embeddings returned from Cohere API")
                return None

        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg or "Unauthorized" in error_msg:
                logger.error(f"Authentication error with Cohere API (check your API key): {e}")
            else:
                logger.error(f"Error when generating single embedding: {e}")
            return None