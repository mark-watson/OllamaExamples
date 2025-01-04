from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_ollama import ChatOllama
import json
from pprint import pprint

@tool
def search(query: str):
    """Use DuckDuckGo to run a web search."""
    ddg_search = DuckDuckGoSearchRun()  # Changed from DuckDuckGoSearchTool
    return ddg_search.run(query)


# Replace ChatVertexAI with Ollama
model = ChatOllama(model="llama3.2:latest")
tools = [search]

query = "Where does Mark Watson (author, AI Common Lisp Semantic Web consultant) live? Name thew city where Mark Watson lives."

agent = create_react_agent(model, tools)
agent_input = {"messages": [("human", query)]}

for s in agent.stream(agent_input, stream_mode="values"):
    message = s["messages"][-1]
    if isinstance(message, tuple):
        print(f"\nTuple message: {message}")
    else:
        print("\nMessage content:")
        print(message.content)

        # Try to parse tool calls from JSON responses
        try:
            content = json.loads(message.content)
            if "name" in content and content["name"] == "search":
                search_result = search(content["parameters"]["query"])
                print(f"\nSearch result: {search_result}")
        except json.JSONDecodeError:
            pass