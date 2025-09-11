import pytest
import httpx
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_health_check():
    """Tests the /health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status"] in ["healthy", "warning"]
    assert "version" in json_response
    assert "provider" in json_response

def test_get_providers():
    """Tests the /providers endpoint."""
    response = client.get("/providers")
    assert response.status_code == 200
    json_response = response.json()
    assert "available_providers" in json_response
    assert "current_provider" in json_response
    assert "supported_modes" in json_response
    assert "supported_cases" in json_response
    assert isinstance(json_response["available_providers"], list)
    assert isinstance(json_response["supported_modes"], list)
    assert isinstance(json_response["supported_cases"], list)

def test_grammar_endpoint():
    """Tests the /grammar endpoint with a simple request."""
    response = client.post("/grammar", json={"text": "this is a test", "case_style": "sentence"})
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["mode"] == "grammar"
    assert json_response["original_text"] == "this is a test"
    assert "processed_text" in json_response

def test_summarize_endpoint():
    """Tests the /summarize endpoint with a simple request."""
    response = client.post("/summarize", json={"text": "this is a test to summarize", "case_style": "sentence"})
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["mode"] == "summarize"
    assert json_response["original_text"] == "this is a test to summarize"
    assert "processed_text" in json_response

def test_translate_endpoint():
    """Tests the /translate endpoint with a simple request."""
    response = client.post("/translate", json={"text": "hello", "target_language": "spanish", "case_style": "sentence"})
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["mode"] == "translate"
    assert json_response["original_text"] == "hello"
    assert json_response["target_language"] == "spanish"
    assert "processed_text" in json_response

# --- New Tests for Invalid Inputs and Edge Cases ---

def test_invalid_mode():
    """Tests providing an invalid mode to the /process endpoint."""
    response = client.post("/process", json={"text": "test", "mode": "invalid_mode", "case_style": "sentence"})
    assert response.status_code == 422  # Unprocessable Entity

def test_missing_text():
    """Tests a request to /grammar with a missing 'text' field."""
    response = client.post("/grammar", json={"case_style": "sentence"})
    assert response.status_code == 422

def test_translate_missing_language():
    """Tests the /translate endpoint without the required 'target_language'."""
    response = client.post("/translate", json={"text": "hello", "case_style": "sentence"})
    assert response.status_code == 422

# --- New Tests for BYOK (Bring Your Own Key) Functionality ---

@pytest.mark.parametrize("provider", ["groq", "openai"])
def test_byok_headers(provider, mocker):
    """Tests that BYOK headers are correctly used to call the right provider."""
    # Mock the core's process_text method to capture the user_keys parameter
    mock_process_text = mocker.patch(
        "api.core.process_text", 
        return_value="mocked response"
    )

    headers = {
        "X-Provider": provider,
        f"X-{provider.title()}-Key": "test-key-1234"  # Maps to x-groq-key or x-openai-key
    }
    response = client.post("/grammar", json={"text": "test with byok"}, headers=headers)

    # Check that the request was successful
    assert response.status_code == 200
    
    # Check that process_text was called
    mock_process_text.assert_called_once()
    
    # Inspect the user_keys dictionary that was passed to process_text
    call_args = mock_process_text.call_args[1]  # keyword arguments
    user_keys_arg = call_args.get('user_keys', {})
    
    assert user_keys_arg.get("provider") == provider
    assert user_keys_arg.get(f"{provider}_key") == "test-key-1234"