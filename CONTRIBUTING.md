# Contributing to Writon

Thank you for your interest in contributing to Writon! 🎉

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- An API key from one of the supported providers (OpenAI, Google, Anthropic, or Groq)

### Setup Development Environment

1. **Clone the repository**
   ```bash
   git clone https://github.com/writon-xyz/writon.git
   cd writon
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
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
├── main.py              # CLI interface
├── api.py               # FastAPI web server
├── core/
│   └── writon.py        # Core business logic
├── formatter/
│   └── case_converter.py # Case formatting utilities
├── prompts/
│   └── prompt_generator.py # AI prompt generation
├── frontend/            # Web interface
│   ├── index.html
│   ├── style.css
│   └── js/
├── tests/               # Test suite
├── requirements.txt     # Python dependencies
└── README.md           # Project documentation
```

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
