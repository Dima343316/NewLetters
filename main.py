import streamlit as st
from pages.create_letter import create_letter_page# Импортируем функцию, а не модуль
from pages.doc_preprocess_rag import rag_doc_page

# Список страниц
PAGES = {
    "Создание письма": create_letter_page,
    "RAG-Система": rag_doc_page,
}

# Получаем название текущей страницы
page = st.sidebar.selectbox("Выберите страницу", options=list(PAGES.keys()))

# Запускаем функцию страницы
PAGES[page]()  # Теперь это вызывает функцию, а не модуль
