from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI
from langchain_community.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate
import streamlit as st


CHROMA_PATH = "data/chroma_emb"
MODEL = "gpt-3.5-turbo"
MODEL = "mixtral:8x7b"
PROMPT_TEMPLATE = """
Réponds à la question posée ci-dessous en te basant sur le contexte fournit.
Si tu ne peux pas répondre précisément à la question, précise "Le contexte fournit ne me permet pas de répondre précisément à votre question".
Mais donne la réponse la plus probable selon toi.

Contexte: {context}

Question: {question}
"""


def get_context(query_text, db_path):
    # Prepare the DB
    embeddings = OpenAIEmbeddings()
    db = Chroma(persist_directory=db_path, embedding_function=embeddings)

    # Search the DB
    results = db.similarity_search(query_text, k=3)
    return results


def answer_question(query_text):
    results = get_context(query_text=query_text, db_path=CHROMA_PATH)
    sources = [(doc.metadata.get("source", None), doc.metadata.get("page", None)) for doc in results]
    fromatted_sources = "\n\n".join([source + ' à la page: ' + str(page+1) for source, page in sources])
    
    context_text = "\n\n---\n\n".join([doc.page_content for doc in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    
    model = ChatOpenAI(model="gpt-3.5-turbo")
    response_text = model.predict(prompt)

    formatted_response = f"{response_text}\n\n\nLes documents les plus pertinents utilisés pour cette réponse:\n\n {fromatted_sources}"
    
    return formatted_response
