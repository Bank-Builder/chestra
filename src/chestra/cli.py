import argparse

from .orchestrator import TaskOrchestrator


def main():
    parser = argparse.ArgumentParser(description="Chestra Orchestrator CLI")
    parser.add_argument('workflow', help='Path to workflow YAML file')
    args = parser.parse_args()
    orchestrator = TaskOrchestrator()
    orchestrator.load_workflow(args.workflow)
    orchestrator.run()
