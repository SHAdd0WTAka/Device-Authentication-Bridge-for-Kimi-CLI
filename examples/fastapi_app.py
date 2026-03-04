#!/usr/bin/env python3
"""
FastAPI web application example with Kimi Authentication Bridge
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from kimi_auth_bridge import (
    KimiAuthBridge,
    AsyncKimiAuthBridge,
    KimiNotAuthenticatedError
)

app = FastAPI(
    title="Kimi Auth Bridge API",
    description="Device Authentication Bridge for Kimi CLI",
    version="1.0.0"
)

# Initialize bridges
sync_bridge = KimiAuthBridge()
async_bridge = AsyncKimiAuthBridge()


class AuthStatus(BaseModel):
    authenticated: bool
    api_base: str
    model: str
    token_preview: str | None


class TokenResponse(BaseModel):
    token: str
    preview: str


class HeadersResponse(BaseModel):
    headers: dict


@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with HTML documentation"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Kimi Auth Bridge API</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            h1 { color: #333; }
            .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
            code { background: #e0e0e0; padding: 2px 6px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <h1>🌙 Kimi Device Auth Bridge API</h1>
        <p>FastAPI application demonstrating Kimi Auth Bridge integration.</p>
        
        <h2>API Endpoints</h2>
        
        <div class="endpoint">
            <h3>GET /api/status</h3>
            <p>Check authentication status</p>
        </div>
        
        <div class="endpoint">
            <h3>GET /api/token</h3>
            <p>Get access token (requires authentication)</p>
        </div>
        
        <div class="endpoint">
            <h3>GET /api/headers</h3>
            <p>Get complete auth headers</p>
        </div>
        
        <div class="endpoint">
            <h3>POST /api/login</h3>
            <p>Trigger Kimi CLI login</p>
        </div>
        
        <div class="endpoint">
            <h3>POST /api/logout</h3>
            <p>Trigger Kimi CLI logout</p>
        </div>
        
        <p style="margin-top: 30px;">
            <a href="/docs">📚 Interactive API Docs (Swagger UI)</a>
        </p>
    </body>
    </html>
    """


@app.get("/api/status", response_model=AuthStatus)
async def get_status():
    """Get current authentication status"""
    return AuthStatus(
        authenticated=await async_bridge.is_authenticated(),
        api_base=async_bridge.get_api_base(),
        model=async_bridge.get_default_model(),
        token_preview=await async_bridge.get_token_preview()
    )


@app.get("/api/token", response_model=TokenResponse)
async def get_token():
    """Get access token (requires authentication)"""
    try:
        token = await async_bridge.get_access_token()
        if not token:
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        return TokenResponse(
            token=token,
            preview=await async_bridge.get_token_preview()
        )
    except KimiNotAuthenticatedError:
        raise HTTPException(status_code=401, detail="Not authenticated")


@app.get("/api/headers", response_model=HeadersResponse)
async def get_headers():
    """Get authentication headers"""
    try:
        headers = await async_bridge.get_auth_headers()
        return HeadersResponse(headers=headers)
    except KimiNotAuthenticatedError:
        raise HTTPException(status_code=401, detail="Not authenticated")


@app.post("/api/login")
async def login():
    """Trigger Kimi CLI login flow"""
    try:
        success = await async_bridge.login()
        if success:
            return {"success": True, "message": "Login successful"}
        else:
            raise HTTPException(status_code=400, detail="Login failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/logout")
async def logout():
    """Trigger Kimi CLI logout"""
    try:
        success = await async_bridge.logout()
        return {"success": success, "message": "Logout completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting FastAPI app...")
    print("📍 Open http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
