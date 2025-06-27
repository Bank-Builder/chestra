import argparse
import logging
import os
import re
import sys

import yaml

from .orchestrator import TaskOrchestrator

# Set default log level to ERROR
logging.basicConfig(level=logging.ERROR)


def generate_plantuml(yaml_file: str, output_file: str = None):
    with open(yaml_file, 'r') as f:
        workflow = yaml.safe_load(f)
    tasks = workflow['workflow']['tasks']
    name = workflow['workflow'].get('name', 'Workflow')
    lines = ["@startuml", f'title {name}']
    # Define components
    for task in tasks:
        lines.append(f'component [{task["name"]}]')
    # Build a map of output var -> task name
    output_to_task = {}
    for task in tasks:
        for outvar in task.get('outputs', []):
            output_to_task[(task['name'], outvar)] = task['name']
    # Draw edges for each input, label links with VARS only (no notes)
    for task in tasks:
        for inp in task.get('inputs', []):
            m = re.match(r'([^.]+)\.(.+)', inp)
            if m:
                src, var = m.group(1), m.group(2)
                dst = task['name']
                lines.append(f'[{src}] --> [{dst}] : {var}')
            else:
                # Fallback: try to find the producing task by output name
                for (prod_task, outvar), src in output_to_task.items():
                    if outvar == inp:
                        dst = task['name']
                        lines.append(f'[{prod_task}] --> [{dst}] : {outvar}')
    lines.append("@enduml")
    plantuml_text = '\n'.join(lines)
    if output_file:
        with open(output_file, 'w') as f:
            f.write(plantuml_text)
    else:
        print(plantuml_text)


def init_plugin(plugin_name: str, plugins_dir: str) -> None:
    """Initialize a new plugin with templates."""
    import os

    # Create plugins directory if it doesn't exist
    os.makedirs(plugins_dir, exist_ok=True)

    # Convert plugin name to proper format
    plugin_class_name = ''.join(word.capitalize() for word in plugin_name.split('_')) + 'Plugin'
    plugin_filename = f"{plugin_name}.py"
    test_filename = f"{plugin_name}_test.py"
    md_filename = f"{plugin_name}.md"

    # Plugin template
    plugin_template = f'''from typing import Any, Dict
from chestra.orchestrator import TaskPlugin
from chestra.log import get_logger

logger = get_logger(__name__)

class {plugin_class_name}(TaskPlugin):
    """
    {plugin_name.replace('_', ' ').title()} plugin.
    
    This plugin [describe what this plugin does].
    
    Parameters:
        param1: Description of parameter 1
        param2: Description of parameter 2
    
    Outputs:
        OUTPUT1: Description of output 1
        OUTPUT2: Description of output 2
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
        logger.info(f"Executing {plugin_name} plugin")
        
        # Check permissions if required
        if self.REQUIRES_AUTH:
            perms = env.get("_permissions", {{}})
            if not all(perms.get(p, False) for p in self.REQUIRED_PERMISSIONS):
                raise PermissionError(f"Insufficient permissions for {plugin_name}")
        
        # TODO: Implement your plugin logic here
        # Example:
        # result = some_operation(params.get("param1", "default"))
        
        # Return output variables
        return {{
            "OUTPUT1": "value1",
            "OUTPUT2": "value2"
        }}
'''

    # Test template
    test_template = f'''import pytest
from {plugin_name} import {plugin_class_name}

def test_{plugin_name}_plugin_executes():
    """Test that the {plugin_name} plugin executes successfully."""
    plugin = {plugin_class_name}()
    result = plugin.execute({{}}, {{}})
    
    # TODO: Add proper assertions based on your plugin's expected behavior
    assert "OUTPUT1" in result
    assert "OUTPUT2" in result

def test_{plugin_name}_plugin_with_params():
    """Test that the {plugin_name} plugin handles parameters correctly."""
    plugin = {plugin_class_name}()
    params = {{"param1": "test_value"}}
    result = plugin.execute({{}}, params)
    
    # TODO: Add assertions for parameter handling
    assert result is not None

def test_{plugin_name}_plugin_with_permissions():
    """Test that the {plugin_name} plugin handles permissions correctly."""
    plugin = {plugin_class_name}()
    
    if plugin.REQUIRES_AUTH:
        # Test with insufficient permissions
        env = {{"_permissions": {{}}}}
        with pytest.raises(PermissionError):
            plugin.execute(env, {{}})
        
        # Test with sufficient permissions
        env = {{"_permissions": {{perm: True for perm in plugin.REQUIRED_PERMISSIONS}}}}
        result = plugin.execute(env, {{}})
        assert result is not None
    else:
        # Plugin doesn't require auth, should work normally
        result = plugin.execute({{}}, {{}})
        assert result is not None
'''

    # Documentation template
    md_template = f'''# {plugin_name.replace('_', ' ').title()} Plugin

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

This plugin {'requires' if plugin_name in ['cmd', 'df'] else 'does not require'} authentication.

{'Required permissions:' if plugin_name in ['cmd', 'df'] else ''}
{'* `can_execute_commands` - For command execution' if plugin_name == 'cmd' else ''}
{'* `can_view_system` - For system information access' if plugin_name == 'df' else ''}

## Example Usage

### Workflow YAML
```yaml
- name: "my_{plugin_name}_task"
  plugin: "{plugin_name}"
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
python -m pytest {test_filename}
```

## Development

1. Edit `{plugin_filename}` to implement your plugin logic
2. Update `{test_filename}` with proper test cases
3. Update this documentation with actual parameters and outputs
4. Test your plugin with a workflow

## Notes

- All plugins must inherit from `TaskPlugin`
- Return a dictionary of output variables
- Use `logger.info()` for logging
- Handle permissions if `REQUIRES_AUTH` is True
- Follow the naming convention: `{plugin_class_name}`
'''

    # Write files
    plugin_path = os.path.join(plugins_dir, plugin_filename)
    test_path = os.path.join(plugins_dir, test_filename)
    md_path = os.path.join(plugins_dir, md_filename)

    with open(plugin_path, 'w') as f:
        f.write(plugin_template)

    with open(test_path, 'w') as f:
        f.write(test_template)

    with open(md_path, 'w') as f:
        f.write(md_template)

    print(f"✅ Created plugin template: {plugin_path}")
    print(f"✅ Created test file: {test_path}")
    print(f"✅ Created documentation: {md_path}")
    print("\n📝 Next steps:")
    print(f"   1. Edit {plugin_filename} to implement your plugin logic")
    print(f"   2. Update {test_filename} with proper test cases")
    print(f"   3. Update {md_filename} with actual documentation")
    print(f"   4. Test your plugin with: python -m pytest {test_filename}")


