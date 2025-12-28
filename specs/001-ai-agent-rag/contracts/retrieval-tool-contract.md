# Contract: Retrieval Tool for AI Agent

## Purpose
Define the interface contract for the retrieval tool used by the OpenAI agent to fetch relevant content from Qdrant vector database.

## Function Signature

```python
def retrieve_content(query: str, top_k: int = 5, threshold: float = 0.5) -> dict:
    """
    Retrieve relevant content chunks from Qdrant based on the input query.

    Args:
        query (str): The search query to find relevant content
        top_k (int, optional): Number of top results to return. Defaults to 5.
        threshold (float, optional): Minimum similarity threshold. Defaults to 0.5.

    Returns:
        dict: Dictionary containing search results with content and metadata
    """
```

## Input Schema

### Parameters
- `query`: String (required)
  - Description: The user's question or query to search for
  - Constraints: Non-empty string, maximum 1000 characters
  - Example: "What are the fundamentals of ROS 2?"

- `top_k`: Integer (optional)
  - Description: Number of results to return
  - Default: 5
  - Constraints: Integer between 1 and 20
  - Example: 3

- `threshold`: Float (optional)
  - Description: Minimum similarity threshold for results
  - Default: 0.5
  - Constraints: Float between 0.0 and 1.0
  - Example: 0.7

## Output Schema

### Response Format
```json
{
  "results": [
    {
      "chunk_id": "string",
      "similarity_score": "float",
      "content": "string",
      "source_url": "string",
      "document_title": "string",
      "chunk_index": "int"
    }
  ],
  "query": "string",
  "total_results": "int",
  "search_performed": "boolean"
}
```

### Response Fields
- `results`: Array of result objects
  - `chunk_id`: Unique identifier for the content chunk
  - `similarity_score`: Similarity score between 0.0 and 1.0
  - `content`: The retrieved content text (truncated to 500 characters)
  - `source_url`: Source URL of the content
  - `document_title`: Title of the source document
  - `chunk_index`: Position of the chunk in the original document

- `query`: The original query that was searched
- `total_results`: Total number of results found
- `search_performed`: Boolean indicating if search was executed

## Error Handling

### Expected Error Cases
1. **Qdrant Connection Error**
   - Condition: Unable to connect to Qdrant database
   - Response: `{ "error": "connection_failed", "message": "Unable to connect to Qdrant database" }`

2. **Empty Results**
   - Condition: No content found matching the query
   - Response: `{ "results": [], "query": "...", "total_results": 0, "search_performed": true }`

3. **Invalid Query**
   - Condition: Query is empty or invalid
   - Response: `{ "error": "invalid_query", "message": "Query cannot be empty" }`

4. **API Rate Limit**
   - Condition: Cohere or Qdrant API rate limit exceeded
   - Response: `{ "error": "rate_limit_exceeded", "message": "API rate limit exceeded, please try again later" }`

## Performance Requirements
- Response time: < 5 seconds for typical queries
- Availability: Must handle Qdrant connection failures gracefully
- Reliability: Should return meaningful results or clear error messages

## Validation Rules
- Tool must return results based only on actual content in the database
- Tool must not generate or fabricate information
- Tool must include source information for all returned content
- Tool must respect the threshold parameter for result filtering