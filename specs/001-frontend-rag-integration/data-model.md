# Data Model: Frontend RAG Integration

## Entities

### Query
- **Description**: User input containing a question or request for information
- **Fields**:
  - `query_text` (string, required): The actual query text from the user
  - `user_id` (string, optional): Identifier for the user (for future features)
  - `session_id` (string, optional): Session identifier for conversation history
  - `metadata` (object, optional): Additional query metadata

### Response
- **Description**: Agent-generated answer containing relevant information from the knowledge base
- **Fields**:
  - `response_text` (string, required): The agent's response to the query
  - `sources` (array, optional): List of sources used to generate the response
  - `confidence` (number, optional): Confidence score of the response (0-1)
  - `query` (string, required): The original query that generated this response
  - `timestamp` (string, required): ISO 8601 timestamp of the response
  - `retrieved_chunks` (array, optional): Raw retrieved chunks used for the response

### APIError
- **Description**: Error response format for API errors
- **Fields**:
  - `error_code` (string, required): Error code identifier
  - `message` (string, required): Human-readable error message
  - `details` (object, optional): Additional error details
  - `timestamp` (string, required): ISO 8601 timestamp of the error

## State Transitions
- Query submitted → Processing → Response generated (success path)
- Query submitted → Processing → Error response (failure path)

## Validation Rules
- Query text must not be empty
- Query text must be under 1000 characters (to prevent extremely long queries)
- Response must contain either response_text or an error message