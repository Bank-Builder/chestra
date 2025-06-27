# My Custom Plugin Plugin

## Description

[Describe what this plugin does and when to use it]

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| param1 | string | No | "default" | Description of parameter 1 |
| param2 | integer | No | 100 | Description of parameter 2 |

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| OUTPUT1 | string | Description of output 1 |
| OUTPUT2 | string | Description of output 2 |

## Permissions

This plugin does not require authentication.





## Example Usage

### Workflow YAML
```yaml
- name: "my_my_custom_plugin_task"
  plugin: "my_custom_plugin"
  inputs: ["previous_task.OUTPUT"]
  outputs: ["OUTPUT1", "OUTPUT2"]
  params:
    param1: "custom_value"
    param2: 200
```

### Environment Variables
This plugin can access environment variables from previous tasks:
- `$PREVIOUS_TASK.OUTPUT` - Output from previous task
- `$AUTH_TOKEN` - Authentication token (if required)

## Testing

Run the plugin tests:
```bash
python -m pytest my_custom_plugin_test.py
```

## Development

1. Edit `my_custom_plugin.py` to implement your plugin logic
2. Update `my_custom_plugin_test.py` with proper test cases
3. Update this documentation with actual parameters and outputs
4. Test your plugin with a workflow

## Notes

- All plugins must inherit from `TaskPlugin`
- Return a dictionary of output variables
- Use `logger.info()` for logging
- Handle permissions if `REQUIRES_AUTH` is True
- Follow the naming convention: `MyCustomPluginPlugin`
