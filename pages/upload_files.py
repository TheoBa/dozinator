import os
from utils.create_database import generate_data_store
import streamlit as st


st.set_page_config(page_title='Chat with Dozinator', page_icon='📚', layout="wide")

CHROMA_PATH = "data/chroma_emb"
DATA_PATH = "data/dunod_physique.pdf"


def list_existing_databases(data_path: str = "data"):
    return [
        d for d in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, d))
        ]


def list_existing_files(data_path: str = "data"):
    return [
        d for d in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, d))
        ]

def upload_pdf():
    st.header("Create a new single file database")
    uploaded_file = st.file_uploader('Upload your .pdf file', type="pdf")
    if uploaded_file is not None:
        file_name = uploaded_file.name
        temp_file = "data/file_name"
        with open(temp_file, "wb") as file:
            file.write(uploaded_file.getvalue())
            
        db_name = st.text_input("Enter the name of associated database (default => file_name)")
        db_path = f"data/{db_name if db_name else file_name[:-4]}"
        st.button('Create vector database based on this document?', on_click=generate_data_store, args=[temp_file, db_path])
    

if __name__ == "__main__":
    st.header("Existing databases:")
    st.selectbox("Scroll through existing databases", list_existing_databases(data_path="data"))
    upload_pdf()