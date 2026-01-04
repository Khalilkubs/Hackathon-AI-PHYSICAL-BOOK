import os
import cohere
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Cohere API key from environment
api_key = os.getenv('COHERE_API_KEY')

print("Testing different Cohere models with your API key...")

if not api_key:
    print("❌ ERROR: COHERE_API_KEY not found in environment variables")
    exit(1)

print("✅ API key found in environment")

try:
    # Create Cohere client
    print("\n🚀 Creating Cohere client...")
    co = cohere.Client(api_key)
    print("✅ Cohere client created successfully")

    # List of models to test
    models_to_test = [
        ("embed-multilingual-v2.0", "Multilingual v2 (your current model)"),
        ("embed-english-v3.0", "English v3 (newer model)"),
        ("embed-multilingual-v3.0", "Multilingual v3 (newer model)"),
    ]

    for model_name, description in models_to_test:
        print(f"\n🔍 Testing {description} ({model_name})...")
        try:
            response = co.embed(
                texts=["What are the fundamentals of ROS 2?"],
                model=model_name,
                input_type="search_query"  # Required for v3 models
            )

            if response.embeddings and len(response.embeddings) > 0:
                embedding = response.embeddings[0]
                print(f"✅ SUCCESS with {model_name}: Embedding generated ({len(embedding)} dimensions)")
            else:
                print(f"❌ No embeddings returned from {model_name}")

        except cohere.CohereError as e:
            error_str = str(e).lower()
            if "429" in error_str or "too many requests" in error_str:
                print(f"⚠️  429 ERROR with {model_name}: Possible account/trial restrictions")
            elif "401" in error_str or "unauthorized" in error_str:
                print(f"❌ 401 ERROR with {model_name}: Invalid API key")
            elif "403" in error_str or "forbidden" in error_str:
                print(f"❌ 403 ERROR with {model_name}: Access forbidden")
            else:
                print(f"❌ Error with {model_name}: {e}")
        except Exception as e:
            print(f"❌ Unexpected error with {model_name}: {e}")

    print("\n📋 Model testing completed!")
    print("\n💡 NOTES:")
    print("   • The input_type parameter is MANDATORY for v3 models")
    print("   • Trial accounts may have restrictions on newer models")
    print("   • embed-multilingual-v2.0 is often more permissive on trial accounts")
    print("   • If v3 models fail, stick with v2.0 models for now")

except Exception as e:
    print(f"❌ Unexpected error in main test: {e}")