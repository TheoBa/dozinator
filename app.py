import streamlit as st
from utils.create_database import generate_data_store
from utils.rag import answer_question, get_context

st.set_page_config(page_title='DOZinator', page_icon='📚', layout="wide")


def welcome_page():
    st.title("Welcome to the DOZinator")
    st.button('Create vector database based on your documents', on_click=generate_data_store)
    chat()


def chat():
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Ask your physics related question"):
        add_chat_message(user='user', text=prompt)
        
        response = answer_question(prompt)

        add_chat_message(user='assistant', text=response)


def add_chat_message(user: str, text: str):
    # Display assistant response in chat message container
    st.chat_message(user).markdown(text)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": user, "content": text})


if __name__ == "__main__":
    welcome_page()