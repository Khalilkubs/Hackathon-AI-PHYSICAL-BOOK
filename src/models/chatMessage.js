// ChatMessage model representing a single interaction in the chat conversation
export class ChatMessage {
  constructor(id, content, sender, timestamp = new Date().toISOString(), status = 'received', error = null) {
    this.id = id;
    this.content = content;
    this.sender = sender; // 'user' or 'system'
    this.timestamp = timestamp;
    this.status = status; // 'pending', 'sent', 'received', 'error'
    this.error = error; // optional error message if status is 'error'

    // Validate inputs
    this.validate();
  }

  validate() {
    if (!this.id || typeof this.id !== 'string') {
      throw new Error('Message ID must be a non-empty string');
    }

    if (typeof this.content !== 'string' || this.content.length < 1) {
      throw new Error('Message content must be a non-empty string');
    }

    if (this.content.length > 1000) {
      throw new Error('Message content must not exceed 1000 characters');
    }

    if (!['user', 'system'].includes(this.sender)) {
      throw new Error('Sender must be either "user" or "system"');
    }

    if (!['pending', 'sent', 'received', 'error'].includes(this.status)) {
      throw new Error('Status must be one of: "pending", "sent", "received", "error"');
    }

    // Validate timestamp format (ISO 8601)
    if (isNaN(Date.parse(new Date(this.timestamp)))) {
      throw new Error('Timestamp must be in ISO 8601 format');
    }
  }

  // Update message status
  updateStatus(newStatus, error = null) {
    if (!['pending', 'sent', 'received', 'error'].includes(newStatus)) {
      throw new Error('Status must be one of: "pending", "sent", "received", "error"');
    }

    this.status = newStatus;
    if (newStatus === 'error' && error) {
      this.error = error;
    }
  }

  // Convert to JSON for storage/transmission
  toJSON() {
    return {
      id: this.id,
      content: this.content,
      sender: this.sender,
      timestamp: this.timestamp,
      status: this.status,
      error: this.error
    };
  }
}

// Helper function to create a new user message
export const createUserMessage = (id, content) => {
  return new ChatMessage(id, content, 'user', new Date().toISOString(), 'sent');
};

// Helper function to create a new system message
export const createSystemMessage = (id, content) => {
  return new ChatMessage(id, content, 'system', new Date().toISOString(), 'received');
};