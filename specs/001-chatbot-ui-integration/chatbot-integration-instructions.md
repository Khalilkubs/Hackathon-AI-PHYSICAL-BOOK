# Chatbot Integration Instructions

## Overview
The AI Assistant chatbot is now integrated across all pages of the Physical AI & Humanoid Robotics book website. The chatbot provides access to the RAG (Retrieval-Augmented Generation) system to answer questions about the book content.

## How to Use

### Accessing the Chatbot
1. Look for the chat icon in the bottom-right corner of any page
2. Click the icon to open the chat window
3. Type your question about the book content in the input field
4. Press Enter or click the send button to submit

### Features
- **Persistent Chat**: Your conversation remains active as you navigate between pages
- **Smart Responses**: The AI Assistant understands the book content and provides relevant answers
- **Mobile Friendly**: The chat interface adapts to all screen sizes

## Technical Details

### Integration Method
The chatbot is integrated using a Docusaurus theme override at `Physical-Ai-Book/src/theme/Layout.js`. This automatically adds the chatbot to all pages without requiring changes to individual components.

### API Connection
- The chatbot connects to the RAG API at `http://127.0.0.1:8000/query`
- All communication is handled through the `apiService.js` module
- Responses are cached to improve performance

### Session Management
- Chat sessions are stored in browser's localStorage
- Sessions persist across page navigation and browser sessions
- Sessions expire after 30 minutes of inactivity

## Troubleshooting

### Chatbot Not Appearing
- Ensure JavaScript is enabled in your browser
- Clear your browser cache and refresh the page
- Check browser console for any JavaScript errors

### API Connection Issues
- Verify the RAG API server is running on `http://127.0.0.1:8000`
- Check your internet connection
- The system will automatically retry failed requests

## Accessibility
The chatbot is designed to be accessible:
- Fully navigable using keyboard (Tab, Enter, Space, Escape)
- Compatible with screen readers
- High contrast color scheme for readability