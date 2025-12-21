"""
Script to populate the RAG system with textbook content
This script will read the textbook markdown files and add them to the vector database
"""

import os
import asyncio
from pathlib import Path
import aiofiles
import json
from typing import List, Dict
import hashlib

# Import required libraries
try:
    from qdrant_client import QdrantClient
    from qdrant_client.http import models
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("Required packages not found. Please install: qdrant-client, sentence-transformers")


class TextbookRAGPopulator:
    def __init__(self, qdrant_host="localhost", qdrant_port=6333):
        self.qdrant_client = QdrantClient(host=qdrant_host, port=qdrant_port)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.collection_name = "textbook_content"

    def read_markdown_file(self, file_path: str) -> str:
        """Read content from a markdown file"""
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content

    def split_content(self, content: str, max_chunk_size: int = 1000) -> List[str]:
        """Split content into chunks of maximum specified size"""
        paragraphs = content.split('\n\n')
        chunks = []
        current_chunk = ""

        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) <= max_chunk_size:
                current_chunk += paragraph + "\n\n"
            else:
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph + "\n\n"

        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return chunks

    def generate_document_id(self, content: str, source_file: str) -> str:
        """Generate a unique ID for a document chunk"""
        content_hash = hashlib.md5(content.encode()).hexdigest()
        source_hash = hashlib.md5(source_file.encode()).hexdigest()
        return f"{source_hash[:8]}_{content_hash[:8]}"

    def get_file_metadata(self, file_path: str) -> Dict:
        """Extract metadata from file path"""
        path_parts = Path(file_path).parts
        metadata = {
            "file_path": file_path,
            "module": "",
            "chapter": "",
            "lesson": ""
        }

        # Extract module, chapter, lesson from path
        for part in path_parts:
            if "module" in part.lower():
                metadata["module"] = part
            elif "chapter" in part.lower():
                metadata["chapter"] = part
            elif "lesson" in part.lower():
                metadata["lesson"] = part

        return metadata

    async def add_document_to_qdrant(self, content: str, metadata: Dict, doc_id: str):
        """Add a document chunk to Qdrant vector database"""
        try:
            # Generate embedding
            embedding = self.embedding_model.encode(content).tolist()

            # Add to Qdrant
            self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=[
                    models.PointStruct(
                        id=doc_id,
                        vector=embedding,
                        payload={
                            "content": content,
                            "metadata": metadata
                        }
                    )
                ]
            )
            print(f"Added document {doc_id} to vector database")
            return True
        except Exception as e:
            print(f"Error adding document {doc_id}: {str(e)}")
            return False

    async def process_directory(self, directory_path: str):
        """Process all markdown files in a directory and its subdirectories"""
        markdown_files = []

        # Find all markdown files recursively
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith('.md'):
                    markdown_files.append(os.path.join(root, file))

        total_chunks = 0
        successful_additions = 0

        for file_path in markdown_files:
            print(f"Processing file: {file_path}")

            try:
                # Read file content
                content = self.read_markdown_file(file_path)

                # Split into chunks
                chunks = self.split_content(content)

                # Get file metadata
                metadata = self.get_file_metadata(file_path)

                # Add each chunk to the database
                for i, chunk in enumerate(chunks):
                    doc_id = self.generate_document_id(chunk, file_path)

                    # Add metadata about chunk number
                    chunk_metadata = metadata.copy()
                    chunk_metadata["chunk_number"] = i
                    chunk_metadata["total_chunks"] = len(chunks)

                    success = await self.add_document_to_qdrant(chunk, chunk_metadata, doc_id)
                    if success:
                        successful_additions += 1

                    total_chunks += 1

            except Exception as e:
                print(f"Error processing file {file_path}: {str(e)}")

        print(f"\nProcessing complete!")
        print(f"Total chunks processed: {total_chunks}")
        print(f"Successful additions: {successful_additions}")
        print(f"Failed additions: {total_chunks - successful_additions}")


async def main():
    # Initialize the populator
    populator = TextbookRAGPopulator()

    # Check if collection exists, create if not
    try:
        populator.qdrant_client.get_collection(populator.collection_name)
        print(f"Collection '{populator.collection_name}' already exists")
    except:
        # Create collection for embeddings
        populator.qdrant_client.create_collection(
            collection_name=populator.collection_name,
            vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE)
        )
        print(f"Created collection '{populator.collection_name}'")

    # Process the textbook content directory
    textbook_dir = "docs"  # Adjust this path as needed
    await populator.process_directory(textbook_dir)


if __name__ == "__main__":
    asyncio.run(main())