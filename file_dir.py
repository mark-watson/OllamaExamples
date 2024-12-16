"""
File Directory Module
Provides functions for listing files in the current directory
"""

from typing import Dict, List, Any
from pathlib import Path
import os


def list_directory(pattern: str = "*", list_dots=None) -> Dict[str, Any]:
    """
    Lists files and directories in the current working directory

    Args:
        pattern (str): Glob pattern for filtering files (default: "*")

    Returns:
        string with directory name, followed by list of files in the directory
    """
    try:
        current_dir = Path.cwd()
        files = list(current_dir.glob(pattern))

        # Convert Path objects to strings and sort
        file_list = sorted([str(f.name) for f in files])

        file_list = [file for file in file_list if not file.endswith("~")]
        if not list_dots:
            file_list = [file for file in file_list if not file.startswith(".")]

        return f"Contents of current directory: [{', '.join(file_list)}]"

    except Exception as e:
        return f"Error listing directory: {str(e)}"


# Function metadata for Ollama integration
list_directory.metadata = {
    "name": "list_directory",
    "description": "Lists files and directories in the current working directory",
    "parameters": {"pattern": 'Glob pattern for filtering files (default: "*")'},
}

# Export the function
__all__ = ["list_directory"]
