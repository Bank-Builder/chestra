# Chestra Developer Guide: Writing Plugins

Chestra supports a modular plugin architecture. Plugins are Python classes that implement the `TaskPlugin` interface and provide custom task logic.

## Plugin Basics

A plugin is a Python class that inherits from `TaskPlugin` and implements the `execute` method:

```python
from chestra.orchestrator import TaskPlugin

class Plugin(TaskPlugin):
    def execute(self, env, params):
        # Your logic here
        return {"OUTPUT_VAR": "value"}
```

- `env`: Dictionary of current environment variables and values
- `params`: Dictionary of parameters from the workflow YAML
- Return a dictionary of output variables

## Permissions

If your plugin requires permissions, set `REQUIRES_AUTH = True` and define `REQUIRED_PERMISSIONS`:

```python
class Plugin(TaskPlugin):
    REQUIRES_AUTH = True
    REQUIRED_PERMISSIONS = ["can_do_something"]
    def execute(self, env, params):
        perms = env.get('_permissions', {})
        if not perms.get('can_do_something', False):
            raise PermissionError("Not allowed!")
        # ...
```

## Registering Plugins

- Place your plugin in a Python file (e.g., `plugins/myplugin.py`)
- Import and register it in your workflow YAML by specifying the plugin name

## Example Workflow YAML

```yaml
- name: "my_task"
  plugin: "myplugin"
  inputs: ["TRUE"]
  outputs: ["RESULT"]
  params:
    foo: "bar"
```

## Testing Plugins

- Write unit tests in the `tests/` directory
- Use pytest for best results

## Contributing

- Follow PEP8 and project guidelines
- Document your plugin and its parameters 