import streamlit as st
import BhajanLLM

st.title("Project Bhajan")
st.write("Welcome to Project Bhajan!")

query = st.text_input("Ask me something: ", placeholder="Type here...")

if st.button("Submit"):
    st.write(f"Hello, {query}!")

BhajanLLM.ask_question(query)