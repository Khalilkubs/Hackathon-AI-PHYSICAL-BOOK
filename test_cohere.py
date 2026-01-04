import os
from dotenv import load_dotenv
import cohere

# Load environment variables
load_dotenv()

# Get the Cohere API key
api_key = os.getenv('COHERE_API_KEY')
print(f"Cohere API Key loaded: {'Yes' if api_key else 'No'}")

if api_key:
    try:
        # Test the Cohere client
        co = cohere.Client(api_key)
        print("Cohere client created successfully")

        # Test embedding generation
        response = co.embed(
            texts=["test query"],
            model="embed-multilingual-v2.0",
            input_type="search_query"
        )
        print(f"Embedding generated successfully with {len(response.embeddings[0])} dimensions")
        print("Cohere API is working correctly!")
    except Exception as e:
        print(f"Error with Cohere API: {e}")
        print("This might be due to rate limiting or other API issues")
else:
    print("No Cohere API key found in environment")