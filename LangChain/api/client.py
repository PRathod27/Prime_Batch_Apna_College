import requests as rs
import streamlit as st

def get_genai_response(input_text):
    response = rs.post(
        'http://localhost:8000/essay/invoke',
        json={'input': {'text': input_text}},
    )

    return response.json()['output']

st.title('LangChain Demo wit API')
input_text = st.text_input("Write an essay on")


if input_text:
    st.markdown(get_genai_response(input_text))
