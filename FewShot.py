from langchain_community.llms import LlamaCpp
from langchain_community.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
from langchain.prompts import PromptTemplate

llm = LlamaCpp(
    model_path="/home/aryan/Desktop/Models/Meta-Llama-3.1-8B-Instruct-IQ3_M.gguf",
    # n_gpu_layers=-1, # For GPU acceleration
    # seed=1337, # For reproducibility
    # n_ctx=2048, # Adjust context window if necessary
)

graph = Neo4jGraph(
    url="bolt://localhost:7687/",
    username="neo4j",
    password="YPgqUvMmeP23FsL",
)

CYPHER_GENERATION_TEMPLATE = """
You are an expert Neo4j Developer tasked with translating natural language questions into Cypher queries. 

The database schema includes nodes and relationships structured as follows:

Node properties:
-Deity [name: STRING]
-Bhajan [text: STRING]
-Meaning [text: STRING

Relationship properties:

The relationships:
(:Bhajan)-[:HAS_MEANING]->(:Meaning)
(:Bhajan)-[:DEDICATED_TO]->(:Deity)

Please convert the user's question into an optimized Cypher query.

For example:
- User Question: "Find all bhajans dedicated to Ganesha."
  Cypher Query: MATCH (b:Bhajan)-[:DEDICATED_TO]->(d:Deity {name: 'Ganesha'}) RETURN b.text AS Bhajan, d.name AS Deity;

- User Question: "Give me a random Ganesha bhajan."
  Cypher Query: MATCH (b:Bhajan)-[:DEDICATED_TO]->(d:Deity {name: 'Ganesha'}) RETURN b.text AS Bhajan ORDER BY rand() LIMIT 1;

- User Question: "Display all ganesha bajanas."
  Cypher Query: MATCH (b:Bhajan)-[:DEDICATED_TO]->(d:Deity {name: 'Ganesha'}) RETURN b.text AS Bhajan, d.name AS Deity;

- User Question: "Find bhajans with the word 'Parvati' in the text, diplay the name of the deity also."
  Cypher Query: MATCH (b:Bhajan)-[:DEDICATED_TO]->(d:Deity) WHERE b.text CONTAINS 'Parvati' RETURN b.text AS Bhajan, d.name AS Deity;

- User Question: "Find a Ganesha bhajan with the word 'Amba' in the text."
  Cypher Query: MATCH (b:Bhajan)-[:DEDICATED_TO]->(d:Deity {name: 'Ganesha'}) WHERE b.text CONTAINS 'Amba' RETURN b.text AS Bhajan, d.name AS Deity;

  Schema: {schema}
  Question: {question}

"""

cypher_generation_prompt = PromptTemplate(
    template=CYPHER_GENERATION_TEMPLATE,
    input_variables=["schema", "question"],
)

cypher_chain = GraphCypherQAChain.from_llm(
    llm,
    graph=graph,
    cypher_prompt=cypher_generation_prompt,
    verbose=True,
    validate_cypher=True,
)

cypher_chain.invoke({"query": "give a krishna bhajan."})

# def ask_question(query):
#     result = cypher_chain.invoke({"query": query})
#     return result
  
# ask_question("give a krishna bhajan.")


# cypher
# MATCH (p:Person)-[r:WORKS_AT]->(o:Organization) WHERE o.name = "OpenAI" RETURN p;

# Full Context:
# [{'p': {'name': 'Alice', 'id': '1'}}]
# Llama.generate: prefix-match hit

# llama_print_timings:        load time =    3348.39 ms
# llama_print_timings:      sample time =     496.66 ms /   256 runs   (    1.94 ms per token,   515.45 tokens per second)
# llama_print_timings: prompt eval time =   69892.21 ms /   181 tokens (  386.14 ms per token,     2.59 tokens per second)
# llama_print_timings:        eval time =  202861.96 ms /   255 runs   (  795.54 ms per token,     1.26 tokens per second)
# llama_print_timings:       total time =  273523.62 ms /   436 tokens

# > Finished chain.