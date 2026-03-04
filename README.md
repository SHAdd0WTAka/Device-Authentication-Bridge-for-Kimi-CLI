# 🌙 Kimi Device Authentication Bridge

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A reusable Python module for integrating **Kimi Code CLI** OAuth authentication into any application. No more hardcoded API keys - just seamless device authentication!

## ✨ Features

- 🔐 **OAuth Token Retrieval** - Reads tokens from Kimi CLI's secure storage
- 🔄 **Auto-Refresh** - Handles token expiration automatically
- 🚀 **Zero Config** - Works out of the box with existing Kimi CLI installations
- 🛡️ **Secure** - Never stores credentials, only reads from Kimi's secure storage
- 🔌 **Framework Agnostic** - Use with Flask, FastAPI, Django, or any Python app
- 📦 **Easy Integration** - Simple API, minimal setup required

## 🎯 Use Cases

This bridge solves 2 major problems:

1. **🔑 No Hardcoded API Keys** - Stop committing secrets to git
2. **👥 User-Friendly** - End users just run `kimi login`, no manual key management

Perfect for:
- AI-powered developer tools
- Coding assistants
- CLI applications
- Web applications needing LLM access
- Any tool that wants to leverage Kimi's API without exposing keys

## 📦 Installation

```bash
pip install kimi-auth-bridge
```

Or install from source:

```bash
git clone https://github.com/yourusername/kimi-device-auth-bridge.git
cd kimi-device-auth-bridge
pip install -e .
```

## 🚀 Quick Start

### Basic Usage

```python
from kimi_auth_bridge import KimiAuthBridge

# Initialize the bridge
bridge = KimiAuthBridge()

# Check if user is authenticated
if bridge.is_authenticated():
    # Get the access token
    token = bridge.get_access_token()
    print(f"Token: {token[:20]}...")
    
    # Use with any HTTP client
    import requests
    response = requests.post(
        "https://api.kimi.com/coding/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {token}",
            "User-Agent": bridge.get_user_agent()
        },
        json={
            "model": "kimi-for-coding",
            "messages": [{"role": "user", "content": "Hello!"}]
        }
    )
else:
    print("Please run 'kimi login' first")
```

### Async Support

```python
import asyncio
from kimi_auth_bridge import AsyncKimiAuthBridge

async def main():
    bridge = AsyncKimiAuthBridge()
    
    if await bridge.is_authenticated():
        token = await bridge.get_access_token()
        # Use token with async HTTP client...
        print(f"Got token: {token[:20]}...")

asyncio.run(main())
```

### Web Framework Integration

#### Flask Example

```python
from flask import Flask, jsonify
from kimi_auth_bridge import KimiAuthBridge

app = Flask(__name__)
bridge = KimiAuthBridge()

@app.route('/api/kimi/status')
def kimi_status():
    return jsonify({
        'authenticated': bridge.is_authenticated(),
        'api_base': bridge.get_api_base(),
        'model': bridge.get_default_model()
    })

@app.route('/api/kimi/token')
def kimi_token():
    if not bridge.is_authenticated():
        return jsonify({'error': 'Not authenticated'}), 401
    
    return jsonify({
        'token_preview': bridge.get_token_preview(),
        'api_base': bridge.get_api_base()
    })

if __name__ == '__main__':
    app.run(debug=True)
```

#### FastAPI Example

```python
from fastapi import FastAPI, HTTPException
from kimi_auth_bridge import KimiAuthBridge

app = FastAPI()
bridge = KimiAuthBridge()

@app.get('/api/kimi/status')
async def kimi_status():
    return {
        'authenticated': bridge.is_authenticated(),
        'api_base': bridge.get_api_base(),
        'model': bridge.get_default_model()
    }

@app.get('/api/kimi/token')
async def kimi_token():
    if not bridge.is_authenticated():
        raise HTTPException(status_code=401, detail='Not authenticated')
    
    return {
        'token': bridge.get_access_token(),
        'api_base': bridge.get_api_base()
    }
```

## 📚 API Reference

### KimiAuthBridge

Main class for synchronous authentication handling.

#### Methods

| Method | Description | Returns |
|--------|-------------|---------|
| `is_authenticated()` | Check if user has valid credentials | `bool` |
| `get_access_token()` | Get the current access token | `str \| None` |
| `get_token_preview()` | Get truncated token for display | `str \| None` |
| `get_api_base()` | Get Kimi API base URL | `str` |
| `get_default_model()` | Get default model name | `str` |
| `get_user_agent()` | Get required User-Agent header | `str` |
| `get_auth_headers()` | Get complete headers dict | `dict` |

### AsyncKimiAuthBridge

Async version for non-blocking operations.

#### Methods

Same as `KimiAuthBridge`, but all methods are async.

## 🔧 Advanced Configuration

```python
from kimi_auth_bridge import KimiAuthBridge, KimiConfig

# Custom configuration
config = KimiConfig(
    credentials_path="/custom/path/credentials.json",
    api_base="https://custom-api.kimi.com/v1",
    model="kimi-custom-model"
)

bridge = KimiAuthBridge(config=config)
```

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=kimi_auth_bridge tests/
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments & Credits

**Special thanks to the incredible team at [Moonshot AI](https://www.moonshot.cn/)** for developing this brilliant authentication system!

### Why Moonshot's Approach is Genius 🧠

The Kimi CLI authentication system represents a **security breakthrough** in AI API access:

- 🔑 **Dynamic Token Generation** - Fresh tokens on every login, no static keys
- 🛡️ **Device-Bound Security** - Tokens only work on authenticated devices  
- 🌐 **Browser-Verified** - Authentication happens through kimi.com website
- 🔒 **No Hardcoded Secrets** - Zero risk of API keys in git repositories
- ✌️ **Multi-Factor by Design** - Combines device + browser + OAuth
- 🔄 **Automatic Rotation** - Seamless token refresh without user intervention

This is how **all** AI API authentication should work! Hats off to the Moonshot team for prioritizing security AND user experience.

- Built for [Kimi Code CLI](https://www.moonshot.cn/)
- Thanks to the Moonshot AI team for the excellent API and revolutionary auth system

## 📞 Support

- 📧 Email: your.email@example.com
- 💬 Issues: [GitHub Issues](https://github.com/yourusername/kimi-device-auth-bridge/issues)
- 📖 Docs: [Full Documentation](https://github.com/yourusername/kimi-device-auth-bridge/tree/main/docs)

---

**Made with ❤️ for the AI developer community**
