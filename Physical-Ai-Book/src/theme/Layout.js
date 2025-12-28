import React from 'react';
import { ChatProvider } from '../contexts/ChatContext.jsx';
import ChatbotWidget from '../components/Chatbot/ChatbotWidget.jsx';
import OriginalLayout from '@theme-original/Layout';

// Layout wrapper to add chatbot widget to all pages
export default function LayoutWrapper(props) {
  return (
    <ChatProvider>
      <OriginalLayout {...props}>
        {props.children}
        <ChatbotWidget />
      </OriginalLayout>
    </ChatProvider>
  );
}