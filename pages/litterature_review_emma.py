import streamlit as st
import pandas as pd
from utils.rag import litterature_review
import os


st.set_page_config(page_title='Chat with Dozinator', page_icon='📚', layout="wide")


QUESTIONS = [
    "When was this article published?",
    "In which newspaper / source was it published?",
    "List the authors of the article",
    "In which of the following type this article falls into: ['systematic review', 'litterature review','experimental research']",
    "In which category does the described experiment falls into: ['in vivo', 'in vitro', 'in silico'] ?",
    "What species are studied ?",
    "On which species are the experiments carried out? ",
    "What is the size of the population studied? What is the size of the group used for the experiment?",
    "What is the age and sex of the studied population? If it’s not specified, at what stage of development are the species mentioned? ",
    "List the main moleculare and cellular techniques used",
    "Can you name the molecular and cellular analysis techniques used in the experiment ? ",
    "What is the observation time of the experiment ?",
    "Which regeneration mechanism is observed, choose between ['epimorphosis', 'morphallaxis', 'heteromorphosis']",
    "What tissues are involved?",
    "Which cells are involved in the regeneration mechanism studied?",
    "How long does regeneration take after amputation? ",
    "What are the different stages of regeneration observed?",
    "What are the different stages of regeneration observed from a cellular point of view?",
    "What genes are expressed?",
    "What proteins are expressed?"
]

def litterature_review_page():
    st.title("Extract information from litterature review")
    list_databases = [d for d in os.listdir("data") if os.path.isdir(os.path.join("data", d))]
    with st.form("my_form"):
        paper_names = st.multiselect(
            "Which paper would you like to extract information from:",
            list_databases
            )
        
        submitted = st.form_submit_button("Submit")
    if submitted:
        db_paths = [f"data/{db_path}" for db_path in paper_names]
        answers = []
        with st.spinner('Review in progress...'):
            for paper in db_paths:
                answers += [litterature_review(questions=QUESTIONS, paper_path=paper)]
        st.success('Done!')
        df = pd.DataFrame(answers, columns=QUESTIONS, index=paper_names)
        st.dataframe(df)
        csv = df.to_csv().encode('utf-8')
        st.download_button(
            "Press to Download",
            csv,
            "litterature_review.csv",
            "text/csv",
            key='download-csv'
            )


if __name__ == "__main__":
    litterature_review_page()