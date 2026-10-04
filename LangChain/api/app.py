from fastapi import FastAPI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langserve import add_routes
import uvicorn as uv
import os
# from langchain_community.llms import Ollama
from dotenv import load_dotenv
load_dotenv()

GOOGLE_GEMINI_API_KEY = os.getenv('GOOGLE_API_KEY')

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple API server"
)


model = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    api_key = GOOGLE_GEMINI_API_KEY,
    temperature = 1.0,
    max_retries=3
)

prompt = ChatPromptTemplate.from_messages([
    ("human", "{text}"),
])


add_routes(
    app,
    prompt | model | StrOutputParser(),
    path="/essay"
)

if __name__=="__main__":
    uv.run(app, host = "localhost", port=8000)
