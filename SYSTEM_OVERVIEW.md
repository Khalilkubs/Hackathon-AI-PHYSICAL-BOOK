# Physical AI & Humanoid Robotics Book - RAG System Overview

## Architecture Overview

Your project is a comprehensive system that combines a Docusaurus-based textbook website with an integrated RAG (Retrieval-Augmented Generation) chatbot. The system is designed to allow users to read the textbook and ask questions about the content through an AI assistant.

## System Components

### 1. Docusaurus Book Website (`Physical-Ai-Book/`)
- **Purpose**: Hosts the complete Physical AI & Humanoid Robotics textbook
- **Technology**: Built with Docusaurus (React-based static site generator)
- **Features**:
  - Module-based organization (4 modules with chapters and lessons)
  - Responsive design for all devices
  - Search functionality
  - Integrated chatbot widget on every page

### 2. Integrated Chatbot Widget (`src/components/Chatbot/`)
- **Location**: Embedded on every page via `Physical-Ai-Book/src/theme/Layout.js`
- **Features**:
  - Expandable/collapsible interface
  - Minimize functionality
  - Persistent chat sessions
  - Real-time responses from the RAG system
  - Accessible design (keyboard navigation, screen reader support)

### 3. Backend RAG System (`src/`)
- **Purpose**: Processes queries and retrieves relevant textbook content
- **Components**:
  - **Fetcher**: Retrieves content from the book URLs
  - **Cleaner**: Extracts relevant content from HTML
  - **Processor**: Orchestrates the ingestion pipeline
  - **Storage**: Connects to Qdrant vector database
  - **Embedder**: Creates embeddings using Cohere
  - **Chunker**: Splits content into manageable pieces

### 4. Four-Component Architecture
The RAG system consists of four key components:

1. **Qdrant Integration**:
   - Vector database for storing textbook content embeddings
   - Enables semantic search and similarity matching
   - Stores metadata about content sources and context

2. **Cohere Integration**:
   - Generates embeddings for content and queries
   - Provides text generation capabilities
   - Handles semantic understanding of content

3. **OpenRouter Integration**:
   - Provides OpenAI agent capabilities via OpenRouter
   - Enhances response generation with advanced AI models
   - Implemented in `agent.py` using OpenAI Agents SDK
   - Uses OpenRouter's API endpoint: `https://openrouter.ai/api/v1`
   - Configurable model selection via `AGENT_MODEL` environment variable

4. **FastAPI Communication**:
   - RESTful API backend for handling requests
   - Orchestrates communication between all components
   - Provides endpoints for the frontend chatbot

## How to Run the System

### Option 1: Full System (Recommended)

1. **Start the RAG Backend**:
   ```bash
   # Make sure Docker is running, then:
   ./scripts/start_rag_system.sh
   ```
   This starts Qdrant, PostgreSQL, and the RAG API on `http://localhost:8000`

2. **Start the Book Website**:
   ```bash
   cd Physical-Ai-Book/
   npm install
   npm start
   ```
   The website will be available at `http://localhost:3000` with the chatbot integrated on every page

### Option 2: Individual Components

1. **Book Website Only** (without chatbot functionality):
   ```bash
   cd Physical-Ai-Book/
   npm install
   npm start
   ```

2. **RAG System Only** (for API testing):
   ```bash
   # After starting Docker services with:
   ./scripts/start_rag_system.sh
   ```
   The API will be available at `http://localhost:8000`

## File Structure

```
Hackathon-AI-PHYSICAL-BOOK/
├── Physical-Ai-Book/           # Docusaurus book website
│   ├── src/
│   │   └── theme/
│   │       └── Layout.js      # Chatbot integration point
│   └── docs/                  # Book content (modules, chapters, lessons)
├── src/                       # Backend RAG system
│   ├── components/            # Chatbot React components
│   ├── contexts/              # React context providers
│   ├── fetcher/               # URL fetching logic
│   ├── cleaner/               # Content extraction
│   ├── processor/             # Pipeline orchestrator
│   ├── storage/               # Qdrant integration
│   ├── embedder/              # Embedding generation
│   └── chunker/               # Content chunking
├── my-app/                    # Alternative React frontend (built)
├── scripts/
│   ├── api/                   # FastAPI backend
│   └── start_rag_system.sh    # Docker startup script
├── docker-compose.yml         # Docker services definition
└── requirements.txt           # Python dependencies
```

## Key Features

1. **Universal Chat Access**: The chatbot appears on every page of the textbook
2. **Persistent Sessions**: Chat history persists across page navigation
3. **Real-time Responses**: Questions are processed against the full textbook
4. **Content-aware**: The RAG system understands the book's structure
5. **Accessible**: Full keyboard navigation and screen reader support
6. **Responsive**: Works on mobile, tablet, and desktop devices

## Environment Variables

Create a `.env` file in the root directory with:
```env
COHERE_API_KEY=your_cohere_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
AGENT_MODEL=mistralai/devstral-2512:free  # or your preferred model
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION_NAME=book_content
```

## Troubleshooting

1. **Chatbot not appearing**: Make sure the Docusaurus site is running from the `Physical-Ai-Book/` directory
2. **API errors**: Verify that the RAG system is running via Docker
3. **No responses**: Check that the vector database has been populated with textbook content

## Development Notes

- The chatbot is integrated via the Docusaurus theme override in `Layout.js`
- All React components are in the `src/components/Chatbot/` directory
- The backend RAG system handles content ingestion and retrieval
- The system is designed to be deployed to GitHub Pages with Docker-based backend