"""
Vector Storage Module for Document Ingestion and Vector Storage System
Interfaces with Qdrant Cloud for storing embeddings with proper metadata
"""

from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Optional, Dict
from src.models import Embedding
import logging

logger = logging.getLogger(__name__)


class VectorStorage:
    """
    Class to interface with Qdrant Cloud for storing embeddings
    """

    def __init__(self, url: str, api_key: str, collection_name: str = "document_embeddings"):
        """
        Initialize the vector storage

        Args:
            url: Qdrant Cloud URL
            api_key: Qdrant API key
            collection_name: Name of the collection to store embeddings in
        """
        self.client = QdrantClient(url=url, api_key=api_key)
        self.collection_name = collection_name

    def create_collection(self, vector_size: int = 1024):
        """
        Create a collection in Qdrant for document embeddings

        Args:
            vector_size: Size of the embedding vectors (default: 1024 for Cohere)
        """
        try:
            # Check if collection already exists
            collections = self.client.get_collections()
            collection_exists = any(col.name == self.collection_name for col in collections.collections)

            if not collection_exists:
                # Create collection with specified vector size for embeddings
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=vector_size,
                        distance=models.Distance.COSINE  # Cosine distance for similarity search
                    )
                )

                # Create payload index for efficient filtering
                self.client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name="source_url",
                    field_schema=models.PayloadSchemaType.KEYWORD
                )

                self.client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name="document_title",
                    field_schema=models.PayloadSchemaType.TEXT
                )

                self.client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name="chunk_index",
                    field_schema=models.PayloadSchemaType.INTEGER
                )

                # Create payload index for content field
                self.client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name="content",
                    field_schema=models.PayloadSchemaType.TEXT
                )

                logger.info(f"Created collection '{self.collection_name}' with {vector_size}-dimensional vectors")
            else:
                logger.info(f"Collection '{self.collection_name}' already exists")
                # Check the existing collection's vector size to verify compatibility
                collection_info = self.client.get_collection(self.collection_name)
                existing_size = collection_info.config.params.vectors.size
                if existing_size != vector_size:
                    logger.warning(f"Collection '{self.collection_name}' exists with {existing_size}-dimensional vectors, but expected {vector_size}")

        except Exception as e:
            logger.error(f"Error creating collection '{self.collection_name}': {e}")
            raise

    def store_embeddings(self, embeddings: List[Embedding]) -> bool:
        """
        Store embeddings in Qdrant with proper metadata

        Args:
            embeddings: List of Embedding objects to store

        Returns:
            True if storage was successful, False otherwise
        """
        if not embeddings:
            logger.warning("No embeddings to store")
            return True

        try:
            # Check the vector size of the first embedding to determine compatibility
            first_embedding_size = len(embeddings[0].vector) if embeddings else 0

            # Check if collection exists and has correct dimensions
            collection_exists = False
            existing_size = 0
            try:
                collection_info = self.client.get_collection(self.collection_name)
                existing_size = collection_info.config.params.vectors.size
                collection_exists = True
            except:
                # Collection doesn't exist, we'll create it
                collection_exists = False

            # If collection exists but has wrong dimensions, we need to handle this
            if collection_exists and existing_size != first_embedding_size:
                logger.error(f"Collection '{self.collection_name}' has {existing_size}-dimensional vectors, but embeddings have {first_embedding_size} dimensions. Collection must be recreated.")
                return False

            # Prepare points for insertion
            points = []
            for embedding in embeddings:
                # Validate embedding before storing
                try:
                    embedding.validate()
                except ValueError as e:
                    logger.error(f"Embedding validation failed for {embedding.id}: {e}")
                    continue

                # Check if the embedding vector has the right dimensions for the collection
                if collection_exists and len(embedding.vector) != existing_size:
                    logger.error(f"Embedding vector has {len(embedding.vector)} dimensions, but collection expects {existing_size}")
                    continue

                point = models.PointStruct(
                    id=embedding.id,
                    vector=embedding.vector,
                    payload={
                        "chunk_id": embedding.chunk_id,
                        "content": embedding.metadata.get("content", ""),  # Store the actual content
                        "source_url": embedding.metadata.get("source_url", ""),
                        "document_title": embedding.metadata.get("document_title", ""),
                        "chunk_index": embedding.metadata.get("chunk_index", 0),
                        "token_count": embedding.metadata.get("token_count", 0),
                        "created_at": embedding.created_at.isoformat() if embedding.created_at else ""
                    }
                )
                points.append(point)

            if not points:
                logger.warning("No valid embeddings to store after validation")
                return False

            # Upload points to Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

            logger.info(f"Successfully stored {len(points)} embeddings in collection '{self.collection_name}'")
            return True

        except Exception as e:
            # Check if the error is due to dimension mismatch
            error_msg = str(e).lower()
            if "dimension" in error_msg or "vector" in error_msg:
                logger.error(f"Vector dimension error storing embeddings: {e}")
                logger.info("This typically means the Qdrant collection was created with different vector dimensions than the embeddings being stored.")
                logger.info("The collection may need to be deleted and recreated with the correct dimensions.")
            else:
                logger.error(f"Error storing embeddings in collection '{self.collection_name}': {e}")
            return False

    def search_similar(self, query_embedding: List[float], top_k: int = 5, filters: Optional[Dict] = None) -> List[Dict]:
        """
        Search for similar embeddings using vector similarity

        Args:
            query_embedding: The embedding vector to search for similarity
            top_k: Number of results to return
            filters: Optional filters for the search

        Returns:
            List of dictionaries containing search results
        """
        try:
            # Prepare filters if provided
            search_filter = None
            if filters:
                conditions = []
                for key, value in filters.items():
                    if isinstance(value, str):
                        conditions.append(models.FieldCondition(
                            key=key,
                            match=models.MatchValue(value=value)
                        ))
                    elif isinstance(value, int):
                        conditions.append(models.FieldCondition(
                            key=key,
                            range=models.Range(gte=value, lte=value)
                        ))

                if conditions:
                    search_filter = models.Filter(must=conditions)

            # Perform search
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k,
                query_filter=search_filter
            )

            # Format results
            results = []
            for hit in search_results:
                result = {
                    "chunk_id": hit.payload.get("chunk_id", ""),
                    "similarity_score": hit.score,
                    "content": hit.payload.get("content", ""),  # This would be populated if stored
                    "source_url": hit.payload.get("source_url", ""),
                    "document_title": hit.payload.get("document_title", ""),
                    "chunk_index": hit.payload.get("chunk_index", 0)
                }
                results.append(result)

            logger.info(f"Search returned {len(results)} results")
            return results

        except Exception as e:
            logger.error(f"Error performing similarity search: {e}")
            return []

    def recreate_collection(self, vector_size: int) -> bool:
        """
        Recreate the collection with specified vector size (deletes existing data)

        Args:
            vector_size: Size of the embedding vectors for the new collection

        Returns:
            True if recreation was successful, False otherwise
        """
        try:
            # Delete the existing collection
            try:
                self.client.delete_collection(self.collection_name)
                logger.info(f"Deleted existing collection '{self.collection_name}'")
            except Exception as e:
                logger.info(f"Collection '{self.collection_name}' didn't exist or couldn't be deleted: {e}")

            # Create new collection with correct dimensions
            self.create_collection(vector_size=vector_size)
            logger.info(f"Recreated collection '{self.collection_name}' with {vector_size}-dimensional vectors")
            return True
        except Exception as e:
            logger.error(f"Error recreating collection '{self.collection_name}': {e}")
            return False

    def check_connection(self) -> bool:
        """
        Check if we can connect to Qdrant

        Returns:
            True if connection is successful, False otherwise
        """
        try:
            # Try to get collection info as a simple connectivity check
            self.client.get_collection(self.collection_name)
            return True
        except Exception as e:
            logger.error(f"Qdrant connection check failed: {e}")
            return False