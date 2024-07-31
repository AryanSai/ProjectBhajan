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
You are an expert Neo4j Developer translating user questions into Cypher to answer questions.
Convert the user's question based on the schema.

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
    verbose=True
)

# cypher_chain.invoke({"query": "Find all persons who work at OpenAI"})
cypher_chain.invoke({"query": "Find a Ganesha bhajan with the word 'Amba' in it."})
# print("Answer: ", result)

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