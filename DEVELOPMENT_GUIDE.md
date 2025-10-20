# 🚀 Writon Development Guide

**Complete blueprint for contributing to and maintaining the Writon project.**

## 📋 Quick Reference

### Repository Information
- **Organization**: `@writon-xyz`
- **Personal Account**: `@etsibeko-dev`
- **Repository**: `https://github.com/writon-xyz/writon`
- **Live Site**: `https://www.writon.xyz`

### Branch Protection Rules
- ✅ **Main branch protected** - All changes must go through PRs
- ✅ **Admin bypass enabled** - `@writon-xyz` can push directly
- ✅ **Code owners** - `@writon-xyz` and `@etsibeko-dev` auto-assigned as reviewers

---

## 🔧 Development Setup

### 1. Clone and Setup
```bash
# Clone the repository
git clone https://github.com/writon-xyz/writon.git
cd writon

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your API keys
```

### 2. Development Commands
```bash
# Run the API server locally
uvicorn api:app --host 0.0.0.0 --port 8000 --reload

# Run tests
python -m pytest tests/ -v

# Run CLI
python main.py

# Check code quality
python -m flake8 . --max-line-length=88
```

---

## 📝 Commit Message Standards

### Format
```
<type>: <description>

[optional body]

[optional footer]
```

### Types
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code formatting (no logic changes)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks, dependency updates
- `perf:` - Performance improvements
- `ci:` - CI/CD changes
- `build:` - Build system changes

### Examples

#### Feature Development
```bash
git commit -m "feat: Add new AI provider integration

- Added support for OpenAI GPT-4 Turbo
- Updated provider selection UI
- Added corresponding tests

Closes #123"
```

#### Bug Fixes
```bash
git commit -m "fix: Resolve frontend JavaScript errors on API docs page

- Added null checks for DOM elements
- Fixed mobile menu navigation
- Improved error handling

Fixes #456"
```

#### Documentation
```bash
git commit -m "docs: Update README with latest dependency versions

- Updated FastAPI version badge to 0.119+
- Added new feature descriptions
- Fixed broken links"
```

#### Dependency Updates
```bash
git commit -m "chore: Update dependencies to latest versions

- Updated FastAPI from 0.118.0 to 0.119.0
- Updated Uvicorn from 0.37.0 to 0.38.0
- Updated Pydantic from 2.11.10 to 2.12.3
- All tests pass with updated dependencies
- Consolidates multiple Dependabot PRs"
```

#### Security Updates
```bash
git commit -m "fix: Update requests library for security patches

- Updated requests from 2.31.0 to 2.32.5
- Addresses CVE-2024-XXXX
- No breaking changes introduced"
```

---

## 🔄 Git Workflow Patterns

### 1. Feature Development (Recommended)
```bash
# Create feature branch
git checkout -b feature/new-ai-provider
git push -u origin feature/new-ai-provider

# Make changes, commit with descriptive messages
git add .
git commit -m "feat: Add initial provider integration"

# Push changes
git push origin feature/new-ai-provider

# Create PR on GitHub
# Merge after review and approval
```

### 2. Hotfix (Emergency)
```bash
# Create hotfix branch
git checkout -b hotfix/critical-security-fix
git push -u origin hotfix/critical-security-fix

# Make urgent fix
git add .
git commit -m "fix: Critical security vulnerability in API endpoint

- Sanitized user input
- Added additional validation
- Updated rate limiting

Fixes CVE-2024-XXXX"

# Push and create PR immediately
git push origin hotfix/critical-security-fix
```

### 3. Documentation Updates
```bash
# Create docs branch
git checkout -b docs/update-api-documentation
git push -u origin docs/update-api-documentation

# Update documentation
git add .
git commit -m "docs: Update API documentation with new endpoints

- Added examples for new grammar endpoint
- Updated authentication section
- Fixed typos in README"

git push origin docs/update-api-documentation
```

### 4. Dependency Updates
```bash
# For individual dependency updates
git checkout -b chore/update-fastapi
git add requirements.txt
git commit -m "chore: Update FastAPI to 0.119.0

- Updated FastAPI from 0.118.0 to 0.119.0
- All tests pass with new version
- No breaking changes detected"

git push origin chore/update-fastapi

# For batch updates (like we did)
git checkout main
# Manually update requirements.txt with multiple versions
git add requirements.txt
git commit -m "chore: Update dependencies to latest versions

- Updated FastAPI from 0.118.0 to 0.119.0
- Updated Uvicorn from 0.37.0 to 0.38.0
- Updated Pydantic from 2.11.10 to 2.12.3
- All tests pass with updated dependencies
- Consolidates multiple Dependabot PRs"

git push origin main
```

---

## 👥 Multi-Account Workflow

### Working as @writon-xyz (Organization)
```bash
# Set up Git credentials for organization
git config user.name "writon-xyz"
git config user.email "hello.writon@gmail.com"

# You can push directly to main (admin bypass)
git push origin main
```

### Working as @etsibeko-dev (Personal)
```bash
# Set up Git credentials for personal account
git config user.name "etsibeko-dev"
git config user.email "your-personal-email@gmail.com"

# Must use PR workflow
git checkout -b feature/my-feature
git push -u origin feature/my-feature
# Create PR on GitHub
```

