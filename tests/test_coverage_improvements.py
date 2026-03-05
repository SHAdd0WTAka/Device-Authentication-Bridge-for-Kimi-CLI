"""Additional tests to reach 80% coverage"""

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
    KimiCLINotFoundError,
)


class TestKimiAuthBridgeAdditional:
    """Additional tests for better coverage"""
    
    def test_load_credentials_file_not_exist(self, tmp_path):
        """Test _load_credentials when file doesn't exist"""
        config = KimiConfig(credentials_path=tmp_path / "nonexistent.json")
        bridge = KimiAuthBridge(config=config)
        
        result = bridge._load_credentials()
        assert result is None
    
    def test_load_credentials_invalid_json(self, tmp_path):
        """Test _load_credentials with invalid JSON"""
        creds_file = tmp_path / "credentials.json"
        creds_file.write_text("invalid json {{")
        
        config = KimiConfig(credentials_path=creds_file)
        bridge = KimiAuthBridge(config=config)
        
        with pytest.raises(KimiInvalidCredentialsError):
            bridge._load_credentials()
    
    def test_load_credentials_io_error(self, tmp_path):
        """Test _load_credentials with IO error"""
        creds_file = tmp_path / "credentials.json"
        creds_file.write_text('{"test": "data"}')
        
        config = KimiConfig(credentials_path=creds_file)
        bridge = KimiAuthBridge(config=config)
        
        with patch('builtins.open', side_effect=IOError("Permission denied")):
            with pytest.raises(KimiCredentialsNotFoundError):
                bridge._load_credentials()
    
    def test_is_authenticated_with_exception(self, tmp_path):
        """Test is_authenticated handles exceptions"""
        config = KimiConfig(credentials_path=tmp_path / "nonexistent.json")
        bridge = KimiAuthBridge(config=config)
        
        # Should return False instead of raising
        assert bridge.is_authenticated() is False
    
    def test_is_authenticated_empty_token(self, tmp_path):
        """Test is_authenticated with empty token"""
        creds_file = tmp_path / "credentials.json"
        creds_file.write_text(json.dumps({"access_token": ""}))
        
        config = KimiConfig(credentials_path=creds_file)
        bridge = KimiAuthBridge(config=config)
        
        assert bridge.is_authenticated() is False
    
    def test_get_access_token_with_exception(self, tmp_path):
        """Test get_access_token handles exceptions"""
        config = KimiConfig(credentials_path=tmp_path / "nonexistent.json")
        bridge = KimiAuthBridge(config=config)
        
        # Should return None instead of raising
        assert bridge.get_access_token() is None
    
    def test_get_refresh_token_with_exception(self, tmp_path):
        """Test get_refresh_token handles exceptions"""
        config = KimiConfig(credentials_path=tmp_path / "nonexistent.json")
        bridge = KimiAuthBridge(config=config)
        
        # Should return None instead of raising
        assert bridge.get_refresh_token() is None
    
    def test_get_token_preview_with_exception(self, tmp_path):
        """Test get_token_preview handles exceptions"""
        config = KimiConfig(credentials_path=tmp_path / "nonexistent.json")
        bridge = KimiAuthBridge(config=config)
        
        # Should return None instead of raising
        assert bridge.get_token_preview() is None
    
    def test_get_token_preview_short_token(self, tmp_path):
        """Test get_token_preview with short token"""
        creds_file = tmp_path / "credentials.json"
        creds_file.write_text(json.dumps({"access_token": "short"}))
        
        config = KimiConfig(credentials_path=creds_file)
        bridge = KimiAuthBridge(config=config)
        
        preview = bridge.get_token_preview(length=10)
        assert preview == "short"
    
    def test_get_auth_headers_success(self, tmp_path):
        """Test get_auth_headers returns correct headers"""
        creds_file = tmp_path / "credentials.json"
        creds_file.write_text(json.dumps({"access_token": "test_token_12345"}))
        
        config = KimiConfig(credentials_path=creds_file)
        bridge = KimiAuthBridge(config=config)
        
        headers = bridge.get_auth_headers()
        assert headers == {"Authorization": "Bearer test_token_12345"}
    
    def test_get_auth_headers_not_authenticated(self, tmp_path):
        """Test get_auth_headers raises error when not authenticated"""
        config = KimiConfig(credentials_path=tmp_path / "nonexistent.json")
        bridge = KimiAuthBridge(config=config)
        
        with pytest.raises(KimiNotAuthenticatedError):
            bridge.get_auth_headers()


