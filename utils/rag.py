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
Answer the following question based on the context provided.
If you cannot answer precisely to the question, precise that your answer is not entirely based on the context provided.

Context: {context}

Question: {question}
"""


def get_context(query_text, db_path):
    # Prepare the DB
    embeddings = OpenAIEmbeddings()
    db = Chroma(persist_directory=db_path, embedding_function=embeddings)

    # Search the DB
    results = db.similarity_search(query_text, k=3)
    return results


def answer_question(query_text, db_path: str = CHROMA_PATH):
    results = get_context(query_text=query_text, db_path=db_path)
    sources = [(doc.metadata.get("source", None), doc.metadata.get("page", None)) for doc in results]
    fromatted_sources = "\n\n".join([source + ' à la page: ' + str(page+1) for source, page in sources])
    
    context_text = "\n\n---\n\n".join([doc.page_content for doc in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    
    model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=st.secrets["OPENAI_API_KEY"])
    response_text = model.predict(prompt)

    formatted_response = f"{response_text}\n\n\nLes documents les plus pertinents utilisés pour cette réponse:\n\n {fromatted_sources}"
    
    return formatted_response


def litterature_review(questions, paper_path):
    answers = []
    for query_text in questions:
        results = get_context(query_text=query_text, db_path=paper_path)
        context_text = "\n\n---\n\n".join([doc.page_content for doc in results])
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query_text)
        model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=st.secrets["OPENAI_API_KEY"])
        answers += [model.predict(prompt)]
    return answers
