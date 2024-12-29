from typing import Dict, Any

import ollama
from tool_summarize_text import summarize_text
from tool_web_search import brave_search_text
from tool_sqlite import SQLiteTool
from tool_judge_results import judge_results  # Import your custom tool


class LLMAgent:
    """
    An agent that utilizes Ollama and your custom tools for various tasks.
    """

    def __init__(self, model_name="llama3.2:latest"):
        self.llm = ollama.Client()
        self.summarizer = summarize_text
        self.web_searcher = brave_search_text
        self.sqlite_tool = SQLiteTool()

    def judge_results(self, prompt: str, response: str) -> Dict[str, str]:
        """
        Uses the provided `judge_results` tool to judge the accuracy
        of the generated response for the prompt.

        This function replaces the previous judge_results functionality.
        """
        return judge_results(prompt, response)

    def search_web(self, query: str) -> str:
        """
        Uses the web_searcher tool to search the web for the given query.
        """
        return self.web_searcher(query)

    def summarize_text(self, text: str) -> str:
        """
        Uses the summarizer tool to summarize the provided text.
        """
        return self.summarizer(text)

    def query_database(self, query: str) -> List[tuple]:
        """
        Uses the sqlite_tool to execute a SQL query on the database.
        """
        return self.sqlite_tool.execute_query(query)

    def run_OLD(self, prompt: str) -> Dict[str, Any]:
        """
        Executes the given prompt and returns a dictionary containing results
        from potentially multiple tools.

        Here, you can extend the functionality based on the prompt or utilize Ollama
        to understand the user's intent and choose the appropriate tool.
        """
        response = self.llm.generate(model=self.model_name, prompt=prompt)
        judgement = self.judge_results(prompt, response.response)

        # Example: Check if the prompt involves searching the web
        if "search" in prompt.lower():
            web_results = self.search_web(prompt)
            return {
                "response": response.response,
                "judgement": judgement,
                "web_results": web_results,
            }
        # Example: Check if the prompt involves summarizing text
        elif "summarize" in prompt.lower():
            summary = self.summarize_text(response.response)
            return {
                "response": summary,
                "judgement": judgement,
            }
        # Example: Check if the prompt involves querying the database
        elif "database" in prompt.lower() and self.sqlite_tool:
            try:
                query_results = self.query_database(response.response)
                return {"query_results": query_results, "judgement": judgement}
            except Exception as e:
                return {"error": f"Database query failed: {str(e)}", "judgement": "E"}
        else:
            return {"response": response.response, "judgement": judgement}

    def run(self, prompt: str, max_retries: int = 3) -> Dict[str, Any]:
        """
        Executes the given prompt with result judging and retries.
        """
        for attempt in range(max_retries):
            response = self.llm.generate(model=self.model_name, prompt=prompt)
            judgement = self.judge_results(prompt, response.response)

            if judgement['judgement'] == 'Y':
                # Process based on prompt type (search, summarize, database, etc.)
                if "search" in prompt.lower():
                    web_results = self.search_web(prompt)
                    return {
                        "response": response.response,
                        "judgement": judgement,
                        "web_results": web_results,
                    }
                elif "summarize" in prompt.lower():
                    summary = self.summarize_text(response.response)
                    return {
                        "response": summary,
                        "judgement": judgement,
                    }
                elif "database" in prompt.lower() and self.sqlite_tool:
                    try:
                        query_results = self.query_database(response.response)
                        return {"query_results": query_results, "judgement": judgement}
                    except Exception as e:
                        return {"error": f"Database query failed: {str(e)}", "judgement": "E"}
                else:
                    return {"response": response.response, "judgement": judgement}
            else:
                print(f"Attempt {attempt + 1} failed judgement. Retrying...")
                print(f"Reason: {judgement['reasoning']}") # print out the reason for failing the test
        return {"error": f"Failed after {max_retries} attempts.", "judgement": judgement}


if __name__ == "__main__":
    agent = LLMAgent()
    prompt = "What is the capital of France?"
    results = agent.run(prompt)
    print(results)

    # Example with database query (assuming a table named 'capitals')
    prompt = "Find the capital of Germany from the database"
