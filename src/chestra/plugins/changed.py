import logging
import os
import time
from typing import Any, Dict
from chestra.orchestrator import TaskPlugin

logger = logging.getLogger("chestra.plugins.changed")
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
handler.setFormatter(formatter)
if not logger.hasHandlers():
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

class ChangedPlugin(TaskPlugin):
    """Plugin that emits TRUE if a file is created or its contents/mtime change within timeout."""
    REQUIRES_AUTH: bool = False
    def execute(self, env: Dict[str, str], params: Dict[str, Any]) -> Dict[str, str]:
        file_path: str = params.get("file", "semaphore.txt")
        timeout: int = int(params.get("timeout", env.get("TIMEOUT", "100")))
        exists = os.path.exists(file_path)
        initial_mtime = os.path.getmtime(file_path) if exists else None
        initial_size = os.path.getsize(file_path) if exists else None
        end_time: float = time.time() + timeout
        logger.info(f"Watching file {file_path} for creation or changes with timeout {timeout} seconds")
        while time.time() < end_time:
            now_exists = os.path.exists(file_path)
            if not exists and now_exists:
                logger.info(f"File {file_path} was created!")
                return {"TRUE": "1"}
            if now_exists:
                current_mtime = os.path.getmtime(file_path)
                current_size = os.path.getsize(file_path)
                if (initial_mtime is not None and current_mtime != initial_mtime) or \
                   (initial_size is not None and current_size != initial_size):
                    logger.info(f"File {file_path} was changed!")
                    return {"TRUE": "1"}
            time.sleep(1)
        logger.warning(f"Timeout reached without file {file_path} being created or changed")
        return {}
