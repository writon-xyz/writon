import os
import json
import requests
from dotenv import load_dotenv
from abc import ABC, abstractmethod

from prompts.prompt_generator import generate_prompt
from formatter.case_converter import convert_case

load_dotenv()

# --- Custom Exceptions ---

class AIProviderError(Exception):
    """Custom exception for AI provider errors."""
    pass

class ConfigurationError(Exception):
    """Custom exception for configuration errors."""
    pass

# --- AI Provider Abstraction ---

class AIProvider(ABC):
    """Abstract base class for all AI providers."""
    def __init__(self, api_key, model):
        if not api_key:
            raise ConfigurationError(f"{self.__class__.__name__} API key is not configured.")
        self.api_key = api_key
        self.model = model

    @abstractmethod
    def call_ai(self, prompt: str) -> str:
        """Calls the AI provider's API and returns the text response."""
        pass

# --- Concrete AI Provider Implementations ---

class OpenAIProvider(AIProvider):
    def call_ai(self, prompt: str) -> str:
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"}
        data = {
            "model": self.model, 
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 4000,
            "temperature": 0.7
        }
        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data, timeout=60)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            raise AIProviderError(f"OpenAI API call failed: {e}")

class GroqProvider(AIProvider):
    def call_ai(self, prompt: str) -> str:
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"}
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a helpful writing assistant."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7,
            "max_tokens": 4000,
        }
        try:
            response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data, timeout=60)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            raise AIProviderError(f"Groq API call failed: {e}")

class GoogleProvider(AIProvider):
    def call_ai(self, prompt: str) -> str:
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4000},
        }
        try:
            response = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}",
                headers=headers,
                json=data,
                timeout=60,
            )
            response.raise_for_status()
            result = response.json()
            if "candidates" in result and len(result["candidates"]) > 0:
                if "content" in result["candidates"][0] and "parts" in result["candidates"][0]["content"]:
                    return result["candidates"][0]["content"]["parts"][0]["text"].strip()
            raise AIProviderError("Google API response is invalid or empty.")
        except Exception as e:
            raise AIProviderError(f"Google API call failed: {e}")

class AnthropicProvider(AIProvider):
    def call_ai(self, prompt: str) -> str:
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }
        data = {
            "model": self.model,
            "max_tokens": 4000,
            "messages": [{"role": "user", "content": prompt}],
        }
        try:
            response = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=data, timeout=60)
            response.raise_for_status()
            result = response.json()
            return result["content"][0]["text"].strip()
        except Exception as e:
            raise AIProviderError(f"Anthropic API call failed: {e}")

# --- Core Logic ---

class WritonCore:
    """
    Handles the core text processing logic by orchestrating AI providers.
    """
    DEFAULT_MODELS = {
        "openai": "gpt-4o",
        "groq": "llama-3.1-8b-instant",
        "google": "gemini-1.5-flash",
        "anthropic": "claude-3-haiku-20240307",
    }

    PROVIDER_CLASSES = {
        "openai": OpenAIProvider,
        "groq": GroqProvider,
        "google": GoogleProvider,
        "anthropic": AnthropicProvider,
    }

    def _get_provider(self, user_keys: dict = None) -> AIProvider:
        """
        Determines the AI provider and credentials to use, then returns an
        instantiated provider object.
        """
        user_keys = user_keys or {}
        provider_name = user_keys.get("provider") or os.getenv("API_PROVIDER")

        if not provider_name or provider_name not in self.PROVIDER_CLASSES:
            raise ConfigurationError(f"Invalid or no provider specified. Available: {list(self.PROVIDER_CLASSES.keys())}")

        api_key = user_keys.get(f"{provider_name}_key") or os.getenv(f"{provider_name.upper()}_API_KEY")
        model = user_keys.get(f"{provider_name}_model") or os.getenv(f"{provider_name.upper()}_MODEL") or self.DEFAULT_MODELS[provider_name]

        if not api_key:
            raise ConfigurationError(f"API key for '{provider_name}' not found in headers or .env.")

        provider_class = self.PROVIDER_CLASSES[provider_name]
        return provider_class(api_key=api_key, model=model)

    def _call_ai(self, prompt_data, user_keys=None) -> str:
        """
        Initializes the correct AI provider and calls it.
        """
        try:
            provider = self._get_provider(user_keys)

            if os.getenv("DEBUG_MODE", "false").lower() == "true":
                key_source = "user-provided" if user_keys else "environment"
                print(f"🧪 Using AI Provider: {provider.__class__.__name__} ({key_source} keys)")

            if isinstance(prompt_data, dict):
                system_msg = prompt_data.get("system", "You are a helpful writing assistant.")
                user_msg = prompt_data.get("user", "")
                full_prompt = f"System: {system_msg}\n\nUser: {user_msg}"
            else:
                full_prompt = prompt_data

            return provider.call_ai(full_prompt)
        except (ConfigurationError, AIProviderError) as e:
            # Re-raise custom exceptions to be handled by the caller
            raise e
        except Exception as e:
            # Catch any other unexpected errors
            raise AIProviderError(f"An unexpected error occurred during AI call: {e}")

    def process_text(self, text: str, mode: str, case_style: str, target_language: str = None, user_keys: dict = None) -> str:
        """Processes text by generating a prompt, calling the AI, and formatting the result."""
        try:
            with open(f"modes/{mode}.json", "r") as f:
                vibe_config = json.load(f)

            params = {"target_language": target_language} if target_language else {}
            prompt_data = generate_prompt(text, vibe_config, params)

            ai_response = self._call_ai(prompt_data, user_keys)

            final_text = convert_case(ai_response, case_style)

            return final_text
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise ConfigurationError(f"Failed to load or parse mode configuration for '{mode}': {e}")
        except Exception as e:
            # Catch and re-raise exceptions from _call_ai or other issues
            raise ValueError(f"Error processing text: {e}")