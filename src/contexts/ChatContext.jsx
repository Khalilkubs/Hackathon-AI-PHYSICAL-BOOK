import React, { createContext, useContext, useState, useEffect } from 'react';
import useChatSession from '../hooks/useChatSession.js';

// Create the context
const ChatContext = createContext();

// Provider component
export const ChatProvider = ({ children }) => {
  const chatSession = useChatSession();
  const [isOpen, setIsOpen] = useState(false);

  // Function to set open state
  const setOpen = (open) => {
    setIsOpen(open);
    if (open && chatSession.session) {
      // Update last active when chat is opened
      chatSession.updateLastActive();
    }
  };

  // Combine the chat session state and functions with our own state
  const value = {
    ...chatSession,
    isOpen,
    setOpen,
  };

  return <ChatContext.Provider value={value}>{children}</ChatContext.Provider>;
};

// Custom hook to use the chat context
export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};


export default ChatContext;