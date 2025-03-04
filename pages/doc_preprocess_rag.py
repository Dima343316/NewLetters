import streamlit as st
from datetime import datetime
import os
from docx import Document
import openai
from dotenv import load_dotenv
from pymupdf import message

from minions import letter_to_text
from minions import rag_doc

load_dotenv()


# Основная страница для ввода данных
def rag_doc_page():
    folders = os.listdir(r"db_docs")
    st.title("📄 RAG-система")
    law = st.selectbox("Выберите документ:", folders)
    query = st.text_input("⚖ Введите ваш вопрос документу:", placeholder="Введите вопрос...")
    name = st.text_input("⚖ Введите название документа в базу:", placeholder="Введите название...")
    incoming_letter = st.file_uploader("Загрузите документ в базу", type=["pdf", "docx", "txt", "odt"])
    if st.button("📌 Загрузить документ в базу"):
        if name in folders:
            st.warning(f"База с именем {name} уже существует!")
        if incoming_letter and (name not in folders):
            text_of_doc = letter_to_text.extract_text_from_file(incoming_letter)
            rag_doc.create_search_db(text_of_doc,f"db_docs/{name}")
            st.success("Успех! База создана.")
    if st.button("📌 Задать вопрос"):
        if query and law:
            answer=rag_doc.run_gpt_query(query, f"db_docs/{law}")
            st.text_area("Результат анализа акта", answer, height=400)


if __name__ == "__main__":
    rag_doc_page()
