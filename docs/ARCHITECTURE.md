# Architecture

## Overview

The Kimi Device Authentication Bridge is a lightweight Python module that acts as a secure intermediary between your application and the Kimi CLI's OAuth authentication system.

```
┌─────────────────┐     ┌──────────────────────┐     ┌─────────────────┐
│   Your App      │────▶│  Kimi Auth Bridge    │────▶│   Kimi CLI      │
│                 │     │                      │     │                 │
│ - Web App       │     │ - Reads tokens       │     │ - OAuth Flow    │
│ - CLI Tool      │     │ - Provides headers   │     │ - Secure Store  │
│ - API Service   │     │ - Handles errors     │     │ - Auto-refresh  │
└─────────────────┘     └──────────────────────┘     └─────────────────┘
         │                       │                            │
         │                       │                            │
         ▼                       ▼                            ▼
   Uses token              ~/.kimi/credentials/         Kimi API
   for API calls           kimi-code.json
```

## Components

### 1. Bridge (`bridge.py`)

The core component providing synchronous and asynchronous interfaces.

#### KimiAuthBridge
- **Purpose**: Main synchronous interface
- **Key Methods**:
  - `is_authenticated()`: Check auth status
  - `get_access_token()`: Retrieve OAuth token
  - `get_auth_headers()`: Get complete HTTP headers
  - `require_auth()`: Decorator for protected functions

#### AsyncKimiAuthBridge
- **Purpose**: Asynchronous interface for non-blocking operations
- **Additional Features**:
  - `login()`: Trigger CLI login flow
  - `logout()`: Trigger CLI logout

### 2. Configuration (`config.py`)

Centralized configuration management using dataclasses.

```python
@dataclass
class KimiConfig:
    credentials_path: Optional[Path]  # Token storage location
    api_base: str                     # API endpoint
    model: str                        # Default model
    user_agent: str                   # Required header
```

### 3. Exceptions (`exceptions.py`)

Hierarchical exception structure for precise error handling:

```
KimiAuthError (base)
├── KimiNotAuthenticatedError
├── KimiTokenExpiredError
├── KimiCLINotFoundError
├── KimiCredentialsNotFoundError
└── KimiInvalidCredentialsError
```

## Security Model

### Principles

1. **Read-Only Access**: The bridge never writes credentials, only reads from Kimi CLI's secure storage
2. **No Key Storage**: No API keys are stored in memory longer than necessary
3. **Token Isolation**: Each application instance accesses tokens independently

### Data Flow

```
1. User runs 'kimi login'
   ↓
2. Kimi CLI stores tokens in ~/.kimi/credentials/ (permission 600)
   ↓
3. Bridge reads token on-demand
   ↓
4. Token used in API request headers
   ↓
5. Token discarded from memory
```

## Integration Patterns

### Pattern 1: Direct Usage

```python
from kimi_auth_bridge import KimiAuthBridge

bridge = KimiAuthBridge()
if bridge.is_authenticated():
    headers = bridge.get_auth_headers()
    # Use headers directly
```

### Pattern 2: Dependency Injection

```python
from fastapi import Depends

async def get_kimi_auth() -> KimiAuthBridge:
    return KimiAuthBridge()

@app.get("/api/data")
async def get_data(bridge: KimiAuthBridge = Depends(get_kimi_auth)):
    # Use bridge
```

### Pattern 3: Middleware

```python
class KimiAuthMiddleware:
    def __init__(self, app):
        self.app = app
        self.bridge = KimiAuthBridge()
    
    def __call__(self, environ, start_response):
        environ['kimi_auth'] = self.bridge
        return self.app(environ, start_response)
```

## Error Handling Strategy

### Layered Approach

```
Layer 1: File System
    └─> FileNotFound → KimiCredentialsNotFoundError

Layer 2: JSON Parsing
    └─> JSONDecodeError → KimiInvalidCredentialsError

Layer 3: Token Validation
    └─> Missing/Empty Token → KimiNotAuthenticatedError

Layer 4: Application
    └─> Custom handling based on exception type
```

### Example

```python
try:
    headers = bridge.get_auth_headers()
except KimiNotAuthenticatedError:
    redirect_to_login()
except KimiCLINotFoundError:
    prompt_install_kimi()
except KimiAuthError as e:
    log_error(e)
```

## Performance Considerations

### Token Caching

The bridge does NOT cache tokens in memory. Each call reads from disk:
- **Pros**: Always fresh tokens, handles refresh automatically
- **Cons**: Slight I/O overhead

### Async Support

For high-throughput applications:
- Use `AsyncKimiAuthBridge`
- Tokens are read in executor to not block event loop
- Recommended for web servers

### Best Practices

1. **Don't cache tokens yourself** - Let Kimi CLI handle it
2. **Check auth status once per request** - Not in tight loops
3. **Use context managers** - For automatic resource cleanup

## Testing Strategy

### Unit Tests
- Mock file system operations
- Test all exception paths
- Validate header formats

### Integration Tests
- Requires actual Kimi CLI installation
- Tests real token retrieval
- Validates API connectivity

## Future Enhancements

### Planned
- [ ] Token refresh scheduling
- [ ] Multiple credential profiles
- [ ] Token encryption at rest

### Under Consideration
- [ ] Caching layer with TTL
- [ ] Webhook for token events
- [ ] Token usage analytics
