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

## TODO

### High Priority
- [ ] **CLI Interface**: Implement the main CLI entry point (`chestra run workflow.yaml`)
- [ ] **Error Handling**: Improve error handling and user feedback for workflow failures
- [ ] **Logging**: Add structured logging with configurable levels
- [ ] **Configuration**: Add support for configuration files (e.g., `chestra.yaml`)
- [ ] **Validation**: Add YAML schema validation for workflow definitions

### Core Features
- [ ] **Task Dependencies**: Implement proper dependency resolution and execution order
- [ ] **Conditional Execution**: Add support for conditional task execution based on environment variables
- [ ] **Retry Logic**: Implement retry mechanisms for failed tasks
- [ ] **Timeout Handling**: Add timeout support for long-running tasks
- [ ] **Task Status**: Add task status tracking and reporting
- [ ] **Workflow Templates**: Create reusable workflow templates

### Plugin System Enhancements
- [ ] **Plugin Discovery**: Auto-discover plugins from external directories
- [ ] **Plugin Versioning**: Add version support for plugins
- [ ] **Plugin Documentation**: Generate documentation from plugin docstrings
- [ ] **Plugin Testing Framework**: Create testing utilities for plugin development
- [ ] **Plugin Marketplace**: Consider a plugin registry/repository

### Security & Permissions
- [ ] **Local Permission System**: Add local permission checking without external service
- [ ] **Permission Caching**: Cache permissions to reduce API calls
- [ ] **Audit Logging**: Add comprehensive audit logging for security-sensitive operations
- [ ] **Encrypted Parameters**: Support for encrypted parameter values

### Performance & Scalability
- [ ] **Async Support**: Full async/await support for plugins
- [ ] **Resource Limits**: Add resource usage limits and monitoring
- [ ] **Distributed Execution**: Support for distributed task execution
- [ ] **Caching**: Add result caching for expensive operations
- [ ] **Progress Tracking**: Real-time progress reporting for long workflows

### Developer Experience
- [ ] **Debug Mode**: Add debug mode with detailed execution information
- [ ] **Dry Run**: Implement dry-run mode for testing workflows
- [ ] **Workflow Visualization**: Generate visual representations of workflows
- [ ] **IDE Integration**: Create extensions for popular IDEs
- [ ] **Interactive Mode**: Add interactive workflow builder

### Documentation & Examples
- [ ] **API Documentation**: Complete API documentation with examples
- [ ] **Tutorial Series**: Create step-by-step tutorials
- [ ] **Example Workflows**: Add more example workflows for common use cases
- [ ] **Best Practices Guide**: Document best practices for workflow design
- [ ] **Migration Guide**: Guide for upgrading between versions

### Testing & Quality
- [ ] **Integration Tests**: Add comprehensive integration tests
- [ ] **Performance Tests**: Add performance benchmarking
- [ ] **Security Tests**: Add security testing for permission system
- [ ] **Code Coverage**: Improve test coverage to >90%
- [ ] **CI/CD Pipeline**: Set up automated testing and deployment

### Packaging & Distribution
- [ ] **Docker Support**: Add Docker containerization
- [ ] **PyPI Publishing**: Automated PyPI releases
- [ ] **Binary Distributions**: Create standalone executables
- [ ] **Dependency Management**: Update to use modern dependency management (poetry/pdm)

### Monitoring & Observability
- [ ] **Metrics Collection**: Add metrics collection for monitoring
- [ ] **Health Checks**: Implement health check endpoints
- [ ] **Alerting**: Add alerting for workflow failures
- [ ] **Dashboard**: Create a web dashboard for workflow monitoring

### Community & Ecosystem
- [ ] **Contributing Guidelines**: Establish contribution guidelines
- [ ] **Code of Conduct**: Add community code of conduct
- [ ] **Plugin Ecosystem**: Foster a community plugin ecosystem
- [ ] **User Feedback**: Set up channels for user feedback and feature requests 