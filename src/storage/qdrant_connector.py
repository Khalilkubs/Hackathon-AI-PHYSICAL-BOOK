"""
Set up Qdrant client connection and configuration
Task T006: Set up Qdrant client connection and configuration
"""

import os
from typing import Dict, List, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.models import Distance, VectorParams
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class QdrantConfig:
    """Configuration for Qdrant connection"""
    def __init__(self):
        self.url = os.getenv('QDRANT_URL')
        self.api_key = os.getenv('QDRANT_API_KEY')
        self.collection_name = os.getenv('QDRANT_COLLECTION_NAME', 'document_embeddings')
        self.vector_size = int(os.getenv('VECTOR_SIZE', '1024'))  # Default to 1024 for Cohere embeddings
        self.distance = Distance.COSINE


class QdrantConnector:
    """Implements Qdrant client connection and configuration"""

    def __init__(self, config: QdrantConfig):
        self.config = config
        self.client = QdrantClient(
            url=config.url,
            api_key=config.api_key,
            # Prefer_grpc=True for better performance
        )
        self.collection_name = config.collection_name

    def validate_connection(self) -> bool:
        """Validate Qdrant connection and collection availability"""
        try:
            # Try to get collection info to verify connection
            collection_info = self.client.get_collection(self.collection_name)
            logger.info(f"Successfully connected to Qdrant collection: {self.collection_name}")
            logger.info(f"Collection vector size: {collection_info.config.params.vectors.size}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Qdrant: {e}")
            return False

    def create_collection_if_not_exists(self) -> bool:
        """Create the collection if it doesn't exist"""
        try:
            # Check if collection exists
            try:
                self.client.get_collection(self.collection_name)
                logger.info(f"Collection {self.collection_name} already exists")
                return True
            except:
                # Collection doesn't exist, create it
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.config.vector_size,
                        distance=self.config.distance
                    )
                )
                logger.info(f"Created collection {self.collection_name} with {self.config.vector_size}-dimension vector")
                return True
        except Exception as e:
            logger.error(f"Failed to create collection {self.collection_name}: {e}")
            return False

    def get_vector_size(self) -> Optional[int]:
        """Get the vector size of the collection"""
        try:
            collection_info = self.client.get_collection(self.collection_name)
            return collection_info.config.params.vectors.size
        except Exception as e:
            logger.error(f"Failed to get vector size: {e}")
            return None

    def store_embeddings(self, embeddings: List[Dict]) -> bool:
        """Store embeddings in the Qdrant collection"""
        try:
            points = []
            for emb in embeddings:
                point = models.PointStruct(
                    id=emb['id'],
                    vector=emb['vector'],
                    payload={
                        'chunk_id': emb['chunk_id'],
                        'source_url': emb['source_url'],
                        'document_title': emb['document_title'],
                        'chunk_index': emb['chunk_index'],
                        'created_at': emb.get('created_at', datetime.now().isoformat()),
                        'content': emb.get('content', '')  # Store content for retrieval
                    }
                )
                points.append(point)

            # Upload points to the collection
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

            logger.info(f"Successfully stored {len(points)} embeddings in Qdrant")
            return True
        except Exception as e:
            logger.error(f"Failed to store embeddings in Qdrant: {e}")
            return False

    def search_similar(self, query_vector: List[float], top_k: int = 5) -> List[Dict]:
        """Perform similarity search in Qdrant to retrieve top-k results"""
        try:
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=top_k
            )

            formatted_results = []
            for hit in search_results:
                result = {
                    "chunk_id": hit.payload.get("chunk_id", ""),
                    "similarity_score": hit.score,
                    "content": hit.payload.get("content", ""),
                    "source_url": hit.payload.get("source_url", ""),
                    "document_title": hit.payload.get("document_title", ""),
                    "chunk_index": hit.payload.get("chunk_index", 0),
                    "id": hit.id
                }
                formatted_results.append(result)

            logger.info(f"Search returned {len(formatted_results)} results")
            return formatted_results
        except Exception as e:
            logger.error(f"Error performing similarity search: {e}")
            return []