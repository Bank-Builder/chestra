#!/usr/bin/env python3
"""
Generic Python project for shell operations and file management.
"""

import logging
import os
import pathlib
import shutil
import subprocess
from typing import List, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ShellOperations:
    """Handles shell command execution and file operations."""

    def __init__(self, working_dir: Optional[str] = None):
        """
        Initialize ShellOperations.
        
        Args:
            working_dir: Directory to run commands in (defaults to current)
        """
        self.working_dir = working_dir or os.getcwd()

    def run_command(self, command: str, capture_output: bool = True) -> Tuple[int, str, str]:
        """
        Execute a shell command.
        
        Args:
            command: Command to execute
            capture_output: Whether to capture stdout/stderr
            
        Returns:
            Tuple of (return_code, stdout, stderr)
        """
        try:
            logger.info(f"Executing command: {command}")
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.working_dir,
                capture_output=capture_output,
                text=True
            )
            return result.returncode, result.stdout, result.stderr
        except Exception as e:
            logger.error(f"Error executing command: {e}")
            return -1, "", str(e)

    def list_files(self, directory: str = None) -> List[str]:
        """
        List files in a directory.
        
        Args:
            directory: Directory to list (defaults to working_dir)
            
        Returns:
            List of file names
        """
        dir_path = directory or self.working_dir
        try:
            files = os.listdir(dir_path)
            logger.info(f"Found {len(files)} files in {dir_path}")
            return files
        except Exception as e:
            logger.error(f"Error listing files: {e}")
            return []

    def copy_file(self, source: str, destination: str) -> bool:
        """
        Copy a file from source to destination.
        
        Args:
            source: Source file path
            destination: Destination file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            shutil.copy2(source, destination)
            logger.info(f"Copied {source} to {destination}")
            return True
        except Exception as e:
            logger.error(f"Error copying file: {e}")
            return False

    def move_file(self, source: str, destination: str) -> bool:
        """
        Move a file from source to destination.
        
        Args:
            source: Source file path
            destination: Destination file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            shutil.move(source, destination)
            logger.info(f"Moved {source} to {destination}")
            return True
        except Exception as e:
            logger.error(f"Error moving file: {e}")
            return False

    def create_directory(self, directory: str) -> bool:
        """
        Create a directory.
        
        Args:
            directory: Directory path to create
            
        Returns:
            True if successful, False otherwise
        """
        try:
            pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {directory}")
            return True
        except Exception as e:
            logger.error(f"Error creating directory: {e}")
            return False

    def delete_file(self, file_path: str) -> bool:
        """
        Delete a file.
        
        Args:
            file_path: Path to file to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            os.remove(file_path)
            logger.info(f"Deleted file: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error deleting file: {e}")
            return False

    def file_exists(self, file_path: str) -> bool:
        """
        Check if a file exists.
        
        Args:
            file_path: Path to check
            
        Returns:
            True if file exists, False otherwise
        """
        return os.path.exists(file_path)


def main():
    """Main function demonstrating usage."""
    # Initialize shell operations
    shell_ops = ShellOperations()

    # Example: List current directory files
    print("Files in current directory:")
    files = shell_ops.list_files()
    for file in files:
        print(f"  - {file}")

    # Example: Run a simple command
    print("\nRunning 'ls -la' command:")
    return_code, stdout, stderr = shell_ops.run_command("ls -la")
    if return_code == 0:
        print("Output:")
        print(stdout)
    else:
        print(f"Error: {stderr}")

    # Example: Create a test directory
    test_dir = "test_directory"
    if shell_ops.create_directory(test_dir):
        print(f"\nCreated test directory: {test_dir}")

        # Create a test file
        test_file = os.path.join(test_dir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("This is a test file\n")

        # Copy the file
        backup_file = os.path.join(test_dir, "test_backup.txt")
        if shell_ops.copy_file(test_file, backup_file):
            print(f"Created backup: {backup_file}")

        # List files in test directory
        print(f"\nFiles in {test_dir}:")
        test_files = shell_ops.list_files(test_dir)
        for file in test_files:
            print(f"  - {file}")

        # Clean up
        shell_ops.delete_file(test_file)
        shell_ops.delete_file(backup_file)
        os.rmdir(test_dir)
        print(f"\nCleaned up {test_dir}")


if __name__ == "__main__":
    main()