class TestAsyncKimiAuthBridgeAdditional:
    """Additional async tests for better coverage"""
    
    @pytest.mark.asyncio
    async def test_async_is_authenticated_false(self, tmp_path):
        """Test async is_authenticated returns False"""
        config = KimiConfig(credentials_path=tmp_path / "nonexistent.json")
        bridge = AsyncKimiAuthBridge(config=config)
        
        result = await bridge.is_authenticated()
        assert result is False
    
    @pytest.mark.asyncio
    async def test_async_get_access_token_none(self, tmp_path):
        """Test async get_access_token returns None"""
        config = KimiConfig(credentials_path=tmp_path / "nonexistent.json")
        bridge = AsyncKimiAuthBridge(config=config)
        
        result = await bridge.get_access_token()
        assert result is None
    
    @pytest.mark.asyncio
    async def test_async_get_refresh_token_none(self, tmp_path):
        """Test async get_refresh_token returns None"""
        config = KimiConfig(credentials_path=tmp_path / "nonexistent.json")
        bridge = AsyncKimiAuthBridge(config=config)
        
        result = await bridge.get_refresh_token()
        assert result is None
    
    @pytest.mark.asyncio
    async def test_async_get_token_preview_none(self, tmp_path):
        """Test async get_token_preview returns None"""
        config = KimiConfig(credentials_path=tmp_path / "nonexistent.json")
        bridge = AsyncKimiAuthBridge(config=config)
        
        result = await bridge.get_token_preview()
        assert result is None
    
    @pytest.mark.asyncio
    async def test_async_get_auth_headers_success(self, tmp_path):
        """Test async get_auth_headers returns correct headers"""
        creds_file = tmp_path / "credentials.json"
        creds_file.write_text(json.dumps({"access_token": "async_test_token"}))
        
        config = KimiConfig(credentials_path=creds_file)
        bridge = AsyncKimiAuthBridge(config=config)
        
        headers = await bridge.get_auth_headers()
        assert headers == {"Authorization": "Bearer async_test_token"}


class TestKimiConfig:
    """Tests for KimiConfig"""
    
    def test_config_default_values(self):
        """Test KimiConfig default values"""
        config = KimiConfig()
        assert config.api_base == "https://api.kimi.com/coding/v1"
        assert config.model == "kimi-for-coding"
    
    def test_config_custom_values(self):
        """Test KimiConfig with custom values"""
        config = KimiConfig(
            api_base="https://custom.api.com",
            model="custom-model"
        )
        assert config.api_base == "https://custom.api.com"
        assert config.model == "custom-model"


class TestExceptions:
    """Tests for custom exceptions"""
    
    def test_kimi_auth_error(self):
        """Test KimiAuthError can be raised"""
        from kimi_auth_bridge import KimiAuthError
        
        with pytest.raises(KimiAuthError):
            raise KimiAuthError("Test error")
    
    def test_kimi_token_expired_error(self):
        """Test KimiTokenExpiredError can be raised"""
        from kimi_auth_bridge import KimiTokenExpiredError
        
        with pytest.raises(KimiTokenExpiredError):
            raise KimiTokenExpiredError("Token expired")
    
    def test_kimi_cli_not_found_error(self):
        """Test KimiCLINotFoundError can be raised"""
        from kimi_auth_bridge import KimiCLINotFoundError
        
        with pytest.raises(KimiCLINotFoundError):
            raise KimiCLINotFoundError("CLI not found")
