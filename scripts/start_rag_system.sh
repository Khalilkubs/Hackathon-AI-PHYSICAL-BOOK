#!/bin/bash
# Startup script for RAG Chatbot System

set -e

echo "Starting RAG Chatbot System..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed. Attempting to use 'docker compose' (v2)..."
    if ! command -v docker &> /dev/null || ! docker compose version &> /dev/null; then
        echo "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    COMPOSE_CMD="docker compose"
else
    COMPOSE_CMD="docker-compose"
fi

# Start the services
echo "Starting Qdrant, PostgreSQL, and RAG API services..."
$COMPOSE_CMD up -d

echo "Waiting for services to be ready..."
sleep 10

# Populate the database with textbook content
echo "Populating vector database with textbook content..."
$COMPOSE_CMD exec rag-api python /app/populate_rag.py || echo "Could not populate database directly - run separately"

echo "RAG Chatbot System is now running!"
echo "API available at: http://localhost:8000"
echo "Qdrant UI available at: http://localhost:6333"
echo "PostgreSQL available at: localhost:5432"

# Display service status
$COMPOSE_CMD ps