"""
Judge results from LLM generation from prompts
"""

from typing import Optional, Dict, Any
from pathlib import Path
import json
import re
from pprint import pprint

import ollama

client = ollama.Client()

def judge_results(original_prompt: str, llm_gen_results: str) -> Dict[str, str]:
    """
    Takes an original prompt to a LLM and the output results

    Args:
        original_prompt (str): original prompt to a LLM
        llm_gen_results (str): output from the LLM that this function judges for accuracy

    Returns:
        result: str: string that is one character with one of these values:
            - 'B': Bad result
            - 'G': A Good result
    """
    try:
        messages = [
            {"role": "system", "content": "Always judge this output for correctness."},
            {"role": "user", "content": f"Evaluate this output:\n\n{llm_gen_results}\n\nfor this prompt:\n\n{original_prompt}\n\nAnswer Y or N, followed by your reason. Just judge correctness of the initial output and if the initial output is incorrect don't print the correct solution. Double check your work"},
        ]

        response = client.chat(
            model="qwen2.5-coder:14b", # "llama3.2:latest",
            messages=messages,
        )

        r = response.message.content.strip()
        print(f"\n\noriginal COT response:\n\n{r}\n\n")

        # next two lines only for marco-o1 chain of thought model:
        # match = re.search(r'<Output>(.*?)</Output>', r, re.DOTALL)
        # r = match.group(1).strip() if match else None

        return {'judgement': r[0], 'reasoning': r[1:].strip()}

    except Exception as e:
        print(f"\n\n***** {e=}\n\n")
        return {'judgement': 'E', 'reasoning': str(e)}  # on any error, assign 'E' result
