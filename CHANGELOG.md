# Changelog

All notable changes to Writon will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Updated `fastapi` from `0.118.0` to `0.119.0` - Adds support for mixed Pydantic v1 and v2 models.
- Updated `uvicorn[standard]` from `0.37.0` to `0.38.0` - Adds Python 3.14 support.
- Updated `pydantic` from `2.11.10` to `2.12.3` - New features and bug fixes.

### Fixed
- Fixed Pydantic V2 deprecation warnings by replacing `.dict()` with `.model_dump()` in error handlers.

## [0.1.0] - 2025-09-12

### Added
- 🎉 **Initial Release** - First public release of Writon
- 🧠 **AI-Powered Text Processing** - Grammar correction, translation, and summarization
- 🌍 **Multi-Language Translation** - Support for multiple languages with custom language option
- 📝 **Case Formatting** - lowercase, Sentence case, Title Case, UPPERCASE
- 🔄 **Multi-Provider AI Support** - OpenAI GPT-4, Google Gemini, Anthropic Claude, Groq Llama
- 🔑 **BYOK Model** - Bring Your Own Key for complete privacy
- 🖥️ **CLI Interface** - Interactive command-line tool
- 🌐 **Web API** - RESTful API with FastAPI
- 🎨 **Beautiful Web Interface** - Modern, responsive frontend with space-themed design
- 📱 **Mobile Support** - Fully responsive design
- ⚡ **Production Deployment** - Live at [writon.xyz](https://www.writon.xyz)
- 📚 **API Documentation** - Swagger UI and custom documentation
- 🔒 **Security Features** - Rate limiting, HTTPS, security headers
- 💾 **Auto File Saving** - Organized output with timestamps (CLI)
- ✅ **Comprehensive Testing** - 13 passing tests
- 🤖 **Dependabot Integration** - Automated dependency updates
- 📖 **Professional Documentation** - README, CONTRIBUTING, CHANGELOG
- 🔒 **Branch Protection** - Main branch protection with required pull requests
- 👥 **Code Owners** - Automatic reviewer assignment via CODEOWNERS file
- 📚 **Development Documentation** - Complete DEVELOPMENT_GUIDE.md and QUICK_REFERENCE.md
- 🛡️ **Enhanced Security** - Advanced middleware and security headers
- 📸 **Project Screenshot** - Visual showcase in README
- 📁 **Organized Structure** - Professional docs/ directory for assets

### Features
- **Grammar Correction** - Fix grammar and improve writing quality
- **Translation** - Translate text to any language with context awareness
- **Summarization** - Condense long texts while preserving key information
- **Case Conversion** - Apply consistent formatting across all text
- **File Upload** - Support for .txt, .md, and .rtf files (CLI only)
- **Real-time Processing** - Fast, efficient text processing
- **Error Handling** - Detailed error messages and graceful failures
- **Share Functionality** - Share processed text with others (Web only)
- **Copy & Download** - Easy text export options (Web only)

### Technical
- **FastAPI Backend** - Modern, fast web framework (v0.119.0)
- **ES6 JavaScript Frontend** - Modern web technologies
- **Responsive CSS** - Mobile-first design approach
- **Token Management** - Optimized for long text processing (4000+ tokens)
- **Environment Configuration** - Flexible deployment options
- **Render Deployment** - Production deployment on Render.com
- **GitHub Actions** - Automated dependency updates via Dependabot
- **Latest Dependencies** - All packages updated to latest stable versions
- **Security Patches** - Requests 2.32.5, Python-dotenv 1.1.1
- **Performance Improvements** - Uvicorn 0.38.0, HTTPx 0.28.1
- **Testing Framework** - Pytest 8.4.2 with async support

### Security
- **Rate Limiting** - Prevent abuse and ensure fair usage
- **HTTPS Enforcement** - Secure communication
- **Security Headers** - Protection against common vulnerabilities
- **Input Validation** - Robust data validation and sanitization
- **Privacy First** - No data storage, user keys remain private
- **Branch Protection** - Protected main branch with required reviews
- **Code Review Process** - Mandatory pull requests and approvals

---

## Support

- **Documentation**: [API Docs](https://www.writon.xyz/api-docs.html)
- **Live Demo**: [writon.xyz](https://www.writon.xyz)
- **Issues**: [GitHub Issues](https://github.com/writon-xyz/writon/issues)
- **Email**: hello.writon@gmail.com

---

*For the complete list of changes, see the [Git commit history](https://github.com/writon-xyz/writon/commits/main).*