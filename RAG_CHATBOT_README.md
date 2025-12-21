# RAG Chatbot for Physical AI & Humanoid Robotics Textbook

This RAG (Retrieval-Augmented Generation) chatbot provides an intelligent interface to query the Physical AI & Humanoid Robotics textbook content using natural language.

## Architecture

The system consists of:
- **FastAPI**: Web framework for the API backend
- **Qdrant**: Vector database for semantic search
- **Neon Postgres**: Metadata storage (simulated with PostgreSQL)
- **Sentence Transformers**: For generating text embeddings
- **OpenAI API**: For generating responses (simulated in this implementation)

## Prerequisites

- Docker and Docker Compose
- Python 3.8+
- An OpenAI API key (optional for full functionality)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Hackathon-AI-PHYSICAL-BOOK
```

### 2. Set Environment Variables

Create a `.env` file in the root directory:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Start the System

Run the startup script:

```bash
# On Linux/Mac
chmod +x scripts/start_rag_system.sh
./scripts/start_rag_system.sh

# On Windows (using WSL or Git Bash)
chmod +x scripts/start_rag_system.sh
./scripts/start_rag_system.sh
```

Alternatively, start manually with Docker Compose:

```bash
docker-compose up -d
```

### 4. Populate the Database

The system will automatically populate the vector database with textbook content. If needed, you can run the population script separately:

```bash
python scripts/populate_rag.py
```

## API Endpoints

- `GET /`: Health check and root endpoint
- `POST /documents`: Add a document to the vector database
- `POST /query`: Query the RAG system for information
- `GET /health`: Health check endpoint
- `DELETE /documents/{doc_id}`: Delete a document

### Query Example

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Explain ROS 2 architecture and nodes",
    "max_results": 5,
    "similarity_threshold": 0.7
  }'
```

## Configuration

- **Qdrant**: Runs on `localhost:6333`
- **PostgreSQL**: Runs on `localhost:5432`
- **API**: Runs on `localhost:8000`

## Development

To run the API locally without Docker:

1. Install dependencies:
```bash
pip install -r scripts/api/requirements.txt
```

2. Set environment variables:
```bash
export OPENAI_API_KEY=your_api_key
```

3. Run the API:
```bash
cd scripts/api
uvicorn rag_chatbot:app --reload
```

## Troubleshooting

1. **Docker containers not starting**: Check Docker is running and you have sufficient permissions
2. **Qdrant connection issues**: Verify Qdrant service is running and accessible
3. **Database connection issues**: Check PostgreSQL service is running and credentials are correct
4. **API not responding**: Check the logs with `docker-compose logs rag-api`

## Security Considerations

- In production, restrict CORS origins in `rag_chatbot.py`
- Use environment variables for sensitive configuration
- Implement authentication for document management endpoints
- Use HTTPS in production deployments

## Next Steps

1. Integrate with a real LLM for response generation
2. Add user authentication and authorization
3. Implement rate limiting
4. Add monitoring and logging