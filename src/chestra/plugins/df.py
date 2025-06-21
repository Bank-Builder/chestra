import subprocess
from typing import Any, Dict

from chestra.orchestrator import TaskPlugin


class DfPlugin(TaskPlugin):
    """Plugin that emits main disk volume and free space. Requires permission if present in env."""
    REQUIRED_PERMISSIONS: list[str] = ["can_view_system"]
    def execute(self, env: Dict[str, str], params: Dict[str, Any]) -> Dict[str, str]:
        perms: Dict[str, Any] = env.get("_permissions", {})
        if perms and not perms.get("can_view_system", False):
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
