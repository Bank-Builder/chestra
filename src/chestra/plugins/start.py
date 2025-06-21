from typing import Any, Dict

from chestra.orchestrator import TaskPlugin


class StartPlugin(TaskPlugin):
    """Plugin that emits TRUE to start the workflow."""
    def execute(self, env: Dict[str, str], params: Dict[str, Any]) -> Dict[str, str]:
        return {"TRUE": "1"}
