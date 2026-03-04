"""
Tests for Kimi Authentication Bridge
"""

import json
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, mock_open

from kimi_auth_bridge import (
    KimiAuthBridge,
    AsyncKimiAuthBridge,
    KimiConfig,
    KimiNotAuthenticatedError,
    KimiCredentialsNotFoundError,
    KimiInvalidCredentialsError,
)


class TestKimiAuthBridge:
    """Test cases for KimiAuthBridge"""
    
    @pytest.fixture
    def mock_credentials(self):
        """Sample credentials data"""
        return {
            "access_token": "eyJhbGciOiJFUzI1NiIs.test.token",
            "refresh_token": "eyJhbGciOiJFUzI1NiIs.test.refresh",
            "expires_at": 1772659008.650313,
        }
    
    @pytest.fixture
    def bridge(self, tmp_path):
        """Create a bridge with temporary credentials path"""
        config = KimiConfig(credentials_path=tmp_path / "credentials.json")
        return KimiAuthBridge(config=config)
    
    def test_init_default_config(self):
        """Test bridge initialization with default config"""
        bridge = KimiAuthBridge()
        assert bridge.config is not None
        assert bridge.config.api_base == "https://api.kimi.com/coding/v1"
        assert bridge.config.model == "kimi-for-coding"
    
    def test_init_custom_config(self):
        """Test bridge initialization with custom config"""
        config = KimiConfig(
            api_base="https://custom.api.com",
            model="custom-model"
        )
        bridge = KimiAuthBridge(config=config)
        assert bridge.config.api_base == "https://custom.api.com"
        assert bridge.config.model == "custom-model"
    
    def test_is_authenticated_true(self, bridge, mock_credentials):
        """Test is_authenticated returns True when credentials exist"""
        with patch.object(bridge, '_load_credentials', return_value=mock_credentials):
            assert bridge.is_authenticated() is True
    
    def test_is_authenticated_false_no_file(self, bridge):
        """Test is_authenticated returns False when no credentials file"""
        with patch.object(bridge, '_load_credentials', return_value=None):
            assert bridge.is_authenticated() is False
    
    def test_is_authenticated_false_empty_token(self, bridge):
        """Test is_authenticated returns False when token is empty"""
        with patch.object(bridge, '_load_credentials', return_value={"access_token": ""}):
            assert bridge.is_authenticated() is False
    
    def test_get_access_token_success(self, bridge, mock_credentials):
        """Test get_access_token returns token when authenticated"""
        with patch.object(bridge, '_load_credentials', return_value=mock_credentials):
            token = bridge.get_access_token()
            assert token == mock_credentials["access_token"]
    
    def test_get_access_token_none(self, bridge):
        """Test get_access_token returns None when not authenticated"""
        with patch.object(bridge, '_load_credentials', return_value=None):
            token = bridge.get_access_token()
            assert token is None
    
    def test_get_token_preview(self, bridge, mock_credentials):
        """Test get_token_preview returns truncated token"""
        with patch.object(bridge, '_load_credentials', return_value=mock_credentials):
            preview = bridge.get_token_preview(length=10)
            assert preview == "eyJhbGciOi..."
    
    def test_get_token_preview_none(self, bridge):
        """Test get_token_preview returns None when no token"""
        with patch.object(bridge, '_load_credentials', return_value=None):
            preview = bridge.get_token_preview()
            assert preview is None
    
    def test_get_auth_headers_success(self, bridge, mock_credentials):
        """Test get_auth_headers returns complete headers"""
        with patch.object(bridge, '_load_credentials', return_value=mock_credentials):
            headers = bridge.get_auth_headers()
            assert "Authorization" in headers
            assert headers["Authorization"] == f"Bearer {mock_credentials['access_token']}"
            assert "User-Agent" in headers
            assert "Content-Type" in headers
    
    def test_get_auth_headers_not_authenticated(self, bridge):
        """Test get_auth_headers raises error when not authenticated"""
        with patch.object(bridge, '_load_credentials', return_value=None):
            with pytest.raises(KimiNotAuthenticatedError):
                bridge.get_auth_headers()
    
    def test_get_api_base(self, bridge):
        """Test get_api_base returns correct URL"""
        assert bridge.get_api_base() == "https://api.kimi.com/coding/v1"
    
    def test_get_default_model(self, bridge):
        """Test get_default_model returns model name"""
        assert bridge.get_default_model() == "kimi-for-coding"
    
    def test_get_user_agent(self, bridge):
        """Test get_user_agent returns user agent string"""
        assert bridge.get_user_agent() == "KimiCLI/1.0.0"
    
    def test_load_credentials_success(self, bridge, mock_credentials, tmp_path):
        """Test _load_credentials loads JSON file correctly"""
        creds_file = tmp_path / "credentials.json"
        creds_file.write_text(json.dumps(mock_credentials))
        
        bridge.config.credentials_path = creds_file
        result = bridge._load_credentials()
        
        assert result == mock_credentials
    
    def test_load_credentials_file_not_found(self, bridge):
        """Test _load_credentials returns None when file not found"""
        bridge.config.credentials_path = Path("/nonexistent/path/credentials.json")
        result = bridge._load_credentials()
        assert result is None
    
    def test_load_credentials_invalid_json(self, bridge, tmp_path):
        """Test _load_credentials raises error on invalid JSON"""
        creds_file = tmp_path / "credentials.json"
        creds_file.write_text("invalid json")
        
        bridge.config.credentials_path = creds_file
        
        with pytest.raises(KimiInvalidCredentialsError):
            bridge._load_credentials()
    
    def test_require_auth_decorator_success(self, bridge, mock_credentials):
        """Test require_auth decorator allows function when authenticated"""
        with patch.object(bridge, '_load_credentials', return_value=mock_credentials):
            
            @bridge.require_auth
            def protected_function():
                return "success"
            
            assert protected_function() == "success"
    
    def test_require_auth_decorator_failure(self, bridge):
        """Test require_auth decorator raises error when not authenticated"""
        with patch.object(bridge, '_load_credentials', return_value=None):
            
            @bridge.require_auth
            def protected_function():
                return "success"
            
            with pytest.raises(KimiNotAuthenticatedError):
                protected_function()


