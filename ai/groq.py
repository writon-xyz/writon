import os
import requests


def call_groq(prompt, user_api_key=None, user_model=None):
    """Call Groq API with the given prompt"""
    # Use user key if provided, otherwise fall back to env
    api_key = user_api_key or os.getenv("GROQ_API_KEY")
    model = user_model or os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")

    if not api_key:
        return "[Groq API key is missing]"

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful writing assistant."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.7,
        "max_tokens": 300,
    }

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data,
        )
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()

    except Exception as e:
        return f"[Groq error] {str(e)}"
