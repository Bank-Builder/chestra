import pytest
from unittest.mock import Mock, patch
from chestra.plugins.http import HttpPlugin
import requests


def test_http_plugin_executes():
    """Test that the HTTP plugin executes successfully."""
    plugin = HttpPlugin()
    
    with patch('requests.request') as mock_request:
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "Hello, World!"
        mock_response.url = "https://example.com"
        mock_response.headers = {"Content-Type": "text/plain"}
        mock_response.json.return_value = {"message": "Hello"}
        mock_response.raise_for_status.return_value = None
        
        mock_request.return_value = mock_response
        
        result = plugin.execute({}, {"url": "https://example.com"})
        
        assert "status_code" in result
        assert "data" in result
        assert "headers" in result
        assert "json_data" in result
        assert "url" in result
        assert result["status_code"] == "200"
        assert result["data"] == "Hello, World!"


def test_http_plugin_with_params():
    """Test that the HTTP plugin handles parameters correctly."""
    plugin = HttpPlugin()
    
    with patch('requests.request') as mock_request:
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.text = "Created"
        mock_response.url = "https://api.example.com/users"
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {"id": 123}
        mock_response.raise_for_status.return_value = None
        
        mock_request.return_value = mock_response
        
        params = {
            "url": "https://api.example.com/users",
            "method": "POST",
            "headers": {"Authorization": "Bearer token123"},
            "json": {"name": "John Doe"}
        }
        
        result = plugin.execute({}, params)
        
        assert result["status_code"] == "201"
        assert "Bearer token123" in mock_request.call_args[1]["headers"]["Authorization"]


def test_http_plugin_missing_url():
    """Test that the HTTP plugin requires a URL parameter."""
    plugin = HttpPlugin()
    
    with pytest.raises(ValueError, match="URL parameter is required"):
        plugin.execute({}, {})


def test_http_plugin_request_failure():
    """Test that the HTTP plugin handles request failures."""
    plugin = HttpPlugin()
    
    with patch('requests.request') as mock_request:
        mock_request.side_effect = requests.exceptions.RequestException("Connection failed")
        
        with pytest.raises(RuntimeError, match="HTTP request failed"):
            plugin.execute({}, {"url": "https://example.com"})


def test_http_plugin_with_custom_options():
    """Test that the HTTP plugin handles custom options."""
    plugin = HttpPlugin()
    
    with patch('requests.request') as mock_request:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "OK"
        mock_response.url = "https://example.com"
        mock_response.headers = {}
        mock_response.json.side_effect = ValueError("Not JSON")
        mock_response.raise_for_status.return_value = None
        
        mock_request.return_value = mock_response
        
        params = {
            "url": "https://example.com",
            "timeout": 10,
            "verify": False,
            "allow_redirects": False
        }
        
        result = plugin.execute({}, params)
        
        # Check that custom options were passed to requests
        call_kwargs = mock_request.call_args[1]
        assert call_kwargs["timeout"] == 10
        assert call_kwargs["verify"] is False
        assert call_kwargs["allow_redirects"] is False
        assert result["json_data"] == ""


def test_http_plugin_with_permissions():
    """Test that the HTTP plugin handles permissions correctly."""
    plugin = HttpPlugin()
    
    # HTTP plugin doesn't require auth by default
    assert plugin.REQUIRES_AUTH is False
    assert plugin.REQUIRED_PERMISSIONS == []
    
    # Should work without permissions
    with patch('requests.request') as mock_request:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "OK"
        mock_response.url = "https://example.com"
        mock_response.headers = {}
        mock_response.json.return_value = {}
        mock_response.raise_for_status.return_value = None
        
        mock_request.return_value = mock_response
        
        result = plugin.execute({}, {"url": "https://example.com"})
        assert result is not None 