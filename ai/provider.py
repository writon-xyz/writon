import os
from dotenv import load_dotenv

load_dotenv()

from ai.openai import call_openai
from ai.groq import call_groq
from ai.google import call_google
from ai.anthropic import call_anthropic


def call_ai(prompt_data, user_keys=None):
    """Route AI calls to the configured provider with optional user keys"""
    # Get provider from user keys or environment
    if user_keys and "provider" in user_keys:
        provider = user_keys["provider"]
    else:
        provider = os.getenv("API_PROVIDER")

    # Only show debug info if explicitly enabled
    if os.getenv("DEBUG_MODE", "false").lower() == "true":
        key_source = "user-provided" if user_keys else "environment"
        print(f"🧪 Using AI Provider: {provider} ({key_source} keys)")

    if not provider:
        return "[API_PROVIDER is not set in .env file]"

    # Handle structured prompts with system/user messages
    if isinstance(prompt_data, dict):
        system_msg = prompt_data.get("system", "You are a helpful writing assistant.")
        user_msg = prompt_data.get("user", "")
        full_prompt = f"System: {system_msg}\n\nUser: {user_msg}"
    else:
        # Fallback for simple string prompts
        full_prompt = prompt_data

    # Extract user keys and model if provided
    user_api_key = None
    user_model = None

    if user_keys:
        if provider == "openai":
            user_api_key = user_keys.get("openai_key")
            user_model = user_keys.get("openai_model")
        elif provider == "groq":
            user_api_key = user_keys.get("groq_key")
            user_model = user_keys.get("groq_model")
        elif provider == "google":
            user_api_key = user_keys.get("google_key")
            user_model = user_keys.get("google_model")
        elif provider == "anthropic":
            user_api_key = user_keys.get("anthropic_key")
            user_model = user_keys.get("anthropic_model")

    try:
        if provider == "openai":
            return call_openai(full_prompt, user_api_key, user_model)
        elif provider == "groq":
            return call_groq(full_prompt, user_api_key, user_model)
        elif provider == "google":
            return call_google(full_prompt, user_api_key, user_model)
        elif provider == "anthropic":
            return call_anthropic(full_prompt, user_api_key, user_model)
        else:
            return f"[Invalid provider: {provider}. Check API_PROVIDER in .env]"
    except Exception as e:
        return f"[API Error: {str(e)}]"
