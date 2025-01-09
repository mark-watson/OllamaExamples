from smolagents.agents import ToolCallingAgent
from smolagents import LiteLLMModel

from smolagents_tools import sa_list_directory
from smolagents_tools import sa_summarize_directory
from smolagents_tools import sa_read_file_contents


model = LiteLLMModel(
    model_id="ollama_chat/llama3.2:latest",
    api_base="http://localhost:11434", # replace with remote open-ai compatible server if necessary
    api_key="your-api-key" # replace with API key if necessary
)
model.set_verbose=True

agent = ToolCallingAgent(tools=[sa_list_directory,
                                sa_summarize_directory,
                                sa_read_file_contents],
                         model=model,
                         add_base_tools=False) # set to True to use built-in tools

#print(agent.run("List the Python programs in the current directory, and then tell me which Python programs in the current directory evaluate the performance of LLMs?\n\n"))

print(agent.run("What are the files in the current directory? Describe the current directory"))

#print(agent.run("Read the text in the file 'data/economics.txt' file and then summarize this text."))