class TestAsyncKimiAuthBridge:
    """Test cases for AsyncKimiAuthBridge"""
    
    @pytest.fixture
    def async_bridge(self, tmp_path):
        """Create an async bridge with temporary credentials path"""
        config = KimiConfig(credentials_path=tmp_path / "credentials.json")
        return AsyncKimiAuthBridge(config=config)
    
    @pytest.mark.asyncio
    async def test_async_is_authenticated(self, async_bridge):
        """Test async is_authenticated method"""
        with patch.object(async_bridge, '_load_credentials', return_value=None):
            result = await async_bridge.is_authenticated()
            assert result is False
    
    @pytest.mark.asyncio
    async def test_async_get_access_token(self, async_bridge):
        """Test async get_access_token method"""
        with patch.object(async_bridge, '_load_credentials', return_value=None):
            result = await async_bridge.get_access_token()
            assert result is None
    
    @pytest.mark.asyncio
    async def test_async_get_auth_headers(self, async_bridge):
        """Test async get_auth_headers raises error when not authenticated"""
        with patch.object(async_bridge, '_load_credentials', return_value=None):
            with pytest.raises(KimiNotAuthenticatedError):
                await async_bridge.get_auth_headers()


class TestKimiConfig:
    """Test cases for KimiConfig"""
    
    def test_default_config(self):
        """Test default configuration values"""
        config = KimiConfig()
        assert config.api_base == "https://api.kimi.com/coding/v1"
        assert config.model == "kimi-for-coding"
        assert config.user_agent == "KimiCLI/1.0.0"
        assert config.credentials_path is not None
    
    def test_custom_config(self):
        """Test custom configuration values"""
        config = KimiConfig(
            api_base="https://custom.api.com",
            model="custom-model",
            user_agent="CustomAgent/1.0"
        )
        assert config.api_base == "https://custom.api.com"
        assert config.model == "custom-model"
        assert config.user_agent == "CustomAgent/1.0"
    
    def test_chat_completions_url(self):
        """Test chat_completions_url property"""
        config = KimiConfig()
        assert config.chat_completions_url == "https://api.kimi.com/coding/v1/chat/completions"
    
    def test_models_url(self):
        """Test models_url property"""
        config = KimiConfig()
        assert config.models_url == "https://api.kimi.com/coding/v1/models"
