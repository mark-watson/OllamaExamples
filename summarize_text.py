"""
Summarize text
"""

from typing import Optional, Dict, Any
from pathlib import Path
import json

from ollama import chat
from ollama import ChatResponse


def summarize_text(text: str, context: str = "", encoding: str = "utf-8") -> str:
    """
    Summarizes text

    Args:
        text (str): text to summarize
        context (str): another tool's output can at the application layer can be used set the context for this tool.

    Returns:
        a string os summarized text
    """
    print(f"\n\n**** summarize input text:\n\n{text}\n\n")
    prompt0 = "You are an expert at summarizing an input string. The only thing you return is the summarized text."
    if len(text.strip()) < 50:
        text = context
        print(f"\n* * modified text (context):\n{text}\n")
    else:
        if len(context) > 10:
            prompt0 += "\n" + context
    summary: ChatResponse = chat(
        model="llama3.2:latest",
        messages=[
            {
                "role": "system",
                "content": prompt0,
            },
            {"role": "user", "content": text},
        ],
    )
    return summary["message"]["content"]


# Function metadata for Ollama integration
summarize_text.metadata = {
    "name": "summarize_text",
    "description": "Summarizes input text",
    "parameters": {"text": "string of text to summarize"},
}

# Export the functions
__all__ = ["summarize_text"]
