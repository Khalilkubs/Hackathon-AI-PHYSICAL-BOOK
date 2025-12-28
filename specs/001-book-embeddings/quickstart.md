# Quickstart Guide: Document Ingestion and Vector Storage System

**Feature**: Document Ingestion and Vector Storage System
**Created**: 2025-12-25

## Overview

This guide provides instructions to quickly set up and run the document ingestion pipeline that fetches content from Docusaurus URLs, generates embeddings using Cohere, and stores them in Qdrant Cloud.

## Prerequisites

- Python 3.11 or higher
- pip package manager
- Cohere API key
- Qdrant Cloud URL and API key

## Setup

### 1. Clone and Navigate to Project

```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or if no requirements.txt exists yet:

```bash
pip install requests beautifulsoup4 cohere qdrant-client python-dotenv tiktoken
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_cloud_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
CHUNK_SIZE=512
CHUNK_OVERLAP=50
REQUEST_TIMEOUT=30
MAX_RETRIES=3
```

## Usage

### 1. Run the Ingestion Pipeline

The main entry point is `main.py`. To ingest a single URL:

```bash
python main.py --url "https://your-docs-site.vercel.app"
```

### 2. Ingest Multiple URLs

Create a text file with URLs (one per line) and process them:

```bash
python main.py --urls-file urls.txt
```

### 3. Advanced Options

```bash
# Custom chunk size and overlap
python main.py --url "https://example.com" --chunk-size 256 --chunk-overlap 25

# Process with specific options
python main.py --url "https://example.com" --max-retries 5 --timeout 60
```

## Pipeline Components

The ingestion pipeline consists of 5 main components:

1. **URL Fetcher**: Retrieves content from the provided URL with error handling
2. **HTML Cleaner**: Extracts relevant text content and removes navigation/UI elements
3. **Text Chunker**: Splits content into appropriately sized chunks (default 512 tokens)
4. **Embedding Generator**: Creates vector embeddings using Cohere API
5. **Vector Storage**: Stores embeddings in Qdrant Cloud with metadata

## Configuration Options

| Environment Variable | Description | Default |
|---------------------|-------------|---------|
| `COHERE_API_KEY` | API key for Cohere services | - |
| `QDRANT_URL` | URL for Qdrant Cloud instance | - |
| `QDRANT_API_KEY` | API key for Qdrant Cloud | - |
| `CHUNK_SIZE` | Maximum size of text chunks | 512 |
| `CHUNK_OVERLAP` | Overlap between consecutive chunks | 50 |
| `REQUEST_TIMEOUT` | HTTP request timeout in seconds | 30 |
| `MAX_RETRIES` | Maximum retry attempts for failed operations | 3 |

## Example Usage

### Basic Ingestion

```python
from main import main

# Ingest a single URL
result = main(url="https://my-docs.vercel.app/getting-started")
print(f"Status: {result['status']}")
print(f"Chunks processed: {result['chunks_processed']}")
```

### Batch Processing

```python
from main import process_multiple_urls

urls = [
    "https://docs.example.com/intro",
    "https://docs.example.com/api-reference",
    "https://docs.example.com/tutorials"
]

results = process_multiple_urls(urls)
for url, result in results.items():
    print(f"{url}: {result['status']}")
```

## Verification

After ingestion, verify that:

1. Content was properly extracted (check logs for document titles)
2. Chunks were created within size limits
3. Embeddings were generated successfully
4. Data was stored in Qdrant (verify through Qdrant dashboard)

## Troubleshooting

### Common Issues

- **URL Not Accessible**: Verify the URL is publicly accessible and returns HTML content
- **API Limits**: Check Cohere and Qdrant rate limits if processing fails
- **Memory Issues**: For very large documents, consider preprocessing to split content

### Logging

The system logs detailed information to help troubleshoot:

- `DEBUG`: Detailed processing information
- `INFO`: Major processing steps
- `WARNING`: Non-critical issues
- `ERROR`: Processing failures

Enable debug logging with:
```bash
export LOG_LEVEL=DEBUG
python main.py --url "https://example.com"
```

## Next Steps

1. Integrate the ingestion pipeline into your RAG application
2. Implement search functionality using the stored embeddings
3. Add monitoring and alerting for production use
4. Optimize chunking strategy based on your content characteristics