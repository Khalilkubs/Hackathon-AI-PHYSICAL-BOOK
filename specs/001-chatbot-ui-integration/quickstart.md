# Quickstart: Chatbot UI Integration

## Development Setup

1. Ensure Docusaurus is properly installed and running
2. Install required dependencies:
   ```bash
   npm install react react-dom
   ```

## Key Components

- `ChatbotWidget.jsx`: Main chatbot component that appears on all pages
- `ChatWindow.jsx`: The expandable/collapsible chat interface
- `Message.jsx`: Individual message display component
- `InputArea.jsx`: Input field and send button
- `apiService.js`: API communication layer
- `useChatSession.js`: Custom hook for session management

## API Integration

The chatbot connects to the existing RAG API at `/query` endpoint. The API expects:
- Method: POST
- Content-Type: application/json
- Request body: `{"query_text": "user's question"}`
- Response: `{"response_text": "AI response", "sources": [], "timestamp": "..."}`

## Testing

1. Run the Docusaurus development server
2. Verify the chatbot widget appears on all pages
3. Test sending a message and receiving a response
4. Verify session persistence across page navigation
5. Test responsive behavior on different screen sizes