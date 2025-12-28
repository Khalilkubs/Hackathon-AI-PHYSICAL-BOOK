# API Contract: RAG Retrieval Validation

## Overview
This contract defines the interface for the RAG retrieval validation system.

## Endpoints

### POST /validate-query
Validates a query against stored embeddings and returns validation results.

**Request**:
```json
{
  "query": "string (required)",
  "top_k": "integer (optional, default: 5)",
  "similarity_threshold": "float (optional, default: 0.5)"
}
```

**Response**:
```json
{
  "query": "string",
  "timestamp": "datetime",
  "results": [
    {
      "chunk_id": "string",
      "similarity_score": "float",
      "content": "string",
      "source_url": "string",
      "document_title": "string",
      "chunk_index": "integer"
    }
  ],
  "validation_report": {
    "validation_passed": "boolean",
    "results_count": "integer",
    "source_urls_matched": "integer",
    "metadata_validated": "integer",
    "avg_similarity_score": "float"
  }
}
```

### GET /health
Checks the health of the retrieval validation system.

**Response**:
```json
{
  "status": "string (ok|error)",
  "qdrant_connected": "boolean",
  "cohere_accessible": "boolean",
  "collection_exists": "boolean"
}
```