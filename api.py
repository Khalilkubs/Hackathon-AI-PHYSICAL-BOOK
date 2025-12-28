#!/usr/bin/env python3
"""
FastAPI server for Frontend RAG Integration
Exposes a query endpoint that connects to the existing RAG agent
"""
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from typing import Optional, List, Dict
import json
import asyncio
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Validate required environment variables for the agent
required_env_vars = [
    'OPENROUTER_API_KEY',
    'COHERE_API_KEY',
    'QDRANT_URL',
    'QDRANT_API_KEY',
    'AGENT_MODEL'
]

missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    logger.warning(f"Missing required environment variables: {', '.join(missing_vars)}")
    logger.warning("Some functionality may not work without these variables.")
else:
    logger.info("All required environment variables are present")

# Import required libraries
try:
    from fastapi import FastAPI, HTTPException, Depends
    from fastapi.middleware.cors import CORSMiddleware
    import uvicorn
    from pydantic import BaseModel
    # Import from existing agent.py
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # Add current directory to path
    from agent import create_agent_with_tools, process_user_query_with_agents_sdk
except ImportError as e:
    print(f"Missing required dependency: {e}")
    print("Please install required dependencies using: pip install fastapi uvicorn python-dotenv")
    exit(1)

# Pydantic models for request/response
class QueryRequest(BaseModel):
    """Input model for query requests"""
    query_text: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    metadata: Optional[Dict] = None

class QueryResponse(BaseModel):
    """Output model for query responses"""
    response_text: str
    sources: Optional[List[Dict]] = None
    confidence: Optional[float] = None
    query: str
    timestamp: str
    retrieved_chunks: Optional[List[Dict]] = None

class APIError(BaseModel):
    """Error response model"""
    error_code: str
    message: str
    timestamp: str
    details: Optional[Dict] = None

# Initialize FastAPI app
app = FastAPI(
    title="Frontend RAG Integration API",
    description="API for connecting Docusaurus frontend with RAG agent",
    version="1.0.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
QUERY_TIMEOUT = 30  # 30 seconds timeout for queries

async def process_query_with_agent(query_text: str) -> str:
    """
    Process query using the existing RAG agent from agent.py with timeout
    """
    logger.info(f"Processing query: {query_text[:50]}...")  # Log first 50 chars of query
    try:
        # Use asyncio.wait_for to implement timeout
        result = await asyncio.wait_for(
            asyncio.get_event_loop().run_in_executor(None, process_user_query_with_agents_sdk, query_text),
            timeout=QUERY_TIMEOUT
        )
        logger.info("Query processed successfully")
        return result
    except asyncio.TimeoutError:
        logger.error(f"Query processing timed out after {QUERY_TIMEOUT} seconds")
        raise HTTPException(status_code=408, detail=f"Query processing timed out after {QUERY_TIMEOUT} seconds")
    except Exception as e:
        logger.error(f"Error processing query with agent: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query with agent: {str(e)}")

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(query_request: QueryRequest):
    """
    Process a user query against the RAG system
    """
    logger.info(f"Received query request for: {query_request.query_text[:50]}...")
    try:
        # Validate query text
        if not query_request.query_text or not query_request.query_text.strip():
            logger.warning("Received empty query")
            raise HTTPException(status_code=400, detail="Query text cannot be empty")

        # Validate query length to prevent extremely long queries
        if len(query_request.query_text) > 1000:  # Limit to 1000 characters
            logger.warning(f"Received query too long: {len(query_request.query_text)} characters")
            raise HTTPException(status_code=400, detail="Query text is too long (max 1000 characters)")

        # Process the query with the RAG agent
        response_text = await process_query_with_agent(query_request.query_text)

        # Create response with timestamp
        timestamp = datetime.utcnow().isoformat() + "Z"

        # Log successful completion
        logger.info(f"Query processed successfully, response length: {len(response_text)}")

        # Return response in the expected format
        return QueryResponse(
            response_text=response_text,
            sources=[],  # Will be populated by the agent if available
            confidence=0.8,  # Default confidence - actual implementation may vary
            query=query_request.query_text,
            timestamp=timestamp,
            retrieved_chunks=[]  # Will be populated by the agent if available
        )
    except HTTPException:
        # HTTPException is already logged by FastAPI
        raise
    except Exception as e:
        # Log the error for debugging
        logger.error(f"Error in query endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")
        
@app.get("/")
async def root():
    return {"message": "Welcome to Physical AI & Humanoid Robotics Book API"}


@app.get("/health")
async def health_check():
    """Health check endpoint to verify API is running"""
    return {"status": "healthy", "service": "frontend-rag-integration-api"}

@app.get("/test")
async def test_endpoint():
    """Test endpoint to verify query functionality with a sample query"""
    try:
        # Test with a simple query
        test_query = QueryRequest(query_text="What are the fundamentals of ROS 2?")
        result = await process_query_with_agent(test_query.query_text)

        return QueryResponse(
            response_text=result,
            sources=[],  # Will be populated by the agent if available
            confidence=0.8,  # Default confidence
            query=test_query.query_text,
            timestamp=datetime.utcnow().isoformat() + "Z",
            retrieved_chunks=[]  # Will be populated by the agent if available
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test failed: {str(e)}")

@app.post("/validate-query")
async def validate_query(query_request: QueryRequest):
    """Validate query without processing it, for testing validation logic"""
    try:
        # Validate query text
        if not query_request.query_text or not query_request.query_text.strip():
            raise HTTPException(status_code=400, detail="Query text cannot be empty")

        # Validate query length to prevent extremely long queries
        if len(query_request.query_text) > 1000:  # Limit to 1000 characters
            raise HTTPException(status_code=400, detail="Query text is too long (max 1000 characters)")

        return {"status": "valid", "message": "Query passed validation"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)