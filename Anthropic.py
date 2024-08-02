import os

os.environ["ANTHROPIC_API_KEY"] = "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"

from langchain_anthropic import AnthropicLLM
from langchain_core.prompts import PromptTemplate

template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate.from_template(template)

model = AnthropicLLM(model="claude-2.1")

chain = prompt | model

chain.invoke({"question": "What is LangChain?"})