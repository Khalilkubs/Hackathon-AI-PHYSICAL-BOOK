# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY scripts/api/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY scripts/api/rag_chatbot.py .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "rag_chatbot:app", "--host", "0.0.0.0", "--port", "8000"]