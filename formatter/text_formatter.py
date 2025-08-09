import json
from prompts.prompt_generator import generate_prompt
from ai.provider import call_ai


def format_text(text, vibe, user_keys=None):
    """Format text using specified vibe/mode with optional user keys"""
    try:
        # Load prompt config from modes directory
        with open(f"modes/{vibe}.json", "r") as f:
            vibe_config = json.load(f)

        # Generate structured prompt
        prompt_data = generate_prompt(text, vibe_config)

        # Send to AI model with optional user keys
        response = call_ai(prompt_data, user_keys)
        return response.strip()

    except Exception as e:
        return f"[error formatting text] {str(e)}"


def format_text_with_params(text, vibe, params, user_keys=None):
    """Format text using specified vibe/mode with additional parameters and optional user keys"""
    try:
        # Load prompt config from modes directory
        with open(f"modes/{vibe}.json", "r") as f:
            vibe_config = json.load(f)

        # Generate structured prompt with parameters
        prompt_data = generate_prompt(text, vibe_config, params)

        # Send to AI model with optional user keys
        response = call_ai(prompt_data, user_keys)
        return response.strip()

    except Exception as e:
        return f"[error formatting text] {str(e)}"