def main():
    parser = argparse.ArgumentParser(description="Chestra Orchestrator CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Run workflow command
    run_parser = subparsers.add_parser('run', help='Run a workflow')
    run_parser.add_argument('workflow', help='Path to workflow YAML file (relative to --workflows)')
    run_parser.add_argument('--plugins', default='/plugins', help='Directory to load user plugins from (default: /plugins)')
    run_parser.add_argument('--workflows', default='/workflows', help='Directory to load workflow YAMLs from (default: /workflows)')
    run_parser.add_argument('--verbose', action='store_true', help='Enable INFO logging to stdout')
    run_parser.add_argument('--plantuml', nargs='?', const=True, help='Output PlantUML DAG diagram to file or stdout')

    # Init plugin command
    init_parser = subparsers.add_parser('init-plugin', help='Initialize a new plugin')
    init_parser.add_argument('plugin_name', help='Name of the plugin to create')
    init_parser.add_argument('--plugins-dir', default='plugins', help='Directory to create plugin in (default: plugins)')

    args = parser.parse_args()

    # Set log level after parsing args
    verbose = getattr(args, 'verbose', False)
    if verbose:
        logging.getLogger().setLevel(logging.INFO)
        for logger_name in [
            "chestra.orchestrator",
            "chestra.plugins.cmd",
            "chestra.plugins.df",
            "chestra.plugins.end",
            "chestra.plugins.start",
            "chestra.plugins.changed",
        ]:
            logger = logging.getLogger(logger_name)
            logger.setLevel(logging.INFO)
            logger.propagate = False
    else:
        logging.getLogger().setLevel(logging.ERROR)
        for logger_name in [
            "chestra.orchestrator",
            "chestra.plugins.cmd",
            "chestra.plugins.df",
            "chestra.plugins.end",
            "chestra.plugins.start",
            "chestra.plugins.changed",
        ]:
            logger = logging.getLogger(logger_name)
            logger.setLevel(logging.ERROR)
            logger.propagate = False

    if args.command == 'init-plugin':
        init_plugin(args.plugin_name, args.plugins_dir)
        return

    if args.command == 'run':
        if args.plantuml:
            output_file = None if args.plantuml is True else args.plantuml
            generate_plantuml(args.workflow, output_file)
            sys.exit(0)

        orchestrator = TaskOrchestrator(
            plugins_dir=args.plugins,
            workflows_dir=args.workflows
        )
        workflow_path = os.path.join(args.workflows, args.workflow)
        orchestrator.load_workflow(workflow_path)
        orchestrator.run()
    else:
        parser.print_help()
