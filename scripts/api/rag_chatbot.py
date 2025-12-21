"""
RAG Chatbot using FastAPI, Neon Postgres, and Qdrant
This implements a Retrieval-Augmented Generation system for the Physical AI & Humanoid Robotics textbook
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import asyncio
import logging
from contextlib import asynccontextmanager

# Import required libraries
try:
    import psycopg
    from qdrant_client import QdrantClient
    from qdrant_client.http import models
    import openai
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("Required packages not found. Please install: psycopg, qdrant-client, openai, sentence-transformers")

app = FastAPI(
    title="Physical AI & Humanoid Robotics RAG Chatbot",
    description="Retrieval-Augmented Generation system for the Physical AI & Humanoid Robotics textbook",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
QDRANT_HOST = "localhost"  # Change to your Qdrant server address
QDRANT_PORT = 6333
NEON_DB_URL = "postgresql://user:password@localhost:5432/rag_db"  # Update with your Neon DB URL
OPENAI_API_KEY = ""  # Set your OpenAI API key

# Global variables for clients
qdrant_client = None
neon_pool = None
embedding_model = None

class QueryRequest(BaseModel):
    query: str
    max_results: int = 5
    similarity_threshold: float = 0.7

class QueryResponse(BaseModel):
    query: str
    response: str
    sources: List[Dict]
    confidence: float

class Document(BaseModel):
    id: str
    content: str
    metadata: Dict
    embedding: Optional[List[float]] = None

class DocumentResponse(BaseModel):
    success: bool
    message: str
    document_id: Optional[str] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler to initialize and cleanup resources
    """
    global qdrant_client, neon_pool, embedding_model

    logger.info("Initializing RAG chatbot resources...")

    try:
        # Initialize Qdrant client
        qdrant_client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

        # Initialize embedding model
        embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

        # Check if collection exists, create if not
        collection_name = "textbook_content"
        try:
            qdrant_client.get_collection(collection_name)
            logger.info(f"Collection '{collection_name}' already exists")
        except:
            # Create collection for embeddings
            qdrant_client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE)
            )
            logger.info(f"Created collection '{collection_name}'")

        logger.info("RAG chatbot resources initialized successfully")
        yield

    except Exception as e:
        logger.error(f"Error initializing RAG chatbot: {str(e)}")
        raise
    finally:
        logger.info("Cleaning up RAG chatbot resources...")
        # Cleanup resources if needed
        if qdrant_client:
            del qdrant_client
        if neon_pool:
            await neon_pool.close()

@app.get("/")
async def root():
    return {"message": "Physical AI & Humanoid Robotics RAG Chatbot API"}

@app.post("/documents", response_model=DocumentResponse)
async def add_document(document: Document):
    """
    Add a document to the vector database for retrieval
    """
    try:
        # Generate embedding if not provided
        if document.embedding is None:
            embedding = embedding_model.encode(document.content).tolist()
        else:
            embedding = document.embedding

        # Store in Qdrant
        qdrant_client.upsert(
            collection_name="textbook_content",
            points=[
                models.PointStruct(
                    id=document.id,
                    vector=embedding,
                    payload={
                        "content": document.content,
                        "metadata": document.metadata
                    }
                )
            ]
        )

        logger.info(f"Added document {document.id} to vector database")

        return DocumentResponse(
            success=True,
            message=f"Document {document.id} added successfully",
            document_id=document.id
        )

    except Exception as e:
        logger.error(f"Error adding document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """
    Query the RAG system to get relevant information and generate response
    """
    try:
        # Generate embedding for the query
        query_embedding = embedding_model.encode(request.query).tolist()

        # Search in Qdrant for similar documents
        search_result = qdrant_client.search(
            collection_name="textbook_content",
            query_vector=query_embedding,
            limit=request.max_results,
            score_threshold=request.similarity_threshold
        )

        # Extract relevant content
        relevant_content = []
        sources = []

        for hit in search_result:
            if hit.score >= request.similarity_threshold:
                content = hit.payload.get("content", "")
                metadata = hit.payload.get("metadata", {})

                relevant_content.append(content)
                sources.append({
                    "id": hit.id,
                    "score": hit.score,
                    "metadata": metadata
                })

        if not relevant_content:
            return QueryResponse(
                query=request.query,
                response="I couldn't find relevant information in the textbook to answer your question.",
                sources=[],
                confidence=0.0
            )

        # Prepare context for LLM
        context = "\n\n".join(relevant_content[:3])  # Use top 3 most relevant
        prompt = f"""
        You are an expert assistant for the Physical AI & Humanoid Robotics textbook.
        Use the following context to answer the user's question.
        If the context doesn't contain enough information, say so.

        Context:
        {context}

        Question: {request.query}

        Answer:
        """

        # Generate response using OpenAI (or alternative)
        # For this implementation, we'll simulate the response
        # In a real implementation, you would use OpenAI API or local LLM

        simulated_response = f"Based on the textbook content, here's what I found regarding: {request.query}. This is a simulated response from the RAG system. In a full implementation, this would be generated by an LLM using the retrieved context."

        # Calculate average confidence from top results
        avg_confidence = sum([source['score'] for source in sources]) / len(sources) if sources else 0.0

        return QueryResponse(
            query=request.query,
            response=simulated_response,
            sources=sources,
            confidence=avg_confidence
        )

    except Exception as e:
        logger.error(f"Error querying documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "service": "RAG Chatbot API",
        "components": {
            "qdrant": "connected" if qdrant_client else "disconnected",
            "embedding_model": "loaded" if embedding_model else "not loaded"
        }
    }

@app.delete("/documents/{doc_id}")
async def delete_document(doc_id: str):
    """
    Delete a document from the vector database
    """
    try:
        qdrant_client.delete(
            collection_name="textbook_content",
            points_selector=models.PointIdsList(
                points=[doc_id]
            )
        )

        logger.info(f"Deleted document {doc_id} from vector database")

        return {"success": True, "message": f"Document {doc_id} deleted successfully"}

    except Exception as e:
        logger.error(f"Error deleting document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)