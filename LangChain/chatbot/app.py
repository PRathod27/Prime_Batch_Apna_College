import os
from dotenv import load_dotenv
import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

GOOGLE_GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
## Langmith tracking
os.environ["LANGSMITH_TRACING"]="true"
os.environ["LANGSMITH_API_KEY"]=os.getenv("LANGSMITH_API_KEY")

# 1. Initialize model with a valid model name
model = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    api_key=GOOGLE_GEMINI_API_KEY,
    temperature=1.0,
    max_retries=3,
)

# 2. Add the dynamic variable {text} to the prompt
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful assistant that translates English to French. Translate the user sentence.",
    ),
    ("human", "{text}"),
])

output_parser = StrOutputParser()

# 3. Build the LCEL chain
chain = prompt | model | output_parser

# Streamlit UI
st.title("LangChain Demo With Gemini API")
input_text = st.text_input("Enter the sentence to translate:")

# 4. Pass the matching key 'text' to invoke()
if input_text:
    response = chain.invoke({"text": input_text})
    st.write(response)