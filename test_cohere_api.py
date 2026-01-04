import os
import cohere
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Cohere API key from environment
api_key = os.getenv('COHERE_API_KEY')

print("Testing your Cohere API key directly...")

if not api_key:
    print("❌ ERROR: COHERE_API_KEY not found in environment variables")
    print("Please make sure your .env file contains: COHERE_API_KEY='your_key_here'")
    exit(1)

print("✅ API key found in environment")
print(f"API key starts with: {api_key[:10]}...")  # Show only first 10 chars for security

try:
    # Create Cohere client
    print("\n🚀 Creating Cohere client...")
    co = cohere.Client(api_key)
    print("✅ Cohere client created successfully")

    # Test embedding generation with a simple query related to your book
    print("\n🔍 Testing embedding generation...")
    test_query = "What are the fundamentals of ROS 2?"

    # Test with the model you're currently using
    print("Testing with embed-multilingual-v2.0...")
    response = co.embed(
        texts=[test_query],
        model="embed-multilingual-v2.0",  # Using the same model as your system
        input_type="search_query"  # Required parameter for v3 models
    )

    if response.embeddings and len(response.embeddings) > 0:
        embedding = response.embeddings[0]
        print(f"✅ SUCCESS: Embedding generated successfully!")
        print(f"📊 Embedding dimensions: {len(embedding)}")
        print(f"🔢 Sample embedding values: {embedding[:5]}...")  # Show first 5 values
        print("\n🎉 Your Cohere API key is working correctly!")
        print("💡 The issue might be elsewhere in your system, not with the API key itself.")
    else:
        print("❌ ERROR: No embeddings returned from API")

except cohere.CohereError as e:
    print(f"❌ Cohere API Error: {e}")
    print(f"📋 Error type: {type(e).__name__}")

    # Check for specific error codes
    error_str = str(e).lower()
    if "429" in error_str or "too many requests" in error_str:
        print("\n⚠️  429 ERROR - Rate Limiting or Account Issue:")
        print("   • This might be due to account restrictions, not rate limiting")
        print("   • Trial accounts often have lower limits than expected")
        print("   • Check if your account needs verification")
        print("   • Verify your subscription tier in Cohere dashboard")
    elif "401" in error_str or "unauthorized" in error_str:
        print("\n❌ 401 ERROR - Invalid API Key:")
        print("   • Your API key might be incorrect")
        print("   • Please verify your COHERE_API_KEY in the .env file")
    elif "403" in error_str or "forbidden" in error_str:
        print("\n❌ 403 ERROR - Access Forbidden:")
        print("   • Your API key might not have proper permissions")
        print("   • Check your Cohere account status")
    else:
        print(f"\n❓ Other Cohere Error: {e}")

except Exception as e:
    print(f"❌ Unexpected error: {e}")
    print(f"📋 Error type: {type(e).__name__}")

    # Check if it's a 429 error
    error_str = str(e).lower()
    if "429" in error_str or "too many requests" in error_str:
        print("\n⚠️  429 ERROR - Possible Rate Limiting or Account Issue:")
        print("   • Even with new accounts, Cohere might have soft limits")
        print("   • Trial accounts often have unexpected restrictions")
        print("   • Check your Cohere dashboard for usage statistics")
        print("   • Verify account verification status")
        print("   • Consider if there are geographic restrictions")

print("\n📋 Test completed!")