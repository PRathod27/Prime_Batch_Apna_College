from dotenv import load_dotenv
load_dotenv()

import os
from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_typesafe import Noul, Choice, Score, TypeSafeClassifier
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, Field
from typing import Literal

MOVIES = {
    "Jawan":        {"about": "Hindi action thriller", "time": "7:00 PM", "price": 250, "seats": 40},
    "Interstellar": {"about": "English space sci-fi",  "time": "9:30 PM", "price": 300, "seats": 25},
    "3 Idiots":     {"about": "Hindi college comedy",  "time": "4:00 PM", "price": 200, "seats": 10},
}

classifier = TypeSafeClassifier(api_key=os.getenv("TYPE_SAFE_API_KEY"))
llm = ChatGroq(model=os.getenv("GROQ_AI_MODEL"), api_key=os.getenv("GROQ_API_KEY"))


class BookingState(BaseModel):
    message:str = ""
    intent:str = "general"
    confidence:float = 0
    reply:str = ""


class MovieDetail(BaseModel):
    name:str = Field(description="Movie name")
    seats: int = Field(description="Number of seates user wants to book")


def jev_router(state:BookingState) -> BookingState:
    INTENT = Choice(
        instructions="What does the user want to do ?",
        criteria={
            "list_movies":"See which movies are showing, show times, price or list all the movies",
            "book_movie":"Book or buy new movie ticket",
            "cancel_movie":"Cancel an existing booking or get a refund of the payment",
            "help":"Anything else, greetings  or not clear"
        }
    )

    res = classifier.invoke({
        "state":state.message,
        "questions": {
            "intent":INTENT
        }
    })

    intent = res.answers["intent"]
    print(f"Jev Router: {intent.choice}")
    state.intent = intent.choice
    state.confidence = intent.confidence

    return state


def router_node(state:BookingState) -> Literal["list_movies", "book_movie", "cancel_movie", "help"]:
    if state.confidence < 0.7:
        return "help"

    return state.intent


def list_movies(state:BookingState) -> BookingState:
    allMovies = str(MOVIES)
    res = llm.invoke(f"""
                        Please answer for the user question based on the provided context.
                        Question " {state.message},
                        Context: {allMovies}
                """)

    state.reply = res.content
    return state



def book_movie(state:BookingState) -> BookingState:
    detail:MovieDetail = llm.with_structured_output(MovieDetail).invoke(state.message)
    selectedMovie = None
    for movieName in MOVIES.keys():
        if detail.name.lower() == movieName.lower():
            selectedMovie = MOVIES.get(movieName)
            break

    if not selectedMovie:
        state.reply =  "Movie not available"
        return state


    if selectedMovie.get("seats") < detail.seats:
        state.reply = f"Seats are not available, only {selectedMovie.get("seats")} seats available"
        return state


    state.reply = "Movie Booked Successfully"
    return state



def cancel_movie(state:BookingState) -> BookingState:
    state.reply = "Movie Canceled Successfully"
    return state



def help(state:BookingState) -> BookingState:
    res = llm.invoke(f"Please answer for user question "
    f"if you know, and if you dont know then just say 'I am not sure..' Question: {state.message}")

    state.reply = res.content
    return state


graph = StateGraph(BookingState)


# ["list_movies", "book_movie", "cancel_movie", "help"]
graph.add_node("jev_router", jev_router)
graph.add_node("list_movies", list_movies)
graph.add_node("book_movie", book_movie)
graph.add_node("cancel_movie", cancel_movie)
graph.add_node("help", help)

graph.add_edge(START, "jev_router")
graph.add_conditional_edges("jev_router", router_node)

graph.add_edge("list_movies", END)
graph.add_edge("book_movie", END)
graph.add_edge("cancel_movie", END)
graph.add_edge("help", END)

final_graph = graph.compile()