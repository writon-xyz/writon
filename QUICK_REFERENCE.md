# 🚀 Writon Quick Reference Card

**Copy-paste commands for daily development**

## 🔧 Setup Commands
```bash
# Clone and setup
git clone https://github.com/sbklabs/writon.git
cd writon
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## 📝 Daily Development
```bash
# Start server
uvicorn api:app --reload
# Or: python -m uvicorn api:app --reload

# Run tests
python -m pytest tests/ -v
# Or: python3 -m pytest tests/ -v

# Run CLI
python main.py
# Or: python3 main.py
```

## 🔄 Git Workflow
```bash
# Create feature branch
git checkout -b feature/your-feature-name
git push -u origin feature/your-feature-name

# Make changes and commit
git add .
git commit -m "feat: Add your feature description"
git push origin feature/your-feature-name

# Create PR on GitHub, merge after review
```

## 📋 Commit Message Templates

### Feature
```bash
git commit -m "feat: Add new AI provider integration

- Added support for OpenAI GPT-4 Turbo
- Updated provider selection UI
- Added corresponding tests

Closes #123"
```

### Bug Fix
```bash
git commit -m "fix: Resolve frontend JavaScript errors

- Added null checks for DOM elements
- Fixed mobile menu navigation
- Improved error handling

Fixes #456"
```

### Documentation
```bash
git commit -m "docs: Update README with latest changes

- Added new feature descriptions
- Updated API examples
- Fixed broken links"
```

### Dependencies
```bash
git commit -m "chore: Update dependencies to latest versions

- Updated FastAPI from 0.118.0 to 0.119.0
- Updated Uvicorn from 0.37.0 to 0.38.0
- Updated Pydantic from 2.11.10 to 2.12.3
- All tests pass with updated dependencies"
```

### Security
```bash
git commit -m "fix: Security update for critical vulnerability

- Updated requests from 2.31.0 to 2.32.5
- Addresses CVE-2024-XXXX
- No breaking changes introduced"
```

## 👥 Account Switching
```bash
# Check current user
git config user.name
git config user.email

# Switch to organization (@sbklabs)
git config user.name "sbklabs"
git config user.email "hello.writon@gmail.com"

# Switch to personal (@etsibeko-dev)
git config user.name "etsibeko-dev"
git config user.email "your-personal-email@gmail.com"
```

## 🚀 Deployment
```bash
# Test before deploy
python -m pytest tests/ -v

# Deploy to production
git push origin main
# Check: https://www.writon.xyz
```

## 🧪 Testing Commands
```bash
# All tests
python -m pytest tests/ -v

# Specific test file
python -m pytest tests/test_api_pytest.py -v

# With coverage
python -m pytest tests/ --cov=core --cov=api
```

## 🚨 Emergency Fix
```bash
# Critical bug fix
git checkout -b hotfix/critical-fix
git add .
git commit -m "fix: Critical production bug

- Fixed API endpoint returning 500 errors
- Minimal change to restore service"
git push origin hotfix/critical-fix
# Create PR and merge immediately
```

## 📞 Quick Info
- **Repo**: `https://github.com/sbklabs/writon`
- **Live**: `https://www.writon.xyz`
- **API Docs**: `https://www.writon.xyz/docs`
- **Email**: `hello.writon@gmail.com`
- **Accounts**: `@sbklabs` (org), `@etsibeko-dev` (personal)

## 🎯 Branch Protection Rules
- ✅ Main branch protected
- ✅ Must use PRs (except admin bypass for @sbklabs)
- ✅ Auto-reviewers: @sbklabs, @etsibeko-dev
- ✅ All tests must pass

**Remember**: Always test locally before pushing!
