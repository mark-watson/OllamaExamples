from langchain.llms import Ollama
from langchain.agents import initialize_agent, Tool
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.vectorstores import FAISS
from langchain.embeddings import OllamaEmbeddings
#from crewai import Agent, Task, Crew

class SingleAgent:
    """
    A single agent that can perform tasks using Ollama and LangChain.
    """
    def __init__(self, model_name="llama3.1", tools=None):
        self.llm = Ollama(model=model_name)
        self.tools = tools if tools else []
        self.agent = initialize_agent(self.tools, self.llm, agent="zero-shot-react-description")

    def run(self, query):
        """
        Execute a task using the agent.
        """
        return self.agent.run(query)

    def add_tool(self, tool):
        """
        Add a tool to the agent.
        """
        self.tools.append(tool)
        self.agent = initialize_agent(self.tools, self.llm, agent="zero-shot-react-description")


class MultiAgentSystem:
    """
    A multi-agent system that orchestrates tasks between multiple agents.
    """
    def __init__(self):
        self.agents = []
        self.tasks = []

    def add_agent(self, role, goal, model_name="llama3.1"):
        """
        Add an agent to the system.
        """
        agent = Agent(role=role, goal=goal, llm=f"ollama/{model_name}")
        self.agents.append(agent)

    def add_task(self, description, agent_role):
        """
        Add a task to the system.
        """
        agent = next((a for a in self.agents if a.role == agent_role), None)
        if agent:
            task = Task(description=description, agent=agent)
            self.tasks.append(task)

    def run(self):
        """
        Execute the multi-agent system.
        """
        crew = Crew(agents=self.agents, tasks=self.tasks)
        return crew.kickoff()


class RAGAgent:
    """
    An agent that uses Retrieval-Augmented Generation (RAG) for enhanced knowledge.
    """
    def __init__(self, model_name="llama3.1", document_path=None):
        self.llm = Ollama(model=model_name)
        self.document_path = document_path
        self.vectorstore = None
        if document_path:
            self._load_documents()

    def _load_documents(self):
        """
        Load documents into a vector store for retrieval.
        """
        loader = TextLoader(self.document_path)
        documents = loader.load()
        embeddings = OllamaEmbeddings(model="llama3.1")
        self.vectorstore = FAISS.from_documents(documents, embeddings)

    def run(self, query):
        """
        Execute a query using RAG.
        """
        if not self.vectorstore:
            raise ValueError("No documents loaded for retrieval.")
        qa_chain = RetrievalQA.from_chain_type(llm=self.llm, chain_type="stuff", retriever=self.vectorstore.as_retriever())
        return qa_chain.run(query)


# Example Usage
if __name__ == "__main__":
    # Single Agent Example
    def search_tool(query):
        # Placeholder for a search tool
        return f"Search results for: {query}"

    single_agent = SingleAgent(tools=[Tool(name="Search", func=search_tool, description="Search the web")])
    print(single_agent.run("What’s the latest news on AI?"))

    # Multi-Agent System Example
    multi_agent_system = MultiAgentSystem()
    multi_agent_system.add_agent(role="Researcher", goal="Find relevant information")
    multi_agent_system.add_agent(role="Writer", goal="Write a report")
    multi_agent_system.add_task(description="Research AI trends", agent_role="Researcher")
    multi_agent_system.add_task(description="Write a summary", agent_role="Writer")
    print(multi_agent_system.run())

    # RAG Agent Example
    rag_agent = RAGAgent(document_path="data/research_papers.txt")
    print(rag_agent.run("Summarize the key findings in the document."))

