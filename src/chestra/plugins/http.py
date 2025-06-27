from typing import Any, Dict
import requests
from chestra.log import get_logger
from chestra.orchestrator import TaskPlugin

logger = get_logger(__name__)


class HttpPlugin(TaskPlugin):
    """
    HTTP plugin.

    This plugin makes HTTP requests with configurable methods, headers, and options.

    Parameters:
        url: The URL to make the request to
        method: HTTP method (GET, POST, PUT, DELETE, etc.) - defaults to GET
        headers: Dictionary of HTTP headers to include in the request
        data: Request body data (for POST/PUT requests)
        json: JSON data to send (for POST/PUT requests)
        timeout: Request timeout in seconds (default: 30)
        verify: Whether to verify SSL certificates (default: True)
        allow_redirects: Whether to follow redirects (default: True)

    Outputs:
        status_code: HTTP status code of the response
        data: Response data (text content)
        headers: Response headers as a dictionary
        json_data: Parsed JSON response (if response is JSON)
        url: Final URL after any redirects
    """

    # Set to True if this plugin requires authentication
    REQUIRES_AUTH: bool = False

    # List of required permissions (if REQUIRES_AUTH is True)
    REQUIRED_PERMISSIONS: list[str] = []

    def execute(self, env: Dict[str, str], params: Dict[str, Any]) -> Dict[str, str]:
        """
        Execute the plugin logic.

        Args:
            env: Current environment variables from previous tasks
            params: Parameters from the workflow YAML

        Returns:
            Dictionary of output variables that will be available to subsequent tasks
        """
        logger.info("Executing HTTP plugin")

        # Extract parameters
        url = params.get("url")
        if not url:
            raise ValueError("URL parameter is required")

        method = params.get("method", "GET").upper()
        headers = params.get("headers", {})
        data = params.get("data")
        json_data = params.get("json")
        timeout = params.get("timeout", 30)
        verify = params.get("verify", True)
        allow_redirects = params.get("allow_redirects", True)

        # Prepare request kwargs
        request_kwargs = {
            "timeout": timeout,
            "verify": verify,
            "allow_redirects": allow_redirects,
        }

        if headers:
            request_kwargs["headers"] = headers

        if data is not None:
            request_kwargs["data"] = data

        if json_data is not None:
            request_kwargs["json"] = json_data

        try:
            logger.info(f"Making {method} request to {url}")
            response = requests.request(method, url, **request_kwargs)
            response.raise_for_status()

            # Prepare outputs
            outputs = {
                "status_code": str(response.status_code),
                "data": response.text,
                "url": response.url,
            }

            # Add headers as a formatted string
            headers_str = "\n".join([f"{k}: {v}" for k, v in response.headers.items()])
            outputs["headers"] = headers_str

            # Try to parse JSON response
            try:
                json_response = response.json()
                import json
                outputs["json_data"] = json.dumps(json_response)
            except (ValueError, TypeError):
                outputs["json_data"] = ""

            logger.info(f"HTTP request successful: {response.status_code}")
            return outputs

        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP request failed: {e}")
            raise RuntimeError(f"HTTP request failed: {e}") 