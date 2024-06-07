from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
import os
import shutil

CHROMA_PATH = "data/chroma_emb"
DATA_PATH = "data/dunod_physique.pdf"


def generate_data_store():
    documents = load_document(data_path=DATA_PATH)
    chunks = split_text(documents)
    save_to_chroma(chunks, db_path=CHROMA_PATH)


def load_document(data_path: str = DATA_PATH):
    loader = PyPDFLoader(data_path)
    documents = loader.load()
    return documents


def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    return chunks


def save_to_chroma(chunks: list[Document], db_path: str = CHROMA_PATH):
    # Clear out the database first.
    if os.path.exists(db_path):
        shutil.rmtree(db_path)

    # Create a new DB from the documents.
    db = Chroma.from_documents(
        documents=chunks, 
        embedding=OpenAIEmbeddings(), 
        persist_directory=db_path
    )
    db.persist()
    db.heartbeat()
    print(f"Saved {len(chunks)} chunks to {db_path}.")
