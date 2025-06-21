import logging
import os
import time
from typing import Any, Dict

from chestra.orchestrator import TaskPlugin

logger = logging.getLogger("chestra.plugins.touched")
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
handler.setFormatter(formatter)
if not logger.hasHandlers():
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

class TouchedPlugin(TaskPlugin):
    """Plugin that waits for a file to be touched, emits TRUE if touched within timeout."""
    REQUIRES_AUTH: bool = False
    def execute(self, env: Dict[str, str], params: Dict[str, Any]) -> Dict[str, str]:
        file_path: str = params.get("file", "semaphore.txt")
        timeout: int = int(params.get("timeout", env.get("TIMEOUT", "100")))
        initial_mtime: float = (
            os.path.getmtime(file_path) if os.path.exists(file_path) else 0
        )
        end_time: float = time.time() + timeout
        logger.info(f"Watching file {file_path} for changes with timeout {timeout} seconds")
        while time.time() < end_time:
            current_mtime: float = (
                os.path.getmtime(file_path) if os.path.exists(file_path) else 0
            )
            if current_mtime != initial_mtime:
                logger.info(f"File {file_path} was touched!")
                return {"TRUE": "1"}
            time.sleep(1)
        logger.warning(f"Timeout reached without file {file_path} being touched")
        return {}
