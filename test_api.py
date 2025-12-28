#!/usr/bin/env python3
"""
Test script for the Frontend RAG Integration API
"""
import requests
import json
import time

def test_api_endpoints():
    base_url = "http://127.0.0.1:8000"

    print("Testing Frontend RAG Integration API...")

    # Test health endpoint
    print("\n1. Testing /health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error testing health endpoint: {e}")

    # Test query validation endpoint with valid query
    print("\n2. Testing /validate-query endpoint with valid query...")
    try:
        valid_query = {
            "query_text": "What are the fundamentals of ROS 2?"
        }
        response = requests.post(f"{base_url}/validate-query", json=valid_query)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error testing validate-query endpoint: {e}")

    # Test query validation endpoint with empty query
    print("\n3. Testing /validate-query endpoint with empty query...")
    try:
        empty_query = {
            "query_text": ""
        }
        response = requests.post(f"{base_url}/validate-query", json=empty_query)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 400:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error testing validate-query endpoint with empty query: {e}")

    # Test query validation endpoint with long query
    print("\n4. Testing /validate-query endpoint with long query...")
    try:
        long_query = {
            "query_text": "This is a very long query " + "word " * 500 + "to test the length validation."
        }
        response = requests.post(f"{base_url}/validate-query", json=long_query)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 400:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error testing validate-query endpoint with long query: {e}")

    # Test the main query endpoint (this might take longer due to RAG processing)
    print("\n5. Testing /query endpoint (this may take a moment)...")
    try:
        query = {
            "query_text": "What are the fundamentals of ROS 2?"
        }
        print("Sending query to /query endpoint...")
        response = requests.post(f"{base_url}/query", json=query, timeout=60)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)[:500]}...")
        else:
            print(f"Error Response: {response.text}")
    except requests.exceptions.Timeout:
        print("Request timed out (expected for RAG processing)")
    except Exception as e:
        print(f"Error testing query endpoint: {e}")

if __name__ == "__main__":
    test_api_endpoints()