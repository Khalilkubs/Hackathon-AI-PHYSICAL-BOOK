import { useState, useEffect } from 'react';
import { ChatSession } from '../models/chatSession.js';

// Custom hook for chat session management with localStorage persistence
const useChatSession = () => {
  const [session, setSession] = useState(null);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Load session from localStorage on mount
  useEffect(() => {
    const savedSessionData = localStorage.getItem('chatSession');
    if (savedSessionData) {
      try {
        const parsedData = JSON.parse(savedSessionData);
        // Create a new session from the saved data
        const loadedSession = ChatSession.fromJSON(parsedData);
        // Check if the session is expired
        if (loadedSession.isExpired()) {
          // If expired, create a new session
          const newSession = new ChatSession(`session_${Date.now()}`);
          setSession(newSession);
          setMessages([]);
          // Save the new session to localStorage
          localStorage.setItem('chatSession', JSON.stringify(newSession.toJSON()));
        } else {
          // If not expired, use the loaded session
          setSession(loadedSession);
          setMessages(loadedSession.getMessages());
        }
      } catch (e) {
        console.error('Error loading session from localStorage:', e);
        // If there's an error, create a new session
        const newSession = new ChatSession(`session_${Date.now()}`);
        setSession(newSession);
        setMessages([]);
      }
    } else {
      // If no saved session, create a new one
      const newSession = new ChatSession(`session_${Date.now()}`);
      setSession(newSession);
      setMessages([]);
    }
  }, []);

  // Save session to localStorage whenever it changes
  useEffect(() => {
    if (session) {
      try {
        localStorage.setItem('chatSession', JSON.stringify(session.toJSON()));
      } catch (e) {
        console.error('Error saving session to localStorage:', e);
        setError('Failed to save session');
      }
    }
  }, [session]);

  // Create a new session
  const createSession = (sessionId) => {
    const newSession = new ChatSession(sessionId);
    setSession(newSession);
    setMessages([]);
    setError(null);
    return newSession;
  };

  // Add a message to the session
  const addMessage = (message) => {
    if (!session) return;

    try {
      // Create a new session instance to ensure methods are available
      const updatedSession = session; // session should already be a ChatSession instance
      updatedSession.addMessage(message);
      // Use the session's toJSON method to preserve structure while triggering re-render
      setSession(updatedSession); // Update with the same instance (methods preserved)
      setMessages([...updatedSession.getMessages()]);
      setError(null);
    } catch (e) {
      console.error('Error adding message:', e);
      setError(e.message);
    }
  };

  // Clear all messages from the session
  const clearMessages = () => {
    if (!session) return;

    try {
      const updatedSession = session;
      updatedSession.clearMessages();
      setSession(updatedSession);
      setMessages([]);
      setError(null);
    } catch (e) {
      console.error('Error clearing messages:', e);
      setError(e.message);
    }
  };

  // Check if the current session is expired
  const isSessionExpired = () => {
    if (!session) return true;
    return session.isExpired();
  };

  // Update the last active time
  const updateLastActive = () => {
    if (!session) return;

    try {
      const updatedSession = session;
      updatedSession.updateLastActive();
      setSession(updatedSession);
      setError(null);
    } catch (e) {
      console.error('Error updating last active time:', e);
      setError(e.message);
    }
  };

  // Reset the session (create a new one)
  const resetSession = () => {
    const newSession = new ChatSession(`session_${Date.now()}`);
    setSession(newSession);
    setMessages([]);
    setError(null);
  };

  // Function to set loading state
  const setLoading = (loading) => {
    setIsLoading(loading);
  };

  return {
    session,
    messages,
    isLoading,
    error,
    createSession,
    addMessage,
    clearMessages,
    isSessionExpired,
    updateLastActive,
    resetSession,
    setLoading,
    setError,
  };
};

export default useChatSession;