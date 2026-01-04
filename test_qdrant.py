import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient

# Load environment variables
load_dotenv()

# Connect to Qdrant
client = QdrantClient(
    url=os.getenv('QDRANT_URL'),
    api_key=os.getenv('QDRANT_API_KEY'),
    https=True
)

collection_name = os.getenv('QDRANT_COLLECTION_NAME', 'document_embeddings')
print(f'Connected to collection: {collection_name}')

# Get collection info
collection_info = client.get_collection(collection_name)
print(f'Total points in collection: {collection_info.points_count}')

# Sample a few points to see what content is actually stored
try:
    # Get a few points to examine the content
    points = client.scroll(
        collection_name=collection_name,
        limit=2,
        with_payload=True,
        with_vectors=False
    )

    print('\nSample points from your collection:')
    for i, point in enumerate(points[0][:2]):  # Show first 2 points
        payload = point.payload
        print(f'\nPoint {i+1}:')
        print(f'  ID: {point.id}')
        print(f'  Document Title: {payload.get("document_title", "N/A")}')
        print(f'  Source URL: {payload.get("source_url", "N/A")}')
        print(f'  Content preview: {payload.get("content", "")[0:200]}...')
        print(f'  Chunk ID: {payload.get("chunk_id", "N/A")}')

except Exception as e:
    print(f'Error retrieving sample points: {e}')