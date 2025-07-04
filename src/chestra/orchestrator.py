import importlib
import logging
import pkgutil
import threading
import time
from abc import ABC, abstractmethod
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Any, Callable, Dict, List, Optional, Type

import requests
import yaml

# Set up a standard logger for the orchestrator
logger = logging.getLogger("chestra.orchestrator")
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
handler.setFormatter(formatter)
if not logger.hasHandlers():
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

class TaskPlugin(ABC):
    """Abstract base class for all task plugins."""
    @abstractmethod
    def execute(self, env: Dict[str, str], params: Dict[str, Any]) -> Dict[str, str]:
        """
        Execute the plugin logic.
        Args:
            env: Current environment variables.
            params: Parameters from the workflow YAML.
        Returns:
            Dictionary of output variables.
        """
        pass

class Task:
    """Represents a single task in the workflow."""
    name: str
    plugin_name: str
    inputs: List[str]
    outputs: List[str]
    params: Dict[str, Any]
    completed: bool
    plugin: Optional[TaskPlugin]
    requires_auth: bool
    permissions: List[str]

    def __init__(
        self,
        name: str,
        plugin_name: str,
        inputs: List[str],
        outputs: List[str],
        params: Dict[str, Any],
        requires_auth: bool = False,
        permissions: Optional[List[str]] = None,
    ) -> None:
        self.name = name
        self.plugin_name = plugin_name
        self.inputs = inputs
        self.outputs = outputs
        self.params = params or {}
        self.completed = False
        self.plugin = None
        self.requires_auth = requires_auth
        self.permissions = permissions or []

    def can_run(self, env: Dict[str, str]) -> bool:
        """
        Check if all input variables are available and task is not completed.
        Inputs are now namespaced as TASKNAME.VARNAME.
        """
        return all(var in env for var in self.inputs) and not self.completed

    def execute(
        self,
        env: Dict[str, str],
        get_permissions: Optional[Callable[[str], Dict[str, bool]]] = None,
    ) -> Dict[str, str]:
        """
        Execute the task using its plugin. Handles permission checks if required.
        Args:
            env: Current environment variables.
            get_permissions: Function to fetch permissions if needed.
        Returns:
            Dictionary of output variables.
        """
        if not self.can_run(env):
            return {}
        if self.requires_auth and get_permissions:
            auth_token: Optional[str] = env.get('AUTH_TOKEN')
            perms: Dict[str, bool] = get_permissions(auth_token)
            env['_permissions'] = perms
            if self.permissions and not all(perms.get(p, False) for p in self.permissions):
                logger.warning(f"Task {self.name} failed permission check")
                return {}
        logger.info(f"Executing task: {self.name} ({self.plugin_name})")
        if not self.plugin:
            logger.error(f"Plugin not loaded for task {self.name}")
            raise RuntimeError(f"Plugin not loaded for task {self.name}")
        try:
            result: Dict[str, str] = self.plugin.execute(env, self.params)
            self.completed = True
            # Only return variables that are declared as outputs
            return {k: v for k, v in result.items() if k in self.outputs}
        except Exception as e:
            logger.error(f"Task {self.name} failed: {e}")
            return {}

class PluginManager:
    """Manages loading and retrieval of plugins."""
    plugins: Dict[str, TaskPlugin]
    def __init__(self) -> None:
        self.plugins = {}
    def load_builtin_plugins(self) -> None:
        """Dynamically load all plugins from the plugins directory."""
        import chestra.plugins
        package = chestra.plugins
        for _, modname, ispkg in pkgutil.iter_modules(package.__path__):
            if not ispkg:
                module = importlib.import_module(f"chestra.plugins.{modname}")
                class_name = ''.join([part.capitalize() for part in modname.split('_')]) + 'Plugin'
                plugin_class: Type[TaskPlugin] = getattr(module, class_name, None)
                if plugin_class:
                    self.plugins[modname] = plugin_class()
                    logger.info(f"Loaded plugin: {modname} -> {plugin_class.__name__}")
                else:
                    logger.warning(f"No plugin class found in module: {modname}")
    def load_user_plugins(self, plugins_dir: str) -> None:
        """Load plugins from a user-supplied directory (each .py file is a plugin)."""
        import importlib.util
        import os
        if not os.path.isdir(plugins_dir):
            logger.info(f"User plugins directory {plugins_dir} does not exist or is not a directory.")
            return
        for fname in os.listdir(plugins_dir):
            if fname.endswith('.py') and not fname.startswith('_'):
                modname = fname[:-3]
                fpath = os.path.join(plugins_dir, fname)
                spec = importlib.util.spec_from_file_location(modname, fpath)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    # Convention: plugin class is <CamelCase>Plugin
                    class_name = ''.join([part.capitalize() for part in modname.split('_')]) + 'Plugin'
                    plugin_class: Type[TaskPlugin] = getattr(module, class_name, None)
                    if plugin_class:
                        self.plugins[modname] = plugin_class()
                        logger.info(f"Loaded plugin: {modname} -> {plugin_class.__name__}")
                    else:
                        logger.warning(f"No plugin class found in user module: {modname}")
    def get_plugin(self, name: str) -> TaskPlugin:
        """Retrieve a plugin by name."""
        if name not in self.plugins:
            logger.error(f"Plugin {name} not found")
            raise KeyError(f"Plugin {name} not found")
        return self.plugins[name]

