from smolagents.agents import ToolCallingAgent
from smolagents import tool, LiteLLMModel
from typing import Optional

from smolagents_tools import sa_list_directory
from smolagents_tools import summarize_directory
from smolagents_tools import read_file_contents

model = LiteLLMModel(
    model_id="ollama_chat/llama3.2:latest",
    api_base="http://localhost:11434", # replace with remote open-ai compatible server if necessary
    api_key="your-api-key" # replace with API key if necessary
)

agent = ToolCallingAgent(tools=[sa_list_directory,
                                summarize_directory,
                                read_file_contents],
                         model=model)

#print(agent.run("What are the files in the current directory? Describe the current directory"))

print(agent.run("List the Python programs in the current directory, and then tell me which Python programs in the current directory evaluate the performance of LLMs?"))