import kuzu
from langchain.chains import KuzuQAChain
from langchain_community.graphs import KuzuGraph
from langchain_ollama.llms import OllamaLLM

db = kuzu.Database("test_db")
conn = kuzu.Connection(db)

# Create two tables and a relation: Movie, Person, ActedIn
conn.execute("CREATE NODE TABLE Movie (name STRING, PRIMARY KEY(name))")
conn.execute(
    "CREATE NODE TABLE Person (name STRING, birthDate STRING, PRIMARY KEY(name))"
)
conn.execute("CREATE REL TABLE ActedIn (FROM Person TO Movie)")
conn.execute("CREATE (:Person {name: 'Al Pacino', birthDate: '1940-04-25'})")
conn.execute("CREATE (:Person {name: 'Robert De Niro', birthDate: '1943-08-17'})")
conn.execute("CREATE (:Movie {name: 'The Godfather'})")
conn.execute("CREATE (:Movie {name: 'The Godfather: Part II'})")
conn.execute(
    "CREATE (:Movie {name: 'The Godfather Coda: The Death of Michael Corleone'})"
)
conn.execute(
    "MATCH (p:Person), (m:Movie) WHERE p.name = 'Al Pacino' AND m.name = 'The Godfather' CREATE (p)-[:ActedIn]->(m)"
)
conn.execute(
    "MATCH (p:Person), (m:Movie) WHERE p.name = 'Al Pacino' AND m.name = 'The Godfather: Part II' CREATE (p)-[:ActedIn]->(m)"
)
conn.execute(
    "MATCH (p:Person), (m:Movie) WHERE p.name = 'Al Pacino' AND m.name = 'The Godfather Coda: The Death of Michael Corleone' CREATE (p)-[:ActedIn]->(m)"
)
conn.execute(
    "MATCH (p:Person), (m:Movie) WHERE p.name = 'Robert De Niro' AND m.name = 'The Godfather: Part II' CREATE (p)-[:ActedIn]->(m)"
)

graph = KuzuGraph(db, allow_dangerous_requests=True)

# Create a chain
chain = KuzuQAChain.from_llm(
    llm=OllamaLLM(model="qwen2.5-coder:14b"),
    graph=graph,
    verbose=True,
    allow_dangerous_requests=True,
)

print(graph.get_schema)

# Ask two questions
chain.invoke("Who acted in The Godfather: Part II?")
chain.invoke("Robert De Niro played in which movies?")
