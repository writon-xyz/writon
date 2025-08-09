import os
import requests


def call_anthropic(prompt, user_api_key=None, user_model=None):
    """Call Anthropic Claude API with the given prompt"""
    # Use user key if provided, otherwise fall back to env
    api_key = user_api_key or os.getenv("ANTHROPIC_API_KEY")
    model = user_model or os.getenv("ANTHROPIC_MODEL", "claude-3-haiku-20240307")

    if not api_key:
        return "[Anthropic API key is missing]"

    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
    }

    data = {
        "model": model,
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": prompt}],
    }

    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages", headers=headers, json=data
        )
        response.raise_for_status()
        result = response.json()
        return result["content"][0]["text"].strip()
    except Exception as e:
        return f"[Anthropic error] {str(e)}"
