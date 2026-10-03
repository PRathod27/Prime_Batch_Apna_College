from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_typesafe import Noul, Score, Choice, TypeSafeClassifier
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.grph import StateGraph, START, END
from typing import Literal
from pydantic import BaseModel

MOVIES = {
    "Jawan":{"about":"Hindi action thriller", "time":"7:00 PM", "price":700, "seats":40},
    "Interstellar" :{"about":"English space sci-fi", "time":"9:30 PM", "price":300, "seats":30},
    "3 Idiots" : {"about":"Comedic movie with real insrpiration","time":"9:00 PM","price":250,"seats": 10}
}

classifier = TypeSafeClassifier()

class BookingState(BaseModel):
    message:str="",
    intent:str="general",
    confidence : float = 0,
    reply: str=""


def jev_router(state:BookingState) -> BookingState:
    INTENT = Choice(
        instructions="What does the user want to do?",
        criteria = {
            "list_movies":"See which movies are showing show times, price or list all the movies",
            "book_movie":"Book or buy new movie ticket",
            "cancel_movie":"Cancel an existing booking or get a refund of the payment",
            "help":"Anything else, greetings or not clear"
        }
    )


    res = classifier.invoke({
        "state":state.message,
        "questions":{
            "intent":INTENT,
        }
    })

    intent = res.answers['intent'].choice
    print(f"Jev Router : {intent}")
    state.intent = intent.choice
    state.confidence = intent.confidence

    return state

def router_node(state:BookingState) -> Literal['list_movies','book_movie','cancel_movie','help']:

    if state.confidence < 0.7:
        return "help"

    return state.intent

# def list_movies(state:BookingState):
