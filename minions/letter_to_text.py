import os
import streamlit as st
import fitz  # PyMuPDF для работы с PDF
from docx import Document
import textract
from odf.opendocument import load
from odf.text import P
import tempfile
import openai
from dotenv import load_dotenv
def extract_text_from_docx(file):
    try:
        doc = Document(file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        raise ValueError(f"Ошибка при извлечении текста из DOCX файла: {str(e)}")

# Функция для извлечения текста из PDF
def extract_text_from_pdf(file):
    try:
        # Открываем PDF файл с помощью PyMuPDF
        doc = fitz.open(file)
        text = ""
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)  # Загружаем страницу
            text += page.get_text()  # Извлекаем текст с текущей страницы
        return text
    except Exception as e:
        raise ValueError(f"Ошибка при извлечении текста из PDF файла: {str(e)}")

# Функция для извлечения текста из текстового файла (.txt)
def extract_text_from_txt(file):
    try:
        text = file.read().decode("utf-8")
        return text
    except Exception as e:
        raise ValueError(f"Ошибка при извлечении текста из TXT файла: {str(e)}")

# Функция для извлечения текста из ODT файлов
def extract_text_from_odt(file):
    try:
        doc = load(file)
        paragraphs = doc.getElementsByType(P)
        text = "\n".join([p.firstChild.data for p in paragraphs if p.firstChild is not None])
        return text
    except Exception as e:
        raise ValueError(f"Ошибка при извлечении текста из ODT файла: {str(e)}")

# Универсальная функция для извлечения текста из различных форматов
def extract_text_from_file(uploaded_file):
    # Получаем расширение файла
    file_extension = uploaded_file.name.split('.')[-1].lower()

    # Сохранение загруженного файла во временный файл
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.getbuffer())
        tmp_file_path = tmp_file.name

    # Определяем формат и извлекаем текст
    if file_extension == 'docx':
        return extract_text_from_docx(tmp_file_path)
    elif file_extension == 'pdf':
        return extract_text_from_pdf(tmp_file_path)
    elif file_extension == 'txt':
        with open(tmp_file_path, 'rb') as file:
            return extract_text_from_txt(file)
    elif file_extension == 'odt':
        return extract_text_from_odt(tmp_file_path)
    else:
        # Для других форматов можно использовать textract
        try:
            text = textract.process(tmp_file_path).decode('utf-8')  # Для большинства других форматов
            return text
        except Exception as e:
            raise ValueError(f"Ошибка при извлечении текста из файла {uploaded_file.name}: {str(e)}")
