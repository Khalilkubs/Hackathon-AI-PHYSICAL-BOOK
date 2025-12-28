import React, { useState } from 'react';

// InputArea component for message input
const InputArea = ({ onSendMessage, disabled = false, placeholder = "Type your message..." }) => {
  const [inputValue, setInputValue] = useState('');

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleSendMessage = () => {
    if (inputValue.trim() !== '') {
      onSendMessage(inputValue);
      setInputValue(''); // Clear input after sending
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="chatbot-input-area">
      <input
        type="text"
        value={inputValue}
        onChange={handleInputChange}
        onKeyDown={handleKeyPress}
        placeholder={placeholder}
        className="chatbot-input"
        aria-label="Type your question to the AI Assistant"
        disabled={disabled}
        role="textbox"
        aria-multiline="false"
        autoComplete="off"
        spellCheck="true"
      />
      <button
        className="chatbot-send-button"
        onClick={handleSendMessage}
        disabled={disabled || inputValue.trim() === ''}
        aria-label="Send message to AI Assistant"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
          <path d="M22 2L11 13M22 2L15 22L11 13M11 13L2 9L22 2" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      </button>
    </div>
  );
};

export default InputArea;