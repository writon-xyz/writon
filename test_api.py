"""
Test script for Writon API
Run this after starting the API server to verify everything works
"""

import requests
import json
from time import sleep

API_BASE = "http://localhost:8000"


def test_endpoint(endpoint, method="GET", data=None, description=""):
    """Test an API endpoint"""
    print(f"\n🧪 Testing: {description}")
    print(f"   {method} {endpoint}")

    try:
        if method == "GET":
            response = requests.get(f"{API_BASE}{endpoint}")
        elif method == "POST":
            response = requests.post(f"{API_BASE}{endpoint}", json=data)

        print(f"   Status: {response.status_code}")

        if response.status_code == 200:
            print("   ✅ Success")
            result = response.json()
            if isinstance(result, dict) and len(result) <= 5:
                print(f"   Response: {json.dumps(result, indent=2)}")
            else:
                print("   Response: [Large response - check manually]")
        else:
            print("   ❌ Failed")
            print(f"   Error: {response.text}")

    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")

    return response.status_code == 200


def main():
    print("🚀 Testing Writon API")
    print("=" * 50)

    # Test basic endpoints
    test_endpoint("/", description="Root endpoint")
    test_endpoint("/health", description="Health check")
    test_endpoint("/providers", description="Available providers")

    # Test text processing endpoints
    sample_text = "this text have some grammar mistake and need fix"

    # Test grammar correction
    grammar_data = {"text": sample_text, "case_style": "sentence"}
    test_endpoint("/grammar", "POST", grammar_data, "Grammar correction")

    # Test summarization
    long_text = "Artificial intelligence is transforming the way we work and live. Machine learning algorithms can now process vast amounts of data and identify patterns that humans might miss. This technology is being applied in healthcare, finance, transportation, and many other industries. As AI continues to evolve, it's important to consider both the benefits and potential risks."

    summarize_data = {"text": long_text, "case_style": "title"}
    test_endpoint("/summarize", "POST", summarize_data, "Text summarization")

    # Test translation
    translate_data = {
        "text": "Hello, how are you today?",
        "target_language": "Spanish",
        "case_style": "sentence",
    }
    test_endpoint("/translate", "POST", translate_data, "Translation to Spanish")

    # Test main process endpoint
    process_data = {"text": sample_text, "mode": "grammar", "case_style": "upper"}
    test_endpoint("/process", "POST", process_data, "Main process endpoint")

    print("\n" + "=" * 50)
    print("🏁 Testing complete!")
    print("   Visit http://localhost:8000/docs for interactive API documentation")


if __name__ == "__main__":
    print("⏳ Waiting 2 seconds for API to be ready...")
    sleep(2)
    main()
