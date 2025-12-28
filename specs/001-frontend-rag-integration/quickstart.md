# Quickstart: Frontend RAG Integration

## Setup Instructions

### 1. Install Dependencies
```bash
pip install fastapi uvicorn python-dotenv
```

### 2. Create the API Server
Create `api.py` in the project root with the FastAPI server implementation that connects to the existing agent.

### 3. Start the API Server
```bash
uvicorn api:app --reload --port 8000
```

### 4. Start the Docusaurus Frontend
```bash
cd docs/docs
npm install
npm run start
```

## API Usage

### Query Endpoint
Send a POST request to `http://localhost:8000/query` with JSON payload:

```json
{
  "query_text": "What are the fundamentals of ROS 2?"
}
```

### Example Response
```json
{
  "response_text": "The fundamentals of ROS 2 include...",
  "sources": [
    {
      "title": "Chapter 1.1: Introduction to ROS 2 Architecture",
      "url": "https://example.com/chapter-1-1"
    }
  ],
  "confidence": 0.85,
  "query": "What are the fundamentals of ROS 2?",
  "timestamp": "2025-12-28T00:30:00Z"
}
```

## Frontend Integration

The Docusaurus frontend can make fetch requests to the API endpoint to get responses from the RAG system. The API supports CORS for localhost development.

## Environment Variables

Ensure the following environment variables are set (same as used by agent.py):
- `OPENROUTER_API_KEY` or `OPEN_API_KEY`
- `COHERE_API_KEY`
- `QDRANT_URL`
- `QDRANT_API_KEY`
- `AGENT_MODEL`