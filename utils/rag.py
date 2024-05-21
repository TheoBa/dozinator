from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain.embeddings import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI
from langchain.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate
import streamlit as st


CHROMA_PATH = "data/chroma_emb"
MODEL = "gpt-3.5-turbo"
MODEL = "mixtral:8x7b"
PROMPT_TEMPLATE = """
Réponds à la question posée ci-dessous en te basant sur le contexte fournit.
Si tu ne peux pas répondre précisément à la question, réponds "je ne sais pas".

Contexte: {context}

Question: {question}
"""


def answer_question(query_text):
    # Prepare the DB
    embeddings = OpenAIEmbeddings()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)

    # Search the DB.
    results = db.similarity_search(query_text, k=3)
    # if len(results) == 0 or results[0][1] < 0.7:
    #     st.markdown(f"Unable to find matching results.")
    #     return

    context_text = "\n\n---\n\n".join([doc.page_content for doc in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    
    # st.markdown(prompt)

    model = ChatOpenAI(model="gpt-3.5-turbo")
    response_text = model.predict(prompt)

    # sources = [doc.metadata.get("source", None) for doc in results]
    # formatted_response = f"Response: {response_text}\nSources: {sources}"
    
    return response_text
