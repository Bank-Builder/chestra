import logging
from typing import Any, Dict

from chestra.orchestrator import TaskPlugin

logger = logging.getLogger("chestra.plugins.end")
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
handler.setFormatter(formatter)
if not logger.hasHandlers():
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

class EndPlugin(TaskPlugin):
    """Plugin that marks the end of the workflow."""
    def execute(self, env: Dict[str, str], params: Dict[str, Any]) -> Dict[str, str]:
        logger.info("Workflow end reached")
        return {}
