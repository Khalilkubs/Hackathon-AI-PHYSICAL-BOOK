# Quickstart: AI Agent with Retrieval-Augmented Capabilities

## Overview
This guide will help you set up and run the AI agent that uses retrieval-augmented generation to answer questions about book content.

## Prerequisites
- Python 3.11 or higher
- OpenAI API key
- Cohere API key
- Qdrant Cloud account with vector database
- Existing book content indexed in Qdrant

## Setup

### 1. Environment Configuration
Create a `.env` file in the project root with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_COLLECTION_NAME=document_embeddings
```

### 2. Install Dependencies
The agent will require additional dependencies beyond the existing project:

```bash
pip install openai
```

### 3. Verify Existing Pipeline
Ensure the existing retrieval pipeline is working:

```bash
python retrieve.py "What is ROS 2?" --top-k 3
```

## Running the Agent

### 1. Execute the Agent
```bash
python agent.py
```

### 2. Interact with the Agent
Once started, you can ask questions about the book content:

```
> What are the fundamentals of ROS 2?
> Explain computer vision for robotics
> How do Vision-Language-Action models work?
> quit
```

## Expected Output
The agent will respond with information retrieved from the book content, citing sources where appropriate:

```
Agent: Based on the Physical AI & Humanoid Robotics book, ROS 2 (Robot Operating System 2) is a flexible framework for writing robot software. It provides services such as hardware abstraction, device drivers, libraries, visualizers, message-passing, package management, and more.

Sources:
- Source URL: https://example.com/ros2-intro
- Document: ROS 2 Fundamentals
```

## Troubleshooting

### Common Issues
1. **Connection Errors**: Verify your QDRANT_URL and QDRANT_API_KEY are correct
2. **No Results**: Ensure book content has been properly indexed in Qdrant
3. **API Errors**: Check that your OPENAI_API_KEY and COHERE_API_KEY are valid

### Verification Steps
1. Test Qdrant connection: `python -c "from qdrant_client import QdrantClient; client = QdrantClient(url='your_url', api_key='your_key'); print(client.get_collections())"`
2. Test Cohere: `python -c "import cohere; client = cohere.Client('your_key'); print(client.embed(texts=['test'], model='embed-multilingual-v2.0'))"`
3. Test OpenAI: `python -c "import openai; openai.api_key='your_key'; print(openai.Model.list())"`

## Next Steps
- Customize the agent's behavior by modifying system prompts
- Adjust retrieval parameters (top_k, threshold) for different use cases
- Extend with additional tools beyond the retrieval tool