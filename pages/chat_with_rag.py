import streamlit as st
from utils.rag import answer_question
import os


st.set_page_config(page_title='Chat with Dozinator', page_icon='📚', layout="wide")


def welcome_page():
    st.title("Welcome to the DOZinator")
    list_databases = [d for d in os.listdir("data") if os.path.isdir(os.path.join("data", d))]
    db_path = st.selectbox(
        "Which database would you like to interact with:",
        list_databases
        )
    chat(f"data/{db_path}")


def chat(db_path: str):
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Ask your question"):
        add_chat_message(user='user', text=prompt)
        
        response = answer_question(prompt, db_path=db_path)

        add_chat_message(user='assistant', text=response)


def add_chat_message(user: str, text: str):
    # Display assistant response in chat message container
    st.chat_message(user).markdown(text)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": user, "content": text})


if __name__ == "__main__":
    welcome_page()