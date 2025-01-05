"""
Wrapper for book example tools for smloagents compatibility
"""
from pathlib import Path

from smolagents import tool, LiteLLMModel
from typing import Optional
from pprint import pprint

from tool_file_dir import list_directory


@tool
def sa_list_directory(list_dots: Optional[bool]=None) -> str:
    """
    Lists files and directories in the current working directory

    Args:
        list_dots: optional boolean (if true, include dot files)

    Returns:
        string with directory name, followed by list of files in the directory
    """
    lst = list_directory()
    pprint(lst)
    return lst

@tool
def read_file_contents(file_path: str) -> str:
    """
    Reads contents from a file and returns the text

    Args:
        file_path: Path to the file to read

    Returns:
        Contents of the file as a string
    """
    try:
        path = Path(file_path)
        if not path.exists():
            return f"File not found: {file_path}"

        with path.open("r", encoding="utf-8") as f:
            content = f.read()
            return f"Contents of file '{file_path}' is:\n{content}\n"

    except Exception as e:
        return f"Error reading file '{file_path}' is: {str(e)}"

@tool
def summarize_directory() -> str:
    """
    Summarizes the files and directories in the current working directory

    Args:
        None

    Returns:
        string with directory name, followed by summary of files in the directory
    """
    lst = list_directory()
    num_files = len(lst)
    num_dirs = len([x for x in lst if x[1] == 'directory'])
    num_files = num_files - num_dirs
    return f"Current directory contains {num_files} files and {num_dirs} directories."

