import os
import subprocess
import time
from typing import Any, Dict

from .orchestrator import TaskPlugin


class StartPlugin(TaskPlugin):
    """Plugin that emits TRUE to start the workflow."""
    def execute(self, env: Dict[str, str], params: Dict[str, Any]) -> Dict[str, str]:
        return {"TRUE": "1"}

class DfPlugin(TaskPlugin):
    """Plugin that emits main disk volume and free space. Requires permission."""
    REQUIRES_AUTH: bool = True
    REQUIRED_PERMISSIONS: list[str] = ["can_view_system"]
    def execute(self, env: Dict[str, str], params: Dict[str, Any]) -> Dict[str, str]:
        perms: Dict[str, Any] = env.get("_permissions", {})
        if self.REQUIRES_AUTH and not perms.get("can_view_system", False):
            raise PermissionError("Insufficient permissions for df")
        result: subprocess.CompletedProcess[str] = subprocess.run(
            "df -h / | awk 'NR==2 {print $1 \" \" $4}'",
            shell=True,
            check=True,
            capture_output=True,
            text=True,
        )
        volume, free = result.stdout.strip().split()
        return {
            "MAIN_VOLUME": volume.replace("/dev/", ""),
            "FREE_SPACE": free,
        }

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
        while time.time() < end_time:
            current_mtime: float = (
                os.path.getmtime(file_path) if os.path.exists(file_path) else 0
            )
            if current_mtime != initial_mtime:
                return {"TRUE": "1"}
            time.sleep(1)
        return {}

class CmdPlugin(TaskPlugin):
    """
    Plugin that executes a shell command. Requires permission.

    How return values are handled:
    - The command can output environment variable assignments (e.g., VAR=value) to stdout.
    - If the command outputs lines in the form VAR=value, these are parsed and returned as output variables.
    - These returned variables are then injected into Chestra's environment for use by subsequent tasks.
    - If no such lines are output, an empty dict is returned.
    """
    REQUIRES_AUTH: bool = True
    REQUIRED_PERMISSIONS: list[str] = ["can_execute_commands"]
    def execute(self, env: Dict[str, str], params: Dict[str, Any]) -> Dict[str, str]:
        perms: Dict[str, Any] = env.get("_permissions", {})
        if self.REQUIRES_AUTH and not perms.get("can_execute_commands", False):
            raise PermissionError("Command execution not allowed")
        command: str = params.get("command", "")
        if not command:
            return {}
        formatted_cmd: str = command
        for var, value in env.items():
            formatted_cmd = formatted_cmd.replace(f"${var}", value)
        result: subprocess.CompletedProcess[str] = subprocess.run(
            formatted_cmd, shell=True, capture_output=True, text=True
        )
        output_vars: Dict[str, str] = {}
        for line in result.stdout.splitlines():
            if "=" in line:
                var, value = line.split("=", 1)
                output_vars[var.strip()] = value.strip()
        return output_vars

class EndPlugin(TaskPlugin):
    """Plugin that marks the end of the workflow."""
    def execute(self, env: Dict[str, str], params: Dict[str, Any]) -> Dict[str, str]:
        print("Workflow end reached")
        return {}
