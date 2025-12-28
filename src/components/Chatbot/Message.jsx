import React from 'react';

// Message component for displaying chat messages
const Message = ({ message, isUserMessage = false }) => {
  // Format timestamp to show only time (HH:MM)
  const formatTime = (timestamp) => {
    if (!timestamp) return '';
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div
      className={`message ${isUserMessage ? 'user-message' : 'system-message'}`}
      role="log"
      aria-label={isUserMessage ? "User message" : "AI Assistant response"}
    >
      <div className="message-content">{message.content}</div>
      <div className="message-timestamp" aria-label={`Sent at ${formatTime(message.timestamp)}`}>
        {formatTime(message.timestamp)}
      </div>
    </div>
  );
};

// SystemMessage component for displaying system responses
const SystemMessage = ({ message }) => {
  return <Message message={message} isUserMessage={false} />;
};

// UserMessage component for displaying user messages
const UserMessage = ({ message }) => {
  return <Message message={message} isUserMessage={true} />;
};

export { Message, SystemMessage, UserMessage };
export default Message;