### Switching Between Accounts
```bash
# Check current configuration
git config user.name
git config user.email

# Switch to organization account
git config user.name "writon-xyz"
git config user.email "hello.writon@gmail.com"

# Switch to personal account
git config user.name "etsibeko-dev"
git config user.email "your-personal-email@gmail.com"
```

---

## 🚀 Deployment Workflow

### Automatic Deployment
- **Render.com** automatically deploys from `main` branch
- **Custom Domain**: `www.writon.xyz`
- **Environment Variables**: Set in Render dashboard

### Manual Deployment Steps
```bash
# 1. Ensure all tests pass
python -m pytest tests/ -v

# 2. Commit and push changes
git add .
git commit -m "feat: Add new feature for production"
git push origin main

# 3. Monitor deployment
# Check Render.com dashboard for build logs
# Test live site: https://www.writon.xyz
```

### Environment Variables (Render)
```
API_PROVIDER=groq
ENVIRONMENT=production
ALLOWED_ORIGINS=https://www.writon.xyz
ALLOWED_HOSTS=www.writon.xyz
MAX_REQUEST_SIZE_MB=1
MAX_FILE_SIZE_MB=5
DEBUG_MODE=false
```

---

## 🧪 Testing Standards

### Running Tests
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_api_pytest.py -v

# Run with coverage
python -m pytest tests/ --cov=core --cov=api

# Run tests in watch mode
python -m pytest tests/ -f
```

### Test Commit Messages
```bash
git commit -m "test: Add comprehensive API endpoint tests

- Added tests for all processing modes
- Added error handling tests
- Added BYOK header validation tests
- Achieved 95% code coverage"
```

---

## 📦 Dependabot Management

### Automatic Updates
- Dependabot creates PRs automatically
- Review and merge individually or in batches

### Manual Dependency Updates
```bash
# Update specific package
pip install package==new.version
pip freeze > requirements.txt

# Update all packages
pip list --outdated
pip install --upgrade package1 package2 package3
pip freeze > requirements.txt

# Test updates
python -m pytest tests/ -v

# Commit updates
git add requirements.txt
git commit -m "chore: Update package dependencies

- Updated package1 from old.version to new.version
- Updated package2 from old.version to new.version
- All tests pass with updated dependencies"
```

---

## 🔒 Security Workflow

### Security Updates
```bash
git commit -m "fix: Security update for critical vulnerability

- Updated requests from 2.31.0 to 2.32.5
- Addresses CVE-2024-XXXX
- No breaking changes introduced
- All tests pass"
```

### Security Reporting
- **Email**: `hello.writon@gmail.com`
- **Process**: Private disclosure preferred
- **Response**: Within 48 hours

---

## 📋 Code Review Checklist

### Before Submitting PR
- [ ] All tests pass
- [ ] Code follows style guidelines
- [ ] Documentation updated if needed
- [ ] No sensitive data in commits
- [ ] Commit messages are descriptive
- [ ] Branch is up to date with main

### Review Process
1. **Auto-assignment**: `@writon-xyz` and `@etsibeko-dev` are auto-assigned
2. **Review**: At least one approval required
3. **Merge**: Squash and merge recommended for clean history
4. **Cleanup**: Delete feature branch after merge

---

## 🎯 Common Commands Reference

### Git Essentials
```bash
# Check status
git status

# Add all changes
git add .

# Add specific file
git add filename.py

# Commit with message
git commit -m "your message here"

# Push to remote
git push origin branch-name

# Pull latest changes
git pull origin main

# Create and switch to branch
git checkout -b branch-name

# Switch branches
git checkout branch-name

# Merge branch
git merge branch-name

# Delete branch
git branch -d branch-name
```

### Project-Specific Commands
```bash
# Start development server
uvicorn api:app --reload

# Run CLI
python main.py

# Test API endpoints
curl -X POST "http://localhost:8000/grammar" \
  -H "Content-Type: application/json" \
  -d '{"text": "test text", "case_style": "sentence"}'

# Check deployment status
curl https://www.writon.xyz/health
```

---

## 🚨 Emergency Procedures

### Critical Bug in Production
```bash
# 1. Create hotfix branch immediately
git checkout -b hotfix/critical-bug-fix

# 2. Make minimal fix
git add .
git commit -m "fix: Critical production bug

- Fixed API endpoint returning 500 errors
- Minimal change to restore service
- Full fix will follow in separate PR"

# 3. Push and create PR
git push origin hotfix/critical-bug-fix

# 4. Merge immediately after review
# 5. Deploy and monitor
```

### Rollback Procedure
```bash
# 1. Identify last good commit
git log --oneline

# 2. Revert to last good commit
git checkout main
git revert <bad-commit-hash>

# 3. Push revert
git push origin main

# 4. Monitor deployment
```

---

## 📞 Support Contacts

- **Development Issues**: GitHub Issues
- **Security Issues**: `hello.writon@gmail.com`
- **General Questions**: GitHub Discussions
- **Live Site**: https://www.writon.xyz
- **API Docs**: https://www.writon.xyz/docs

---

**Remember**: Always test locally before pushing to main, and never commit sensitive information like API keys or passwords!
