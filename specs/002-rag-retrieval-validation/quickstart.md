# Quickstart Guide: RAG Retrieval Validation System

**Feature**: RAG Retrieval Validation System
**Created**: 2025-12-25
**Status**: Draft

## Overview

This guide provides step-by-step instructions for setting up and using the RAG retrieval validation system. The system validates that stored embeddings in Qdrant can be properly retrieved with relevant results matching source metadata.

## Prerequisites

- Python 3.11+
- pip package manager
- Access to Cohere API (valid API key)
- Access to Qdrant Cloud instance (valid URL and API key)
- Existing embeddings stored in Qdrant from the book ingestion process

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd path/to/Hackathon-AI-PHYSICAL-BOOK
   ```

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the project root with the following variables:
   ```env
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_URL=your_qdrant_cloud_url_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   QDRANT_COLLECTION_NAME=document_embeddings
   ```

## Basic Usage

1. **Run the retrieval validation script:**
   ```bash
   python retrieve.py "Your test query here"
   ```

2. **With custom top-k parameter:**
   ```bash
   python retrieve.py "Your test query here" --top-k 10
   ```

3. **With verbose output:**
   ```bash
   python retrieve.py "Your test query here" --verbose
   ```

## Advanced Usage

1. **Validate multiple queries from a file:**
   ```bash
   python retrieve.py --queries-file queries.txt
   ```

2. **Validate with custom similarity threshold:**
   ```bash
   python retrieve.py "Your test query here" --threshold 0.7
   ```

3. **Run comprehensive validation report:**
   ```bash
   python retrieve.py --validate-all
   ```

## Expected Output

When running a query, you should see:
- Connection status to Qdrant
- Query embedding generation status
- Retrieved results with similarity scores
- Source URL validation
- Metadata completeness check
- Validation report summary

Example output:
```
✓ Connected to Qdrant successfully
✓ Generated query embedding (1024 dimensions)
Query: "What are the principles of Physical AI?"
Retrieved 5 results:

1. [Score: 0.842] Source: https://example.com/physical-ai/principles
   "Physical AI systems integrate sensing, reasoning, and acting..."

2. [Score: 0.791] Source: https://example.com/robotics/fundamentals
   "The core principle of embodied intelligence requires..."

✓ Validation passed: 5/5 results matched source URLs
✓ All metadata fields present and valid
✓ Average similarity score: 0.768
```

## Troubleshooting

**Common Issues:**

1. **Connection errors**: Verify QDRANT_URL and QDRANT_API_KEY are correct
2. **API key errors**: Check COHERE_API_KEY is valid and properly formatted
3. **No results returned**: Ensure embeddings exist in the collection
4. **Dimension mismatch**: Verify stored embeddings are 1024-dimensional

**Diagnostic Commands:**

- Test Qdrant connection: `python retrieve.py --test-connection`
- Check collection info: `python retrieve.py --collection-info`
- Validate configuration: `python retrieve.py --validate-config`

## Next Steps

- Run validation on multiple test queries
- Adjust top-k and threshold parameters based on your needs
- Review validation reports for accuracy assessment
- Integrate validation into your CI/CD pipeline