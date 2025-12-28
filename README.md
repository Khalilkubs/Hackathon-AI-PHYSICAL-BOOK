# Physical AI & Humanoid Robotics Textbook

This repository contains a comprehensive textbook on Physical AI & Humanoid Robotics, structured as a Docusaurus-based website with additional features for enhanced learning.

## Features

- **Complete Curriculum**: 13-week curriculum covering ROS 2, Gazebo/Unity, NVIDIA Isaac, and Vision-Language-Action (VLA) models
- **Interactive Documentation**: Built with Docusaurus for an excellent reading experience
- **RAG Chatbot**: Retrieval-Augmented Generation system for intelligent Q&A about the textbook content
- **AI Assistant Integration**: Embedded chatbot accessible across all pages for immediate help with book content
- **GitHub Pages Deployment**: Automatically deployed website for easy access

## Repository Structure

- `docs/` - Contains the textbook content organized by modules and chapters
- `Physical-Ai-Book/` - Docusaurus project for the textbook website
- `scripts/` - Utility scripts for RAG system and deployment
- `.github/workflows/` - GitHub Actions for automated deployment
- `src/` - Source code for frontend components including chatbot UI

## Components

### 1. Textbook Content (Modules 1-4)
- **Module 1**: ROS 2 Fundamentals
- **Module 2**: Gazebo/Unity Simulation
- **Module 3**: NVIDIA Isaac Platform
- **Module 4**: Vision-Language-Action (VLA) Models

### 2. RAG Chatbot System
- FastAPI backend
- Qdrant vector database
- PostgreSQL for metadata
- Semantic search capabilities
- Docker-based deployment

### 3. Frontend Chatbot Integration
- React-based chatbot widget
- Docusaurus theme integration for universal access
- Session persistence across page navigation
- Responsive design for all devices
- Accessibility features (keyboard navigation, screen reader support)

### 4. GitHub Pages Deployment
- Automated deployment via GitHub Actions
- Docusaurus-optimized configuration
- Custom domain support

## Setup and Usage

### For the Textbook Website
1. Navigate to `Physical-Ai-Book/`
2. Install dependencies: `npm install`
3. Start local server: `npm start`

### For the RAG Chatbot
1. Ensure Docker and Docker Compose are installed
2. Run: `./scripts/start_rag_system.sh`
3. API will be available at `http://localhost:8000`

### For the Frontend Chatbot Integration
1. The chatbot is automatically integrated into all pages via Docusaurus theme override
2. Access the chatbot by clicking the icon in the bottom-right corner of any page
3. Ask questions about the book content and receive responses from the RAG system
4. Chat sessions persist across page navigation and browser sessions

### For GitHub Pages Deployment
The site is automatically deployed when changes are pushed to the main branch.

## Technical Requirements

- Node.js 20+ for Docusaurus
- Docker and Docker Compose for RAG system
- GitHub account for Pages deployment

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.