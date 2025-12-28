# Data Model: RAG Retrieval Validation System

**Feature**: RAG Retrieval Validation System
**Created**: 2025-12-25
**Status**: Draft

## Entity Definitions

### Query Entity
Represents a user search query that will be converted to an embedding for similarity search

**Fields**:
- `id`: string (unique identifier for the query, auto-generated)
- `text`: string (the input query text, required, min length 1)
- `embedding`: list[float] (vector representation of the query, 1024-dimensional)
- `created_at`: datetime (timestamp when query was created)
- `top_k`: integer (number of results to retrieve, default: 5, range: 1-20)

**Validation Rules**:
- Text must not be empty or contain only whitespace
- Embedding must have exactly 1024 dimensions
- Top-k must be between 1 and 20

**State Transitions**:
- Created → Embedded (when query is converted to embedding)

### Retrieval Result Entity
Contains relevant text chunks, similarity scores, source URLs, and metadata returned from the vector search

**Fields**:
- `id`: string (unique identifier for the result, from Qdrant)
- `chunk_id`: string (reference to the original text chunk, from Qdrant payload)
- `similarity_score`: float (cosine similarity score between query and result, range: 0.0-1.0)
- `content`: string (the retrieved text content, from Qdrant payload)
- `source_url`: string (URL where the original content was sourced from, from Qdrant payload)
- `document_title`: string (title of the source document, from Qdrant payload)
- `chunk_index`: integer (position of the chunk in the original document, from Qdrant payload)
- `token_count`: integer (number of tokens in the chunk, from Qdrant payload)
- `retrieval_timestamp`: datetime (when result was retrieved)

**Validation Rules**:
- Similarity score must be between 0.0 and 1.0
- Content must not be empty
- Source URL must be a valid URL format
- Chunk ID must match the expected pattern

**State Transitions**:
- Retrieved → Validated (when result is validated against source metadata)

### Validation Report Entity
Summarizes the results of retrieval tests, including relevance metrics and error status

**Fields**:
- `id`: string (unique identifier for the report, auto-generated)
- `query_text`: string (the original query that was executed)
- `query_embedding`: list[float] (the embedding used for the search)
- `timestamp`: datetime (when validation was performed)
- `results_count`: integer (number of results returned)
- `top_k_requested`: integer (number of results requested)
- `validation_passed`: boolean (whether results meet validation criteria)
- `validation_details`: list[dict] (details about each validation check)
- `source_urls_matched`: integer (count of results with matching source URLs)
- `metadata_validated`: integer (count of results with valid metadata)
- `avg_similarity_score`: float (average similarity score of results)
- `min_similarity_score`: float (minimum similarity score among results)
- `max_similarity_score`: float (maximum similarity score among results)
- `error_message`: string (any error that occurred during validation)

**Validation Rules**:
- Results count must match or be less than top_k_requested
- Average similarity score must be calculated correctly
- Validation details must contain at least one validation entry
- Timestamp must be in the past or present

**State Transitions**:
- Created → Processing (when validation begins)
- Processing → Completed (when validation finishes successfully)
- Processing → Failed (when validation encounters errors)

## Entity Relationships

### Query → Retrieval Result
- One Query can produce many Retrieval Results (one-to-many)
- Relationship: "retrieved_results"
- Cardinality: 1..* (one query produces 1 to many results)

### Query → Validation Report
- One Query produces one Validation Report (one-to-one)
- Relationship: "generates_report"
- Cardinality: 1..1 (one query generates exactly one report)

### Retrieval Result → Validation Report
- Many Retrieval Results belong to one Validation Report (many-to-one)
- Relationship: "included_in_report"
- Cardinality: 0..* (many results, may be 0 if query failed)

## Data Flow Patterns

### Query Processing Flow
1. Query entity is created with user input
2. Query text is converted to embedding vector (1024 dimensions)
3. Similarity search is performed in Qdrant
4. Retrieval results are collected and validated
5. Validation report is generated

### Validation Flow
1. Retrieved results are checked against source URLs
2. Metadata completeness is verified
3. Content relevance is assessed
4. Validation report is populated with results
5. Success/failure status is determined

## Constraints and Assumptions

### Constraints
- Vector dimension: All embeddings must be 1024-dimensional to match Cohere model output
- Top-k range: Results count must be between 1 and 20 for reasonable performance
- Similarity range: Scores must be between 0.0 and 1.0 for cosine similarity
- URL format: Source URLs must follow standard URL format

### Assumptions
- Qdrant collection exists with appropriate schema
- Cohere API is accessible and functional
- Existing embeddings in Qdrant have the expected metadata structure
- Network connectivity is available for API calls