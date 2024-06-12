import streamlit as st
from utils.rag import answer_question

# debug streamlit cloud
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

st.set_page_config(page_title='DOZinator', page_icon='📚', layout="wide")


def welcome_page():
    st.title("Welcome to Dozinator's front page")
    url = "https://github.com/TheoBa/dozinator"
    st.markdown("This personnal project is open source, see the repo on github: [link](%s)" % url)
    st.header("Pages description")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**App**")
        st.markdown("The front page you are currently on")
    with col2:
        st.markdown("**Upload files**")
        st.markdown("Upload your documents and create your own embedded database")
    with col3:
        st.markdown("**Chat with rag**")
        st.markdown("Interract with your custom DB thx to the RAG architecture")

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