import logging
import subprocess
from typing import Any, Dict

from chestra.orchestrator import TaskPlugin

logger = logging.getLogger("chestra.plugins.cmd")
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
handler.setFormatter(formatter)
if not logger.hasHandlers():
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

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
            logger.error("Command execution not allowed by permissions")
            raise PermissionError("Command execution not allowed")
        command: str = params.get("command", "")
        if not command:
            logger.warning("No command provided to CmdPlugin")
            return {}
        formatted_cmd: str = command
        for var, value in env.items():
            formatted_cmd = formatted_cmd.replace(f"${var}", value)
        logger.info(f"Executing command: {formatted_cmd}")
        result: subprocess.CompletedProcess[str] = subprocess.run(
            formatted_cmd, shell=True, capture_output=True, text=True
        )
        output_vars: Dict[str, str] = {}
        for line in result.stdout.splitlines():
            if "=" in line:
                var, value = line.split("=", 1)
                output_vars[var.strip()] = value.strip()
        if output_vars:
            logger.info(f"CmdPlugin output vars: {output_vars}")
        return output_vars
