from typing import Any, Dict

from chestra.log import get_logger
from chestra.orchestrator import TaskPlugin

logger = get_logger(__name__)

class MyCustomPluginPlugin(TaskPlugin):
    """
    My Custom Plugin plugin.

    This plugin [describe what this plugin does].

    Parameters:
        param1: Description of parameter 1
        param2: Description of parameter 2

    Outputs:
        OUTPUT1: Description of output 1
        OUTPUT2: Description of output 2
    """

    # Set to True if this plugin requires authentication
    REQUIRES_AUTH: bool = False

    # List of required permissions (if REQUIRES_AUTH is True)
    REQUIRED_PERMISSIONS: list[str] = []

    def execute(self, env: Dict[str, str], params: Dict[str, Any]) -> Dict[str, str]:
        """
        Execute the plugin logic.

        Args:
            env: Current environment variables from previous tasks
            params: Parameters from the workflow YAML

        Returns:
            Dictionary of output variables that will be available to subsequent tasks
        """
        logger.info("Executing my_custom_plugin plugin")

        # Check permissions if required
        if self.REQUIRES_AUTH:
            perms = env.get("_permissions", {})
            if not all(perms.get(p, False) for p in self.REQUIRED_PERMISSIONS):
                raise PermissionError("Insufficient permissions for my_custom_plugin")

        # TODO: Implement your plugin logic here
        # Example:
        # result = some_operation(params.get("param1", "default"))

        # Return output variables
        return {
            "OUTPUT1": "value1",
            "OUTPUT2": "value2"
        }
