# 📝 Writon

[![Live Demo](https://img.shields.io/badge/Live%20Demo-writon.xyz-blue?style=for-the-badge&logo=internet-explorer)](https://www.writon.xyz)
[![API Documentation](https://img.shields.io/badge/API%20Docs-Swagger-green?style=for-the-badge&logo=swagger)](https://www.writon.xyz/docs)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/downloads/)

> **AI-powered text processor** with CLI and API interfaces for grammar correction, translation, and summarization.

**Writon** transforms your text with AI while maintaining your intent and applying consistent case formatting. Clean, fast, and reliable - available as both a command-line tool and a web API.

## 🌟 Live Demo

**Try Writon right now!** → [**www.writon.xyz**](https://www.writon.xyz)

- ✨ **Grammar Correction** - Fix grammar and improve writing
- 🌍 **Translation** - Translate to multiple languages with custom language support  
- 📝 **Summarization** - Condense long texts intelligently
- 🔑 **BYOK Model** - Use your own API keys for privacy

## 🚀 Two Ways to Use Writon

### 1. CLI (Command Line Interface)
Interactive terminal application for direct text processing.

### 2. API (Web API)
RESTful API for integration with applications, websites, and services.

## ✨ Features

- 🧠 **AI-Powered Processing**: Grammar correction, translation, and summarization
- 🌍 **Multi-Language Translation**: Built-in presets + custom language support
- 📝 **Case Formatting**: lowercase, Sentence case, Title Case, UPPERCASE
- 🔄 **Multi-Provider AI**: Supports OpenAI, Google Gemini, Anthropic Claude, and Groq
- 🔑 **BYOK (Bring Your Own Key)**: Use your own API keys for complete privacy
- ⚡ **Lightning Fast**: Optimized for speed and reliability
- 🎨 **Beautiful UI**: Modern, responsive web interface
- 📱 **Mobile Friendly**: Works perfectly on all devices
- 🔒 **Privacy First**: Your data stays with you
- 🚀 **Production Ready**: Deployed and running at writon.xyz

## 🛠️ Tech Stack

**Backend:**
- ![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
- ![FastAPI](https://img.shields.io/badge/FastAPI-0.117+-green?logo=fastapi)
- ![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI-red)

**Frontend:**
- ![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5)
- ![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3)
- ![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?logo=javascript)

**AI Providers:**
- ![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-black?logo=openai)
- ![Google](https://img.shields.io/badge/Google-Gemini-blue?logo=google)
- ![Anthropic](https://img.shields.io/badge/Anthropic-Claude-orange)
- ![Groq](https://img.shields.io/badge/Groq-Llama--3--70B-purple)

**Deployment:**
- ![Render](https://img.shields.io/badge/Render-Deployed-46E3B7?logo=render)
- ![GitHub](https://img.shields.io/badge/GitHub-CI%2FCD-black?logo=github)
- ✨ **Backend Zero-Config**: Backend works out-of-the-box with Groq's free tier when `API_PROVIDER` is set in `.env`. Frontend requires API key input.
- 🔑 **BYOK Support**: Bring Your Own Key - users can use their own API keys
- 💾 **Auto File Saving**: Organized output with timestamp naming (CLI)
- ✅ **Input Validation**: Robust error handling and user guidance
- 🚪 **Graceful Exit**: Clean Ctrl+C and Ctrl+D handling (CLI)
- 🌐 **REST API**: JSON endpoints for programmatic access
- 📚 **Interactive Docs**: Auto-generated API documentation
- 🔒 **Secure**: No API keys stored on server (when using BYOK mode)

## ⚙️ Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/writon-xyz/writon.git
cd writon

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# For development, install in editable mode (after creating pyproject.toml)
pip install -e .

# Set up environment
cp .env.example .env
# Edit .env with your API keys
```

### CLI Usage

```bash
python main.py
```

### API Usage

```bash
# Start the API server in one terminal
uvicorn api:app --host 0.0.0.0 --port 8000 --reload



# Or visit the interactive documentation in your browser
# http://localhost:8000/docs
```

## 📝 CLI Example

```
Writon CLI - AI-powered text processor
Enter your text: This have a grammar mistake, please fix it.

Select mode:
1. Fix Grammar
2. Translate
3. Summarize
> 1

Select case:
1. lowercase
2. Sentence case
3. Title Case
4. UPPERCASE
> 2

Processing Summary:
   Mode: Fix Grammar
   Case: Sentence case

Proceed? (y/n): y

Processing with AI...

Formatted text:
This has a grammar mistake, please fix it.

Save to file? (y/n): y
Saved to output/gram_20250809_163000.txt
```

## 💻 API Example

### Grammar Correction (BYOK Mode)
This example uses a Groq API key via headers.

```bash
curl -X POST "http://localhost:8000/grammar" \
  -H "Content-Type: application/json" \
  -H "X-Provider: groq" \
  -H "X-Groq-Key: your_groq_api_key_here" \
  -d '{
    "text": "this text have grammar mistake",
    "case_style": "sentence"
  }'
```

### Translation (BYOK Mode)
This example uses an OpenAI API key via headers.

```bash
curl -X POST "http://localhost:8000/translate" \
  -H "Content-Type: application/json" \
  -H "X-Provider: openai" \
  -H "X-OpenAI-Key: your_openai_api_key_here" \
  -d '{
    "text": "Hello, how are you?",
    "target_language": "Spanish",
    "case_style": "sentence"
  }'
```

### Python Client Example

```python
import requests

# Using user's keys (BYOK - Bring Your Own Key)
headers = {
    "Content-Type": "application/json",
    "X-Provider": "groq",
    "X-Groq-Key": "your_groq_api_key_here"
}

response = requests.post("http://localhost:8000/grammar",
    json={"text": "this have bad grammar", "case_style": "sentence"},
    headers=headers
)

result = response.json()
print(result["processed_text"])
# Output: "This has bad grammar."
```

## 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|---------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check and provider status |
| `/providers` | GET | Available providers and configuration |
| `/grammar` | POST | Grammar correction |
| `/translate` | POST | Text translation |
| `/summarize` | POST | Text summarization |
| `/process` | POST | Universal endpoint (all modes) |
| `/upload` | POST | Upload a text file |

### Interactive Documentation
Visit `http://localhost:8000/docs` for full API documentation with:

- Request/response schemas
- Try-it-out functionality
- Parameter descriptions
- Example requests

## API Headers (BYOK Mode)

To use your own API keys, include these headers in requests:

| Header | Description | Example |
|--------|-------------|---------|
| `X-Provider` | AI provider to use | `groq`, `openai`, `google`, `anthropic` |
| `X-OpenAI-Key` | OpenAI API key | `sk-...` |
| `X-Groq-Key` | Groq API key | `gsk_...` |
| `X-Google-Key` | Google Gemini API key | `AI...` |
| `X-Anthropic-Key` | Anthropic API key | `sk-ant-...` |
| `X-OpenAI-Model` | OpenAI model (optional) | `gpt-4o`, `gpt-3.5-turbo` |
| `X-Groq-Model` | Groq model (optional) | `llama-3.1-70b-versatile` |
| `X-Google-Model` | Google model (optional) | `gemini-1.5-flash` |
| `X-Anthropic-Model` | Anthropic model (optional) | `claude-3-haiku-20240307` |

Example with custom headers:

```bash
curl -X POST "http://localhost:8000/grammar" \
  -H "Content-Type: application/json" \
  -H "X-Provider: groq" \
  -H "X-Groq-Key: your_groq_key_here" \
  -H "X-Groq-Model: llama-3.1-70b-versatile" \
  -d '{"text": "fix this grammar", "case_style": "sentence"}'
```

## Processing Modes

### 1. Grammar
Fixes grammar, spelling, and punctuation while preserving your original tone and intent.

### 2. Translation
Translates text to your target language with perfect grammar in the destination language.

**Supported languages:**
- Hindi, Maori, Arabic, French, German, Swahili, English, Spanish, Tok Pisin, Portuguese, Mandarin Chinese
- Custom language input for any other language

### 3. Summarization
Creates concise summaries while maintaining grammatical accuracy and key information.

## Configuration

Writon is configured to work out-of-the-box using Groq. For most users, you only need to get a free Groq API key and place it in your `.env` file.

### For CLI and API Server
Create a `.env` file by copying the `.env.example` (`cp .env.example .env`). Then, add your Groq key.

```env
# The default provider is Groq. You can optionally switch to openai, google, or anthropic.
API_PROVIDER=groq

# Groq Configuration (Recommended for easy setup)
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-70b-versatile

# --- Optional Providers ---

# Google Configuration  
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_MODEL=gemini-1.5-flash

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o

# Anthropic Configuration
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ANTHROPIC_MODEL=claude-3-haiku-20240307

# Debug mode (optional)
DEBUG_MODE=false

# CORS Configuration (optional)
# Comma-separated list of allowed origins for API access
ALLOWED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000

# Security Configuration (optional)
# Environment (development/production)
ENVIRONMENT=development

# Request and file size limits
MAX_REQUEST_SIZE_MB=1
MAX_FILE_SIZE_MB=5

# Trusted hosts for production (comma-separated)
ALLOWED_HOSTS=writon.xyz,*.writon.xyz
```

> **Note:** For advanced use, you can switch the `API_PROVIDER` and provide the corresponding API key. In API mode, keys can also be provided directly via headers (see BYOK mode).

## Output Files (CLI)

Processed text is automatically saved to the `output/` folder with descriptive names:

- `gram_20250801_143022.txt` - Grammar correction
- `trans_spanish_20250801_143045.txt` - Translation to Spanish
- `summ_20250801_143100.txt` - Summarization

## Error Handling

Writon gracefully handles common issues:

- **No internet connection**: Clear error message with guidance
- **Invalid API keys**: Helpful error message and .env file guidance
- **Rate limiting**: Detects and displays rate limit errors
- **Malformed responses**: Automatic error detection and fallback
- **Frontend errors**: Now displayed with clear messages.

## Security Features

Writon includes comprehensive security measures:

- **Rate Limiting**: 30 requests/minute for processing, 10/minute for uploads
- **Request Size Limits**: 1MB maximum request size
- **File Size Limits**: 5MB maximum file upload size
- **Security Headers**: XSS protection, content type validation, frame options
- **CORS Protection**: Configurable allowed origins
- **HTTPS Enforcement**: Automatic redirect in production
- **Trusted Hosts**: Host validation in production
- **Input Validation**: Strict validation for all API inputs
- **File Type Validation**: Only allows safe text file types
- **BYOK Model**: No API keys stored on server

## 📁 Architecture

```
writon/
├── main.py                 # CLI interface and user interaction
├── api.py                  # FastAPI web server
├── LICENSE
├── .gitignore              # Git ignore rules
├── .env.example            # Environment configuration template
├── render.yaml             # Render deployment configuration
├── .github/
│   └── dependabot.yml      # Automated dependency updates
├── CODEOWNERS              # Automatic reviewer assignment
├── requirements.txt        # All dependencies
├── pyproject.toml          # Project configuration and build metadata
├── README.md               # This documentation
├── CONTRIBUTING.md         # Contribution guidelines
├── CHANGELOG.md            # Version history
├── SECURITY.md             # Security policy
├── core/
│   ├── __init__.py
│   └── writon.py           # Core business logic and AI integration
├── formatter/
│   └── case_converter.py   # Deterministic case transformations
├── frontend/
│   ├── assets/
│   │   ├── favicon.ico     # Browser icon
│   │   ├── logo.PNG        # Application logo
│   │   ├── horizontal.jpg  # Horizontal banner image
│   │   └── portrait.jpg    # Portrait banner image
│   ├── js/
│   │   ├── main.js         # Main web application logic
│   │   ├── api.js          # API communication
│   │   ├── config.js       # Configuration management
│   │   ├── events.js       # Event handling
│   │   └── ui.js           # UI interactions
│   ├── api-docs.html       # API documentation website
│   ├── index.html          # Main web application
│   └── style.css           # Frontend styling
├── modes/
│   ├── grammar.json        # Grammar correction configuration
│   ├── translate.json      # Translation configuration
│   └── summarize.json      # Summarization configuration
├── prompts/
│   └── prompt_generator.py # Template engine for AI prompts
├── tests/
│   ├── test_api_pytest.py  # API testing script
│   ├── test_core.py        # Core logic testing script
│   └── check_env.py        # Environment configuration tester
├── output/                 # Auto-generated output files (CLI)
└── __pycache__/            # Python cache files (auto-generated)
```

## 📚 Supporting Files

- **LICENSE**: The project's MIT License
- **favicon.ico**: The project favicon
- **logo.PNG**: The project logo

## Requirements

- Python 3.7+
- See `requirements.txt` for complete dependency list
- API key for at least one supported provider

### Core Dependencies

- `requests` - HTTP client for AI APIs
- `python-dotenv` - Environment configuration
- `fastapi` - Web API framework
- `uvicorn` - ASGI web server
- `pydantic` - Data validation

## Supported AI Providers

- **OpenAI**: GPT-4, GPT-3.5, and newer models
- **Google**: Gemini Pro, Gemini Flash, and Gemini models
- **Anthropic**: Claude 3 family models
- **Groq**: Fast inference with Llama and open source models

## Testing

### Test CLI
```bash
python main.py
```

### Test API
```bash
# Start API in one terminal
uvicorn api:app --reload

# Run tests in another terminal using pytest
.venv/bin/pytest tests/
# Or, if you prefer running pytest as a module:
.venv/bin/python -m pytest tests/

# Or visit http://localhost:8000/docs
```

## Use Cases

### CLI
- Personal text processing
- Batch file processing
- Scripting and automation
- Development and testing

### API
- Web applications
- Mobile app backends
- Microservices integration
- Third-party application integration
- Android keyboard development
- SaaS applications with BYOK model
- Multi-tenant applications

## 🤝 Contributing

We welcome contributions to Writon! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on how to:

- Report bugs and request features
- Set up your development environment
- Submit pull requests
- Follow our code style and testing standards

The modular architecture makes it easy to:
- Add new AI providers
- Create additional processing modes
- Extend case formatting options
- Improve error handling
- Add new API endpoints

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Writon: Transform text with AI - CLI for developers, API for applications** 🚀
