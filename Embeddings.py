from langchain_community.embeddings import LlamaCppEmbeddings

llama = LlamaCppEmbeddings(model_path="/home/aryan/Desktop/Models/Meta-Llama-3.1-8B-Instruct-Q8_0.gguf")
text = "This is a test document."
query_result = llama.embed_query(text)
print(query_result)
# doc_result = llama.embed_documents([text])