# Chatbot API Contract

## Query Endpoint

### POST /query

#### Request
```json
{
  "query_text": "string (user's question)",
  "user_id": "string (optional)",
  "session_id": "string (optional)",
  "metadata": "object (optional)"
}
```

#### Response
```json
{
  "response_text": "string (AI response)",
  "sources": "array of objects (optional)",
  "confidence": "number (optional)",
  "query": "string (echo of input query)",
  "timestamp": "string (ISO 8601)",
  "retrieved_chunks": "array of objects (optional)"
}
```

#### Error Response
```json
{
  "error_code": "string",
  "message": "string",
  "timestamp": "string (ISO 8601)",
  "details": "object (optional)"
}
```

## Expected HTTP Status Codes

- 200: Successful query processing
- 400: Invalid request (e.g., empty query)
- 408: Request timeout
- 500: Internal server error