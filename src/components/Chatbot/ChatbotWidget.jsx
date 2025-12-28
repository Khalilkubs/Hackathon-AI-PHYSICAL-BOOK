import React, { useState, useEffect } from 'react';
import { useChat } from '../../contexts/ChatContext.jsx';
import { createUserMessage, createSystemMessage } from '../../models/chatMessage.js';
import InputArea from './InputArea.jsx';
import Message from './Message.jsx';
import apiService from '../../services/apiService.js';
import './styles.css';

// Main chatbot widget component with expand/collapse functionality
const ChatbotWidget = () => {
  const [isMinimized, setIsMinimized] = useState(false);
  const {
    session,
    messages,
    isLoading,
    error,
    isOpen,
    setOpen,
    addMessage,
    setLoading,
    setError
  } = useChat();


  const toggleChat = () => {
    const newOpenState = !isOpen;
    setOpen(newOpenState);
    if (newOpenState) {
      setIsMinimized(false); // When opening, ensure it's not minimized
    }
  };

  const minimizeChat = () => {
    setIsMinimized(true);
    setOpen(false);
  };

  const restoreChat = () => {
    setIsMinimized(false);
    setOpen(true);
  };

  // Handle sending a message to the API
  const handleSendMessage = async (messageText) => {
    if (messageText.trim() === '') return;

    try {
      // Create and add user message
      const userMessage = createUserMessage(`msg_${Date.now()}`, messageText);
      addMessage(userMessage);

      // Set loading state
      setLoading(true);
      setError(null);

      // Call the RAG API
      const response = await apiService.queryRAG(messageText, {
        sessionId: session?.id || null,
      });

      if (response.success) {
        // Create and add system response message
        const systemMessage = createSystemMessage(
          `msg_${Date.now()}`,
          response.data.response_text
        );
        addMessage(systemMessage);
      } else {
        // Handle API error
        const errorMessage = createSystemMessage(
          `msg_${Date.now()}`,
          `Sorry, I encountered an error: ${response.message || 'Unknown error'}`
        );
        addMessage(errorMessage);
      }
    } catch (err) {
      console.error('Error sending message:', err);
      setError(err.message || 'An error occurred while sending the message');

      // Add error message to chat
      const errorMessage = createSystemMessage(
        `msg_${Date.now()}`,
        'Sorry, I encountered an error processing your request. Please try again.'
      );
      addMessage(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chatbot-widget" role="complementary" aria-label="AI Assistant Chat">
      {/* Chatbot minimized icon */}
      {!isOpen && !isMinimized && (
        <button
          className="chatbot-toggle-button"
          onClick={toggleChat}
          aria-label="Open AI Assistant chat"
          title="Chat with AI Assistant"
          onKeyDown={(e) => {
            if (e.key === 'Enter' || e.key === ' ') {
              e.preventDefault();
              toggleChat();
            }
          }}
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
            <path d="M12 2C6.48 2 2 6.48 2 12C2 13.54 2.36 15.01 3.02 16.32L2 22L7.68 20.98C8.99 21.64 10.46 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2Z" fill="currentColor"/>
            <path d="M9 12L11 14L15 10" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
      )}

      {/* Minimized chat window */}
      {isMinimized && (
        <div className="chatbot-minimized" role="region" aria-label="Minimized chat window">
          <button
            className="chatbot-restore-button"
            onClick={restoreChat}
            aria-label="Restore chat window"
            onKeyDown={(e) => {
              if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                restoreChat();
              }
            }}
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
              <path d="M20 2H4C2.9 2 2 2.9 2 4V20C2 21.1 2.9 22 4 22H20C21.1 22 22 21.1 22 20V4C22 2.9 21.1 2 20 2ZM20 20H4V4H20V20ZM18 6L12 11L6 6H18Z" fill="currentColor"/>
            </svg>
          </button>
        </div>
      )}

      {/* Full chat window */}
      {isOpen && (
        <div
          className="chatbot-window"
          role="dialog"
          aria-modal="true"
          aria-label="AI Assistant Chat"
          onKeyDown={(e) => {
            if (e.key === 'Escape') {
              toggleChat();
            }
          }}
        >
          <div className="chatbot-header">
            <div className="chatbot-title" aria-live="polite">AI Assistant</div>
            <div className="chatbot-actions">
              <button
                className="chatbot-minimize-button"
                onClick={minimizeChat}
                aria-label="Minimize chat window"
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    minimizeChat();
                  }
                }}
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                  <path d="M6 12H18M12 6V18" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                </svg>
              </button>
              <button
                className="chatbot-close-button"
                onClick={toggleChat}
                aria-label="Close chat window"
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    toggleChat();
                  }
                }}
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                  <path d="M6 18L18 6M6 6L18 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                </svg>
              </button>
            </div>
          </div>

          <div className="chatbot-content">
            <div className="chatbot-messages" id="chat-messages" aria-live="polite" aria-relevant="additions">
              {messages.map((message) => (
                <Message
                  key={message.id}
                  message={message}
                  isUserMessage={message.sender === 'user'}
                />
              ))}

              {isLoading && (
                <div className="message system-message" role="status" aria-label="AI Assistant is typing">
                  <div className="message-content">
                    <div className="typing-indicator" aria-label="Typing indicator">
                      <span aria-hidden="true"></span>
                      <span aria-hidden="true"></span>
                      <span aria-hidden="true"></span>
                    </div>
                  </div>
                </div>
              )}
            </div>

            <InputArea
              onSendMessage={handleSendMessage}
              disabled={isLoading}
              placeholder="Ask a question about the book..."
            />

            {error && (
              <div className="chatbot-error" role="alert" aria-live="assertive">
                Error: {error}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatbotWidget;