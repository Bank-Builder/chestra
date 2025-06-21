import pytest
from chestra.orchestrator import TaskOrchestrator
from chestra.plugins.start import StartPlugin

def test_plugin_loading():
    orchestrator = TaskOrchestrator()
    orchestrator.plugin_manager.load_builtin_plugins()
    assert 'start' in orchestrator.plugin_manager.plugins
    assert 'df' in orchestrator.plugin_manager.plugins
    assert 'cmd' in orchestrator.plugin_manager.plugins
    assert 'end' in orchestrator.plugin_manager.plugins

def test_start_plugin_executes():
    plugin = StartPlugin()
    result = plugin.execute({}, {})
    assert result == {"TRUE": "1"} 