from dotenv import load_dotenv
import os

load_dotenv()

print("API_PROVIDER:", os.getenv("API_PROVIDER"))
print()

# Show configurations for all providers
provider = os.getenv("API_PROVIDER")

if provider == "groq":
    print(
        "GROQ_API_KEY:",
        (
            os.getenv("GROQ_API_KEY", "Not set")[:10] + "..."
            if os.getenv("GROQ_API_KEY")
            else "Not set"
        ),
    )
    print("GROQ_MODEL:", os.getenv("GROQ_MODEL", "Not set"))
elif provider == "google":
    print(
        "GOOGLE_API_KEY:",
        (
            os.getenv("GOOGLE_API_KEY", "Not set")[:10] + "..."
            if os.getenv("GOOGLE_API_KEY")
            else "Not set"
        ),
    )
    print("GOOGLE_MODEL:", os.getenv("GOOGLE_MODEL", "Not set"))
elif provider == "openai":
    print(
        "OPENAI_API_KEY:",
        (
            os.getenv("OPENAI_API_KEY", "Not set")[:10] + "..."
            if os.getenv("OPENAI_API_KEY")
            else "Not set"
        ),
    )
    print("OPENAI_MODEL:", os.getenv("OPENAI_MODEL", "Not set"))
elif provider == "anthropic":
    print(
        "ANTHROPIC_API_KEY:",
        (
            os.getenv("ANTHROPIC_API_KEY", "Not set")[:10] + "..."
            if os.getenv("ANTHROPIC_API_KEY")
            else "Not set"
        ),
    )
    print("ANTHROPIC_MODEL:", os.getenv("ANTHROPIC_MODEL", "Not set"))
else:
    print(
        "Invalid or missing API_PROVIDER. Valid options: openai, google, anthropic, groq"
    )

print()
print("DEBUG_MODE:", os.getenv("DEBUG_MODE", "false"))
