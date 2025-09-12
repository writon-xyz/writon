# Security Policy

## Supported Versions

We actively support the following versions of Writon with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1   | :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please report it responsibly.

### How to Report

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please email us directly at: **security@writon.xyz**

### What to Include

In your report, please include:

- **Description** of the vulnerability
- **Steps to reproduce** the issue
- **Potential impact** assessment
- **Suggested fixes** (if you have any)
- **Your contact information** for follow-up

### What to Expect

- **Acknowledgment** within 48 hours
- **Initial assessment** within 7 days
- **Regular updates** on our progress
- **Public disclosure** after the issue is fixed (with your permission)

### Responsible Disclosure

We follow responsible disclosure practices:

1. **Report privately** to security@writon.xyz
2. **Allow reasonable time** for us to fix the issue
3. **Coordinate public disclosure** after the fix is deployed
4. **Credit researchers** who report valid vulnerabilities

## Security Measures

### Data Protection
- **No Data Storage**: Writon does not store your text or API keys
- **Privacy First**: All processing happens in real-time
- **User Keys**: Your API keys remain on your device/browser
- **No Logging**: Text content is not logged or stored

### Technical Security
- **HTTPS Only**: All communication is encrypted
- **Rate Limiting**: Prevents abuse and DoS attacks
- **Input Validation**: Robust data validation and sanitization
- **Security Headers**: Protection against common web vulnerabilities
- **Dependency Updates**: Regular updates via Dependabot

### Infrastructure Security
- **Secure Hosting**: Deployed on Render.com with security best practices
- **SSL Certificates**: Valid SSL certificates for all domains
- **Environment Isolation**: Separate environments for development and production
- **Access Controls**: Limited access to production systems

## Security Features

### API Security
- **Authentication**: BYOK model ensures user control
- **Rate Limiting**: 30 requests per minute per IP
- **Request Size Limits**: Prevents large payload attacks
- **CORS Protection**: Proper cross-origin resource sharing
- **Input Sanitization**: All inputs are validated and sanitized

### Web Security
- **Content Security Policy**: Prevents XSS attacks
- **X-Frame-Options**: Prevents clickjacking
- **X-Content-Type-Options**: Prevents MIME sniffing
- **Referrer Policy**: Controls referrer information
- **Strict Transport Security**: Enforces HTTPS

## Best Practices for Users

### API Key Security
- **Keep Keys Private**: Never share your API keys
- **Use Environment Variables**: Store keys securely
- **Rotate Keys Regularly**: Change keys periodically
- **Monitor Usage**: Check API usage for anomalies

### General Security
- **Use HTTPS**: Always access Writon via HTTPS
- **Keep Software Updated**: Use the latest versions
- **Be Cautious with Text**: Don't process sensitive information
- **Report Suspicious Activity**: Contact us immediately

## Security Contact

- **Email**: security@writon.xyz
- **Response Time**: Within 48 hours
- **PGP Key**: Available upon request

## Security Updates

We will announce security updates through:
- **GitHub Releases**: Tagged security releases
- **Email Notifications**: For critical vulnerabilities
- **Documentation Updates**: Security-related changes

## Bug Bounty

We appreciate security researchers and may offer recognition for responsible vulnerability reports. Please contact us at security@writon.xyz for more information.

---

**Thank you for helping keep Writon secure!** 🔒
