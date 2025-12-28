# Data Model: Chatbot UI Integration

## Entities

### Chat Message
- **id**: string (unique identifier for the message)
- **content**: string (the text content of the message)
- **sender**: enum (either "user" or "system")
- **timestamp**: datetime (when the message was created)
- **status**: enum ("pending", "sent", "received", "error")
- **error**: string (optional error message if status is "error")

### Chat Session
- **id**: string (unique identifier for the session)
- **messages**: array of Chat Message (conversation history)
- **createdAt**: datetime (when the session was created)
- **lastActiveAt**: datetime (when the session was last used)
- **isActive**: boolean (whether the session is currently active)

## State Transitions

### Chat Message States
- `pending` → `sent` → `received` (normal flow)
- `pending` → `error` (if sending fails)

### Chat Session States
- `active` ↔ `inactive` (based on user interaction and time since last activity)

## Validation Rules

### Chat Message
- Content must not be empty (min length: 1 character)
- Content must not exceed 1000 characters (max length: 1000 characters)
- Sender must be either "user" or "system"
- Timestamp must be in ISO 8601 format

### Chat Session
- Messages array must not exceed 100 messages (to prevent memory issues)
- Session must be marked as inactive after 30 minutes of inactivity
- Session ID must be unique per browser instance