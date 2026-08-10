# Contributing to Writon

Thank you for your interest in contributing to Writon! 🎉

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- Git
- An API key from one of the supported providers (OpenAI, Google, Anthropic, or Groq)

### Setup Development Environment

1. **Clone the repository**
   ```bash
   git clone https://github.com/sbk-labs/writon.git
   cd writon
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   # Or: python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Run tests**
   ```bash
   pytest
   ```

## 🐛 Reporting Bugs

Found a bug? Please help us fix it!

1. **Check existing issues** - Make sure the bug hasn't been reported already
2. **Create a new issue** with:
   - Clear, descriptive title
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)
   - Screenshots if applicable

## 💡 Suggesting Features

Have an idea for a new feature? We'd love to hear it!

1. **Check existing discussions** - See if your idea has been discussed
2. **Create a new discussion** or issue with:
   - Clear description of the feature
   - Use case and benefits
   - Implementation ideas (if you have any)

## 🔧 Making Changes

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings for functions and classes
- Keep functions focused and small

### Testing
- Add tests for new features
- Ensure all existing tests pass
- Test both CLI and API functionality

### Documentation
- Update README.md if needed
- Add/update docstrings
- Update API documentation

### Pull Request Process

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Add tests** (if applicable)
5. **Run tests** to ensure everything works
6. **Commit your changes**
   ```bash
   git commit -m "Add: your feature description"
   ```
7. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
8. **Create a Pull Request**

### Pull Request Guidelines

- **Clear title** describing the change
- **Detailed description** of what was changed and why
- **Reference related issues** using "Fixes #123" or "Closes #123"
- **Add screenshots** for UI changes
- **Ensure tests pass** and coverage is maintained

## 🏗️ Project Structure

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
├── DEVELOPMENT_GUIDE.md    # Complete development workflow
├── QUICK_REFERENCE.md      # Daily development commands
├── CHANGELOG.md            # Version history
├── SECURITY.md             # Security policy
├── docs/
│   ├── BADGE_STYLE_GUIDE.md # Badge styling standards for documentation
│   └── screenshot.png      # Project screenshots and assets
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

## 🔒 Branch Protection & Code Review

Writon uses branch protection rules to ensure code quality:

- **Main branch protection**: All changes must go through pull requests
- **Required approvals**: At least 1 approval required before merging
- **Code owners**: Automatic reviewer assignment via CODEOWNERS file
- **Conversation resolution**: All discussions must be resolved before merging
- **No bypassing**: Protection rules apply to everyone including administrators

## 🤝 Community Guidelines

- **Be respectful** and inclusive
- **Help others** learn and grow
- **Share knowledge** and best practices
- **Follow the code of conduct**

## 📞 Getting Help

- **GitHub Discussions** - For questions and general discussion
- **GitHub Issues** - For bug reports and feature requests
- **Email** - hello.writon@gmail.com for private matters

## 🎯 Areas We Need Help With

- **Frontend improvements** - UI/UX enhancements
- **Additional AI providers** - Support for more AI services
- **Performance optimization** - Speed and efficiency improvements
- **Documentation** - Better guides and examples
- **Testing** - More comprehensive test coverage
- **Translations** - Multi-language support for the interface

## 📜 License

By contributing to Writon, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Writon! 🙏
