import os
import requests


def call_openai(prompt, user_api_key=None, user_model=None):
    """Call OpenAI API with the given prompt"""
    # Use user key if provided, otherwise fall back to env
    api_key = user_api_key or os.getenv("OPENAI_API_KEY")
    model = user_model or os.getenv("OPENAI_MODEL", "gpt-4o")

    if not api_key:
        return "[OpenAI API key is missing]"

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    data = {"model": model, "messages": [{"role": "user", "content": prompt}]}

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions", headers=headers, json=data
        )
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"[OpenAI error] {str(e)}"
