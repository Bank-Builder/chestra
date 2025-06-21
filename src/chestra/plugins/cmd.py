from chestra.orchestrator import TaskPlugin
from chestra.log import get_logger
import subprocess
from typing import Any, Dict

logger = get_logger(__name__)

class CmdPlugin(TaskPlugin):
    """
    Plugin that executes a shell command. Requires permission if present in env.
    How return values are handled:
    - The command can output environment variable assignments (e.g., VAR=value) to stdout.
    - If the command outputs lines in the form VAR=value, these are parsed and returned as output variables.
    - These returned variables are then injected into Chestra's environment for use by subsequent tasks.
    - If no such lines are output, an empty dict is returned.
    """
    REQUIRED_PERMISSIONS: list[str] = ["can_execute_commands"]
    def execute(self, env: Dict[str, str], params: Dict[str, Any]) -> Dict[str, str]:
        perms: Dict[str, Any] = env.get("_permissions", {})
        if perms and not perms.get("can_execute_commands", False):
            logger.error("Command execution not allowed by permissions")
            raise PermissionError("Command execution not allowed")
        command: str = params.get("command", "")
        if not command:
            logger.warning("No command provided to CmdPlugin")
            return {}
        formatted_cmd: str = command
        for var, value in env.items():
            formatted_cmd = formatted_cmd.replace(f"${var}", value)
        logger.info(f"About to run: {formatted_cmd}")
        result: subprocess.CompletedProcess[str] = subprocess.run(
            formatted_cmd, shell=True, capture_output=True, text=True
        )
        logger.info(f"Command returncode: {result.returncode}")
        logger.info(f"Command stdout: {result.stdout!r}")
        logger.info(f"Command stderr: {result.stderr!r}")
        print(result.stdout, end="")  # Print command output to stdout
        output_vars: Dict[str, str] = {}
        for line in result.stdout.splitlines():
            if "=" in line:
                var, value = line.split("=", 1)
                output_vars[var.strip()] = value.strip()
        if output_vars:
            logger.info(f"CmdPlugin output vars: {output_vars}")
        return output_vars
