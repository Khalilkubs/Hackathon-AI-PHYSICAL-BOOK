# Data Model: Document Ingestion and Vector Storage System

**Feature**: Document Ingestion and Vector Storage System
**Created**: 2025-12-25
**Status**: Draft

## Entity Models

### Document
Represents a source document from a Docusaurus URL

**Fields**:
- `id`: string (unique identifier, auto-generated)
- `url`: string (source URL of the document)
- `title`: string (document title extracted from HTML)
- `content`: string (full cleaned text content)
- `created_at`: datetime (timestamp of ingestion)
- `updated_at`: datetime (timestamp of last update)
- `metadata`: dict (additional page metadata like author, tags, etc.)

**Validation Rules**:
- URL must be a valid, accessible Docusaurus URL
- Content must be non-empty after cleaning
- Title must be present

### Text Chunk
Represents a segment of processed text that will be converted to an embedding

**Fields**:
- `id`: string (unique identifier, auto-generated)
- `document_id`: string (foreign key reference to Document.id)
- `content`: string (chunked text content)
- `chunk_index`: integer (sequential position in document)
- `token_count`: integer (number of tokens in chunk)
- `start_pos`: integer (starting position in original document)
- `end_pos`: integer (ending position in original document)

**Validation Rules**:
- Content must be non-empty
- Chunk size must be within embedding model limits (≤512 tokens)
- chunk_index must be non-negative

### Embedding
Vector representation of a text chunk, stored with metadata in the vector database

**Fields**:
- `id`: string (unique identifier, auto-generated)
- `chunk_id`: string (foreign key reference to Text Chunk.id)
- `vector`: list[float] (embedding vector, 1024-dimensional for Cohere)
- `metadata`: dict (additional metadata including content, source URL, document title, chunk index, token count)
- `created_at`: datetime (timestamp of embedding generation)

**Validation Rules**:
- Vector must have exactly 1024 dimensions (for Cohere multilingual model)
- chunk_id must reference a valid Text Chunk
- Vector values must be finite numbers

### Search Result
Contains relevant chunks and similarity scores returned by vector search

**Fields**:
- `chunk_id`: string (reference to the matched Text Chunk)
- `similarity_score`: float (cosine similarity score between 0 and 1)
- `content`: string (the text content of the matched chunk)
- `source_url`: string (URL of the source document)
- `document_title`: string (title of the source document)
- `chunk_index`: integer (position of chunk in original document)

## Relationships

```
Document (1) → (n) Text Chunk
Text Chunk (1) → (1) Embedding
Embedding → Search Result (virtual, generated during search)
```

## Collection Schema (Qdrant)

### Collection: "document_embeddings"
- Vector size: 1024
- Distance function: Cosine
- Payload schema:
  - source_url: keyword
  - document_title: text
  - chunk_index: integer
  - content: text
  - token_count: integer
  - chunk_id: keyword
  - created_at: datetime

## State Transitions

### Document States
1. **PENDING**: URL identified, not yet fetched
2. **FETCHED**: Content retrieved from URL
3. **CLEANED**: HTML cleaned, text extracted
4. **CHUNKED**: Content split into chunks
5. **EMBEDDED**: All chunks have embeddings generated
6. **STORED**: Embeddings stored in vector database
7. **FAILED**: Processing failed at any stage

### Processing Flow
```
PENDING → FETCHED → CLEANED → CHUNKED → EMBEDDED → STORED
                    ↓
                  FAILED (on any error)
```

## Indexing Strategy

### Vector Index
- Type: HNSW (Hierarchical Navigable Small World)
- M: 16 (number of connections per layer)
- ef_construct: 100 (construction parameter)
- ef: 10 (search parameter)

### Payload Indexes
- source_url: keyword index for filtering
- document_title: full-text index for search
- chunk_index: integer index for ordering
- content: full-text index for content search
- token_count: integer index for filtering
- chunk_id: keyword index for filtering

## Data Validation

### Input Validation
- URL format validation using regex
- Content type verification (must be HTML)
- Size limits for documents (max 10MB)

### Processing Validation
- Token count validation for chunks
- Embedding dimension validation
- Metadata completeness checks

### Output Validation
- Similarity score range validation (0-1)
- Result completeness verification