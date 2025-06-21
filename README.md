# Chestra: The Pythonista Orchestrator

Chestra is a modular, plugin-based workflow orchestrator for Pythonistas. It allows you to define, schedule, and execute complex task workflows using YAML configuration, with support for parallel and asynchronous execution, permissions, and custom plugins.

## Features
- **YAML-based workflow definitions**
- **Plugin architecture** for easy extensibility
- **Parallel and async task execution**
- **Permission model** with external auth service integration
- **Environment variable and parameter passing**
- **Human-friendly CLI and Python API**

## Installation
```bash
pip install chestra
```

## Usage
1. Define your workflow in a YAML file:
```yaml
workflow:
  name: "Example Workflow"
  tasks:
    - name: "start"
      plugin: "start"
      outputs: ["TRUE"]
    - name: "my_task"
      plugin: "my_plugin"
      inputs: ["TRUE"]
      outputs: ["RESULT"]
      params:
        foo: "bar"
    - name: "end"
      plugin: "end"
      inputs: ["TRUE"]
```
2. Run the orchestrator:
```bash
chestra run workflow.yaml
```

## Creating Plugins
See [docs/DEVELOPER.md](docs/DEVELOPER.md) for details on writing your own plugins.

## Project Structure
```
chestra/
  src/orquestra/           # Main package
  docs/                  # Documentation
  tests/                 # Tests
  README.md
  requirements.txt
  setup.py / pyproject.toml
```

## License
MIT 