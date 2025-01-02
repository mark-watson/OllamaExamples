from smolagents.agents import ToolCallingAgent
from smolagents import tool, LiteLLMModel
from typing import Optional

from smolagents_tools import sa_list_directory
from tool_file_contents import read_file_contents
from tool_web_search import uri_to_markdown

model = LiteLLMModel(
    model_id="ollama_chat/llama3.2:latest",
    api_base="http://localhost:11434", # replace with remote open-ai compatible server if necessary
    api_key="your-api-key" # replace with API key if necessary
)

agent = ToolCallingAgent(tools=[sa_list_directory], model=model)

print(agent.run("What are the files in the current directory?"))

