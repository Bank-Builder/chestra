# HTTP Plugin

## Description

The HTTP plugin makes HTTP requests with configurable methods, headers, and options. It supports all HTTP methods (GET, POST, PUT, DELETE, etc.) and provides comprehensive output including status codes, response data, headers, and parsed JSON.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| url | string | Yes | - | The URL to make the request to |
| method | string | No | "GET" | HTTP method (GET, POST, PUT, DELETE, etc.) |
| headers | object | No | {} | Dictionary of HTTP headers to include in the request |
| data | string/bytes | No | - | Request body data (for POST/PUT requests) |
| json | object | No | - | JSON data to send (for POST/PUT requests) |
| timeout | integer | No | 30 | Request timeout in seconds |
| verify | boolean | No | true | Whether to verify SSL certificates |
| allow_redirects | boolean | No | true | Whether to follow redirects |

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| status_code | string | HTTP status code of the response |
| data | string | Response data (text content) |
| headers | string | Response headers as a formatted string |
| json_data | string | Parsed JSON response (if response is JSON, empty string otherwise) |
| url | string | Final URL after any redirects |

## Permissions

This plugin does not require authentication.

## Example Usage

### Basic GET Request
```yaml
- name: "fetch_data"
  plugin: "http"
  outputs: ["status_code", "data", "headers", "json_data", "url"]
  params:
    url: "https://api.example.com/data"
    method: "GET"
```

### POST Request with JSON Data
```yaml
- name: "create_user"
  plugin: "http"
  outputs: ["status_code", "data", "headers", "json_data", "url"]
  params:
    url: "https://api.example.com/users"
    method: "POST"
    headers:
      Content-Type: "application/json"
      Authorization: "Bearer $AUTH_TOKEN"
    json:
      name: "John Doe"
      email: "john@example.com"
```

### Request with Custom Options
```yaml
- name: "api_call"
  plugin: "http"
  outputs: ["status_code", "data", "headers", "json_data", "url"]
  params:
    url: "https://api.example.com/secure"
    method: "GET"
    headers:
      X-API-Key: "$API_KEY"
    timeout: 60
    verify: false
    allow_redirects: false
```

### Using Previous Task Outputs
```yaml
- name: "get_user"
  plugin: "http"
  inputs: ["auth.token"]
  outputs: ["status_code", "data", "headers", "json_data", "url"]
  params:
    url: "https://api.example.com/user/profile"
    method: "GET"
    headers:
      Authorization: "Bearer $auth.token"
```

## Environment Variables

This plugin can access environment variables from previous tasks:
- `$AUTH_TOKEN` - Authentication token
- `$API_KEY` - API key for authentication
- Any output from previous tasks (e.g., `$previous_task.output`)

## Error Handling

The plugin will raise a `RuntimeError` if:
- The HTTP request fails (network error, timeout, etc.)
- The server returns an error status code (4xx, 5xx)

The plugin will raise a `ValueError` if:
- The `url` parameter is missing

## Testing

Run the plugin tests:
```bash
python -m pytest plugins/http_test.py
```

## Development

1. Edit `plugins/http.py` to modify the plugin logic
2. Update `plugins/http_test.py` with additional test cases
3. Update this documentation with any new parameters or outputs
4. Test your plugin with a workflow

## Notes

- All HTTP methods are supported (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS)
- Headers are passed as a dictionary in the params
- The `data` parameter is for raw request body data
- The `json` parameter automatically sets Content-Type to application/json
- Response headers are returned as a formatted string for easy parsing
- JSON responses are automatically parsed and returned as a JSON string
- Non-JSON responses will have an empty `json_data` output
- The plugin uses the `requests` library for HTTP operations