class TaskOrchestrator:
    """Main orchestrator for loading workflows and running tasks."""
    tasks: List[Task]
    env: Dict[str, str]
    plugin_manager: PluginManager
    auth_service_url: str
    env_lock: threading.Lock
    plugins_dir: str
    workflows_dir: str

    def __init__(self, plugins_dir: str = '/plugins', workflows_dir: str = '/workflows') -> None:
        self.tasks = []
        self.env = {}
        self.plugin_manager = PluginManager()
        self.auth_service_url = "https://attica.tech/permissions"
        self.env_lock = threading.Lock()
        self.plugins_dir = plugins_dir
        self.workflows_dir = workflows_dir
    def get_permissions(self, auth_token: Optional[str]) -> Dict[str, bool]:
        """
        Fetch permissions from the Attica Auth service.
        Args:
            auth_token: The authentication token.
        Returns:
            Dictionary of permissions.
        """
        if not auth_token:
            return {}
        try:
            response = requests.post(
                self.auth_service_url,
                json={"auth_token": auth_token},
                timeout=3,
            )
            response.raise_for_status()
            return response.json().get('permissions', {})
        except Exception as e:
            logger.error(f"Auth service error: {e}")
            return {}
    def load_workflow(self, yaml_file: str) -> None:
        """
        Load workflow definition from a YAML file and initialize tasks.
        Args:
            yaml_file: Path to the workflow YAML file.
        """
        with open(yaml_file, 'r') as f:
            workflow: Dict[str, Any] = yaml.safe_load(f)
        # Always load built-in plugins first
        self.plugin_manager.load_builtin_plugins()
        # Then load user plugins if the directory exists
        self.plugin_manager.load_user_plugins(self.plugins_dir)
        seen_names = set()
        for task_def in workflow['workflow']['tasks']:
            name = task_def['name']
            if name in seen_names:
                raise ValueError(f"Duplicate task name: {name}")
            seen_names.add(name)
            # Inject task_name into params for plugin use
            params = task_def.get('params', {}).copy()
            params['task_name'] = name
            task = Task(
                name=name,
                plugin_name=task_def['plugin'],
                inputs=task_def.get('inputs', []),
                outputs=task_def.get('outputs', []),
                params=params,
                requires_auth=task_def.get('requires_auth', False),
                permissions=task_def.get('permissions', {}).get('required', [])
                if 'permissions' in task_def
                else [],
            )
            task.plugin = self.plugin_manager.get_plugin(task.plugin_name)
            self.tasks.append(task)
    def run(self) -> None:
        """
        Main execution loop. Runs eligible tasks in parallel when their dependencies are met.
        Keeps all running tasks alive and updates environment as soon as any task completes.
        """
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures: Dict[Future, Task] = {}
            running_tasks: set = set()
            while True:
                # Start all eligible tasks that haven't started yet
                for task in self.tasks:
                    if task.can_run(self.env) and task not in running_tasks:
                        future = executor.submit(self._run_task_threadsafe, task)
                        futures[future] = task
                        running_tasks.add(task)
                # Check for completed tasks and update env
                done_futures = [f for f in futures if f.done()]
                for f in done_futures:
                    task = futures[f]
                    result = f.result()
                    with self.env_lock:
                        namespaced = {f"{task.name}.{k}": v for k, v in result.items()}
                        self.env.update(namespaced)
                    task.completed = True
                    del futures[f]
                # If all tasks are completed, break
                if all(task.completed for task in self.tasks):
                    logger.info("Workflow completed successfully!")
                    break
                # If no tasks are running or can run, and not all are completed, stuck
                no_running = not any(
                    not t.completed for t in self.tasks if t in running_tasks
                )
                no_eligible = not any(
                    t.can_run(self.env) for t in self.tasks if not t.completed
                )
                if no_running and no_eligible:
                    logger.error("Workflow stuck - some tasks cannot run")
                    incomplete: List[str] = [t.name for t in self.tasks if not t.completed]
                    logger.error(f"Incomplete tasks: {incomplete}")
                    logger.error(f"Current environment: {self.env}")
                    break
                time.sleep(0.1)

    def _run_task_threadsafe(self, task: Task) -> Dict[str, str]:
        # Copy env for thread safety
        with self.env_lock:
            env_copy = self.env.copy()
        return task.execute(env_copy, get_permissions=self.get_permissions)
