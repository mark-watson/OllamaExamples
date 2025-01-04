"""
Wrapper for book example tools for smloagents compatibility
"""

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