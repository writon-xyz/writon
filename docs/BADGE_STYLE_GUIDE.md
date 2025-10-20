# Badge Style Guide

This document defines the standard badge styling for Writon documentation to ensure visual consistency across all documentation files.

## Brand Colors

- **Primary Brand Color**: `#0B84FE` (Writon Blue)
- Use for: Main project badges (Live Demo, API Docs)

## Badge Style Standards

### Format
```markdown
![Badge Text](https://img.shields.io/badge/Label-Value-COLOR?style=flat-square&logo=LOGO&logoColor=white)
```

### Required Parameters
- `style=flat-square` - Modern, clean appearance
- `logo=LOGO_NAME` - Use appropriate Simple Icons logo
- `logoColor=white` - Consistent white icons (except JavaScript which uses black)

## Standard Badges

### Header Badges (README.md only)
Centered below logo, use Writon brand color for primary badges:

```markdown
<div align="center">

[![Live Demo](https://img.shields.io/badge/Live_Demo-0B84FE?style=flat-square&logo=googlechrome&logoColor=white)](https://www.writon.xyz)
[![API Docs](https://img.shields.io/badge/API_Docs-00D9FF?style=flat-square&logo=swagger&logoColor=white)](https://www.writon.xyz/docs)
[![License: MIT](https://img.shields.io/badge/License-MIT-00C853?style=flat-square)](https://opensource.org/licenses/MIT)

</div>
```

**Note:** Use Markdown link syntax `[![badge](url)](link)` instead of HTML `<a>` tags to prevent underlines on GitHub.

### Tech Stack Badges

**Backend:**
```markdown
- ![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=flat-square&logo=python&logoColor=white)
- ![FastAPI](https://img.shields.io/badge/FastAPI-0.119+-009688?style=flat-square&logo=fastapi&logoColor=white)
- ![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI-499848?style=flat-square&logo=gunicorn&logoColor=white)
```

**Frontend:**
```markdown
- ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&labelColor=grey&logo=html5&logoColor=white)
- ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&labelColor=grey&logo=css3&logoColor=white)
- ![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=flat-square&logo=javascript&logoColor=white)
```

**AI Providers:**
```markdown
- ![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-412991?style=flat-square&logo=openai&logoColor=white)
- ![Google](https://img.shields.io/badge/Google-Gemini-4285F4?style=flat-square&logo=google&logoColor=white)
- ![Anthropic](https://img.shields.io/badge/Anthropic-Claude-191919?style=flat-square&logo=anthropic&logoColor=white)
- ![Groq](https://img.shields.io/badge/Groq-Llama--3-F55036?style=flat-square&logo=lightning&logoColor=white)
```

**Deployment:**
```markdown
- ![Render](https://img.shields.io/badge/Render-Deployed-46E3B7?style=flat-square&logo=render&logoColor=white)
- ![GitHub](https://img.shields.io/badge/GitHub-CI%2FCD-181717?style=flat-square&logo=github&logoColor=white)
```

## Color Reference

| Technology | Color Code | Logo |
|------------|-----------|------|
| Writon (Primary) | `#0B84FE` | googlechrome |
| API Docs | `#00D9FF` | swagger |
| Python | `#3776AB` | python |
| FastAPI | `#009688` | fastapi |
| Uvicorn | `#499848` | gunicorn |
| HTML5 | `#E34F26` (grey label) | html5 |
| CSS3 | `#1572B6` (grey label) | css3 |
| JavaScript | `#F7DF1E` | javascript (white logo) |
| OpenAI | `#412991` | openai |
| Google | `#4285F4` | google |
| Anthropic | `#191919` | anthropic |
| Groq | `#F55036` | lightning |
| Render | `#46E3B7` | render |
| GitHub | `#181717` | github |
| License (MIT) | `#00C853` | - |
| Python Version | `blue` | python |

## Badge Placement Guidelines

### README.md
1. **Header Section**: Logo + Primary badges (centered)
2. **Tech Stack Section**: Technology badges (inline with bullet points)
3. **No badges in**: Feature lists, installation instructions, usage examples

### CONTRIBUTING.md
- No badges needed (keep clean and focused on contribution guidelines)

### CHANGELOG.md
- No badges needed (version history only)

### DEVELOPMENT_GUIDE.md
- No badges needed (technical documentation)

### QUICK_REFERENCE.md
- No badges needed (command reference)

## Rules

1. ✅ **Always use `flat-square` style**
2. ✅ **Always include appropriate logo icons**
3. ✅ **Use Writon brand color (`#0B84FE`) for Live Demo badge**
4. ✅ **Use cyan (`#00D9FF`) for API Docs badge** - Differentiates from Live Demo
5. ✅ **Use official brand colors for technology badges**
6. ✅ **Maintain white logo color for all badges**
7. ✅ **Use Markdown link syntax for clickable badges** - Prevents underlines
8. ❌ **Never use emojis in badges**
9. ❌ **Never use `for-the-badge` style** (outdated)
10. ❌ **Never use HTML `<a>` tags for badges** (causes underlines)
11. ❌ **Don't add badges to every document** (only README.md)

## Format Guidelines

### For Clickable Badges (Header Section)
Use Markdown link syntax to prevent underlines:
```markdown
[![Badge Text](badge-url)](link-url)
```

### For Non-Clickable Badges (Tech Stack Section)
Use standard Markdown image syntax:
```markdown
![Badge Text](badge-url)
```

## Updating Badges

When updating version numbers or adding new technologies:

1. Check [Simple Icons](https://simpleicons.org/) for official logos
2. Use official brand colors when available
3. Follow the format above exactly
4. Update this guide if adding new badge types
5. Ensure consistency across all occurrences

---

**Last Updated**: 2025-10-20
**Maintainer**: @writon-xyz, @etsibeko-dev
