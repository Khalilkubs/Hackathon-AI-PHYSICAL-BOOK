// ChatSession model representing the context of a user's conversation with the chatbot
import { ChatMessage } from './chatMessage.js';

export class ChatSession {
  constructor(id, createdAt = new Date().toISOString()) {
    this.id = id;
    this.messages = []; // Array of ChatMessage objects
    this.createdAt = createdAt;
    this.lastActiveAt = createdAt;
    this.isActive = true;

    // Validate inputs
    this.validate();
  }

  validate() {
    if (!this.id || typeof this.id !== 'string') {
      throw new Error('Session ID must be a non-empty string');
    }

    if (!Array.isArray(this.messages)) {
      throw new Error('Messages must be an array');
    }

    if (this.messages.length > 100) {
      throw new Error('Messages array must not exceed 100 messages');
    }

    // Validate timestamp format (ISO 8601)
    if (isNaN(Date.parse(new Date(this.createdAt)))) {
      throw new Error('CreatedAt must be in ISO 8601 format');
    }

    if (isNaN(Date.parse(new Date(this.lastActiveAt)))) {
      throw new Error('LastActiveAt must be in ISO 8601 format');
    }
  }

  // Add a message to the session
  addMessage(message) {
    if (!(message instanceof ChatMessage)) {
      throw new Error('Message must be an instance of ChatMessage');
    }

    if (this.messages.length >= 100) {
      throw new Error('Messages array must not exceed 100 messages');
    }

    this.messages.push(message);
    this.lastActiveAt = new Date().toISOString();
    this.isActive = true;
  }

  // Get all messages in the session
  getMessages() {
    return [...this.messages]; // Return a copy to prevent external modification
  }

  // Get the last N messages
  getLastMessages(count) {
    return [...this.messages.slice(-count)];
  }

  // Mark session as inactive after timeout
  markInactive() {
    this.isActive = false;
  }

  // Check if session is expired (inactive for more than 30 minutes)
  isExpired() {
    const now = new Date();
    const lastActive = new Date(this.lastActiveAt);
    const diffInMinutes = (now - lastActive) / (1000 * 60);
    return diffInMinutes > 30; // 30 minutes
  }

  // Update last active time
  updateLastActive() {
    this.lastActiveAt = new Date().toISOString();
    this.isActive = true;
  }

  // Clear all messages from the session
  clearMessages() {
    this.messages = [];
    this.lastActiveAt = new Date().toISOString();
  }

  // Convert to JSON for storage/transmission
  toJSON() {
    return {
      id: this.id,
      messages: this.messages.map(msg => msg.toJSON()),
      createdAt: this.createdAt,
      lastActiveAt: this.lastActiveAt,
      isActive: this.isActive
    };
  }

  // Create a session from JSON data
  static fromJSON(jsonData) {
    const session = new ChatSession(jsonData.id, jsonData.createdAt);
    session.messages = jsonData.messages.map(msg =>
      new ChatMessage(msg.id, msg.content, msg.sender, msg.timestamp, msg.status, msg.error)
    );
    session.lastActiveAt = jsonData.lastActiveAt;
    session.isActive = jsonData.isActive;
    return session;
  }
}