# Research: AI Agent with Retrieval-Augmented Capabilities

## Objective
Research the existing retrieval pipeline to understand how to integrate it with an OpenAI agent for RAG capabilities.

## Existing Retrieval Pipeline Analysis

### Key Components Identified
1. **retrieve.py**: Main retrieval module with QueryEmbedder, QdrantConnector, and ResultValidator
2. **simple_rag_query.py**: Simple RAG query interface
3. **src/storage/__init__.py**: Qdrant integration
4. **src/embedder/__init__.py**: Embedding generation
5. **src/processor/__init__.py**: Full pipeline orchestration

### Retrieval Function Analysis
The existing `retrieve.py` contains a `QdrantConnector` class with a `search_similar` method that:
- Takes a query embedding vector and top_k parameter
- Returns formatted results with content, source_url, document_title, etc.

### Integration Strategy
The retrieval tool for the OpenAI agent will need to:
1. Accept a text query from the agent
2. Generate an embedding for the query using the same Cohere model
3. Call the Qdrant search functionality
4. Format results for the agent to consume

### Decision: Retrieval Tool Implementation
**Rationale**: The existing retrieval pipeline is well-structured and can be reused by creating a wrapper function that conforms to OpenAI's tool calling interface.

**Implementation approach**:
- Create a retrieval function that accepts a query string
- Use the existing QueryEmbedder to generate embeddings
- Use the existing QdrantConnector to search
- Return formatted results that the agent can use

### Alternatives Considered
1. **Reimplementing retrieval from scratch**: Would duplicate functionality and increase maintenance
2. **Creating a new API endpoint**: Would add unnecessary complexity for a single-file implementation
3. **Direct Qdrant client usage**: Would bypass existing validation and formatting logic

### OpenAI Agent SDK Integration
The OpenAI Agents SDK allows defining tools as Python functions with proper type hints. The retrieval tool will be defined as a function with:
- Proper type hints for the query parameter
- Docstring that describes the function's purpose
- Return type that includes the retrieved content

### Dependencies Required
- openai (for agent functionality)
- cohere (for embedding generation - same as existing pipeline)
- qdrant-client (for vector search - same as existing pipeline)
- python-dotenv (for configuration - already in project)

### Error Handling Strategy
The retrieval tool will need to handle:
- Qdrant connection failures
- Empty search results
- API rate limits
- Invalid queries

### Environment Configuration
The agent will need access to:
- OPENAI_API_KEY
- COHERE_API_KEY
- QDRANT_URL
- QDRANT_API_KEY
- QDRANT_COLLECTION_NAME

### Architecture Decision: Single File Implementation
**Rationale**: Following the constraint of a single file implementation, all agent functionality will be contained in agent.py with:
- OpenAI agent initialization
- Retrieval tool definition
- Tool registration
- Conversation loop
- Error handling

This maintains the minimal and modular architecture requirement while providing full functionality.