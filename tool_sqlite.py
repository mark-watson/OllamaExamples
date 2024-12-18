import sqlite3
import json
from typing import Dict, Any, List, Optional
import ollama
from functools import wraps
import re

# Add comment for creating sqlite table using command line tool
class SQLiteTool:
    def __init__(self, default_db: str = "test.db"):
        print(f"{default_db=}")
        try:  # attempt to create the database if it does not exist
            conn = sqlite3.connect(default_db)
            print(f"{conn=}")
            cursor = conn.cursor()

            example_table = """
             CREATE TABLE IF NOT EXISTS example (
                 id INTEGER PRIMARY KEY,
                 name TEXT,
                 value REAL
             );
             """
            cursor.execute(example_table)
            conn.commit()

        except Exception as e:
            print(e)

        self.default_db = default_db
        self.current_connection = None

    def connect(self, db_name: Optional[str] = None) -> None:
        """Connect to SQLite database"""
        db_to_use = db_name or self.default_db
        self.current_connection = sqlite3.connect(db_to_use)

    def close(self) -> None:
        """Close the current database connection"""
        if self.current_connection:
            self.current_connection.close()
            self.current_connection = None

    def ensure_connection(func):
        """Decorator to ensure database connection exists"""
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self.current_connection:
                self.connect()
            return func(self, *args, **kwargs)
        return wrapper

    @ensure_connection
    def get_tables(self) -> List[str]:
        """Get list of tables in the database"""
        cursor = self.current_connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return [table[0] for table in cursor.fetchall()]

    @ensure_connection
    def get_table_schema(self, table_name: str) -> List[tuple]:
        """Get schema for a specific table"""
        cursor = self.current_connection.cursor()
        cursor.execute(f"PRAGMA table_info({table_name});")
        return cursor.fetchall()

    @ensure_connection
    def execute_query(self, query: str) -> List[tuple]:
        """Execute a SQL query and return results"""
        cursor = self.current_connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()

class OllamaFunctionCaller:
    def __init__(self, model: str = "llama3.2:latest"):
        self.model = model
        self.sqlite_tool = SQLiteTool()
        print(f"self.sqlite_tool=")
        self.function_definitions = self._get_function_definitions()

    def _get_function_definitions(self) -> Dict:
        """Define available functions and their parameters"""
        return {
            "query_database": {
                "description": "Execute a SQL query on the database",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The SQL query to execute"
                        },
                        "database": {
                            "type": "string",
                            "description": "Database name (optional)"
                        }
                    },
                    "required": ["query"]
                }
            },
            "list_tables": {
                "description": "List all tables in the database",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "database": {
                            "type": "string",
                            "description": "Database name (optional)"
                        }
                    }
                }
            }
        }

    def _generate_prompt(self, user_input: str) -> str:
        """Generate a prompt for Ollama with function definitions"""
        return f"""You are a SQL assistant. Based on the user's request, generate a JSON response that calls the appropriate function.
Available functions: {json.dumps(self.function_definitions, indent=2)}

User request: {user_input}

Respond with a JSON object containing:
- "function": The function name to call
- "parameters": The parameters for the function

Response:"""

    def _parse_ollama_response(self, response: str) -> Dict[str, Any]:
        """Parse Ollama's response to extract function call details"""
        try:
            # Find JSON-like content in the response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            raise ValueError("No valid JSON found in response")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON in response")

    def process_request(self, user_input: str) -> Any:
        """Process a natural language request and execute the appropriate function"""
        prompt = self._generate_prompt(user_input)

        # Get response from Ollama
        response = ollama.generate(model=self.model, prompt=prompt)

        # Parse the response
        function_call = self._parse_ollama_response(response.response)

        # Execute the appropriate function
        if function_call["function"] == "query_database":
            db_name = function_call["parameters"].get("database")
            if db_name:
                self.sqlite_tool.connect(db_name)
            return self.sqlite_tool.execute_query(function_call["parameters"]["query"])

        elif function_call["function"] == "list_tables":
            db_name = function_call["parameters"].get("database")
            if db_name:
                self.sqlite_tool.connect(db_name)
            return self.sqlite_tool.get_tables()

        else:
            raise ValueError(f"Unknown function: {function_call['function']}")

def main():
    # Example usage
    function_caller = OllamaFunctionCaller()

    # Example queries
    queries = [
        "Show me all tables in the database",
        "Get all users from the users table",
        "What are the top 5 products by price?"
    ]

    for query in queries:
        try:
            print(f"\nQuery: {query}")
            result = function_caller.process_request(query)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error processing query: {str(e)}")

if __name__ == "__main__":
    main()
