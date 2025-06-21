import argparse
import logging
import re
import sys

import yaml

from .orchestrator import TaskOrchestrator

# Set default log level to ERROR
logging.basicConfig(level=logging.ERROR)


def generate_plantuml(yaml_file: str, output_file: str = None):
    with open(yaml_file, 'r') as f:
        workflow = yaml.safe_load(f)
    tasks = workflow['workflow']['tasks']
    name = workflow['workflow'].get('name', 'Workflow')
    lines = ["@startuml", f'title {name}']
    # Define components
    for task in tasks:
        lines.append(f'component [{task["name"]}]')
    # Build a map of output var -> task name
    output_to_task = {}
    for task in tasks:
        for outvar in task.get('outputs', []):
            output_to_task[(task['name'], outvar)] = task['name']
    # Draw edges for each input, label links with VARS only (no notes)
    for task in tasks:
        for inp in task.get('inputs', []):
            m = re.match(r'([^.]+)\.(.+)', inp)
            if m:
                src, var = m.group(1), m.group(2)
                dst = task['name']
                lines.append(f'[{src}] --> [{dst}] : {var}')
            else:
                # Fallback: try to find the producing task by output name
                for (prod_task, outvar), src in output_to_task.items():
                    if outvar == inp:
                        dst = task['name']
                        lines.append(f'[{prod_task}] --> [{dst}] : {outvar}')
    lines.append("@enduml")
    plantuml_text = '\n'.join(lines)
    if output_file:
        with open(output_file, 'w') as f:
            f.write(plantuml_text)
    else:
        print(plantuml_text)


def main():
    parser = argparse.ArgumentParser(description="Chestra Orchestrator CLI")
    parser.add_argument('workflow', help='Path to workflow YAML file')
    parser.add_argument('--verbose', action='store_true', help='Enable INFO logging to stdout')
    parser.add_argument('--plantuml', nargs='?', const=True, help='Output PlantUML DAG diagram to file or stdout')
    args = parser.parse_args()

    # Set log level after parsing args
    if args.verbose:
        logging.getLogger().setLevel(logging.INFO)
        for logger_name in [
            "chestra.orchestrator",
            "chestra.plugins.cmd",
            "chestra.plugins.df",
            "chestra.plugins.end",
            "chestra.plugins.start",
            "chestra.plugins.changed",
        ]:
            logger = logging.getLogger(logger_name)
            logger.setLevel(logging.INFO)
            logger.propagate = False
    else:
        logging.getLogger().setLevel(logging.ERROR)
        for logger_name in [
            "chestra.orchestrator",
            "chestra.plugins.cmd",
            "chestra.plugins.df",
            "chestra.plugins.end",
            "chestra.plugins.start",
            "chestra.plugins.changed",
        ]:
            logger = logging.getLogger(logger_name)
            logger.setLevel(logging.ERROR)
            logger.propagate = False

    if args.plantuml:
        output_file = None if args.plantuml is True else args.plantuml
        generate_plantuml(args.workflow, output_file)
        sys.exit(0)

    orchestrator = TaskOrchestrator()
    orchestrator.load_workflow(args.workflow)
    orchestrator.run()
