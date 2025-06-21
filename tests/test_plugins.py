import pytest
from chestra.orchestrator import TaskOrchestrator
from chestra.plugins.start import StartPlugin
from chestra.plugins.df import DfPlugin

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

def test_df_plugin_with_permissions():
    plugin = DfPlugin()
    env = {"_permissions": {"can_view_system": True}}
    result = plugin.execute(env, {})
    assert "MAIN_VOLUME" in result
    assert "FREE_SPACE" in result 