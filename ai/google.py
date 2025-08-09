import os
import requests


def call_google(prompt, user_api_key=None, user_model=None):
    """Call Google Gemini API with the given prompt"""
    # Use user key if provided, otherwise fall back to env
    api_key = user_api_key or os.getenv("GOOGLE_API_KEY")
    model = user_model or os.getenv("GOOGLE_MODEL", "gemini-1.5-flash")

    if not api_key:
        return "[Google API key is missing]"

    headers = {"Content-Type": "application/json"}

    # Google Gemini API format
    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 1024},
    }

    try:
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}",
            headers=headers,
            json=data,
        )
        response.raise_for_status()
        result = response.json()

        # Extract text from Google's response format
        if "candidates" in result and len(result["candidates"]) > 0:
            if (
                "content" in result["candidates"][0]
                and "parts" in result["candidates"][0]["content"]
            ):
                return result["candidates"][0]["content"]["parts"][0]["text"].strip()

        return "[Google error] No valid response received"

    except Exception as e:
        return f"[Google error] {str(e)}"
