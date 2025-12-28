# Chatbot UI Integration - Documentation

## Overview
The Chatbot UI Integration feature provides an AI assistant that is accessible across all pages of the Docusaurus frontend. Users can ask questions about the Physical AI & Humanoid Robotics book content and receive intelligent responses from the RAG system.

## Components

### ChatbotWidget
The main component that displays the chat interface with expand/collapse functionality.

#### Props
- None required - self-contained component

#### Features
- Persistent across page navigation
- LocalStorage session persistence
- Responsive design for all device sizes
- Accessibility features (keyboard navigation, screen reader support)
- Loading indicators and error handling

### InputArea
Handles user input for chat messages.

#### Props
- `onSendMessage`: Function called when user sends a message
- `disabled`: Boolean to disable input during loading
- `placeholder`: Placeholder text for the input field

### Message
Displays individual chat messages.

#### Props
- `message`: Message object containing content and metadata
- `isUserMessage`: Boolean indicating if the message is from the user

## Usage

The chatbot is automatically integrated into all Docusaurus pages through the custom Layout wrapper in `Physical-Ai-Book/src/theme/Layout.js`. No additional setup is required on individual pages.

## API Integration

The chatbot connects to the RAG API at `http://127.0.0.1:8000/query` by default. The API service handles:
- Query submission to the RAG system
- Response processing
- Error handling and retry mechanisms
- Session management

## Accessibility Features

- Keyboard navigation support (Enter, Space, Escape keys)
- Screen reader compatibility with ARIA labels
- Sufficient color contrast for WCAG 2.1 AA compliance
- Focus management for interactive elements
- Semantic HTML structure

## Responsive Design

The chatbot adapts to different screen sizes:
- Desktop: 350px width x 500px height
- Tablet: 300px width x 450px height
- Mobile: 280px width x 400px height
- Collapses to floating icon on small screens

## Session Management

- Chat sessions are persisted in localStorage
- Sessions expire after 30 minutes of inactivity
- Conversation history is maintained across page navigation
- Sessions are automatically restored when returning to the site

## Error Handling

- Network error detection and user feedback
- Retry mechanism with exponential backoff for failed API calls
- Graceful handling of API timeouts
- Clear error messages for users