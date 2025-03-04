import streamlit as st
from datetime import datetime
import os
from docx import Document
import openai
import json
from dotenv import load_dotenv
from minions import letter_to_text

load_dotenv()


# Класс для работы с моделью GPT (например, Llama)
# Класс для работы с API
class LlamaModel:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_TOKEN_API')  # Чтение ключа API
        self.base_url = os.getenv('BASE_OPENAI_URL')
        self.max_input_tokens = 2048  # Максимум токенов для входного сообщения
        self.max_response_tokens = 2048  # Максимум токенов для ответа

    def count_tokens(self, messages):
        tokens = sum(len(message["content"].split()) for message in messages)
        return tokens

    def get_response(self, message):
        messages = [
            {"role": "user", "content": message}
        ]

        total_tokens = self.count_tokens(messages)
        if total_tokens > self.max_input_tokens:
            return "Ваш вопрос слишком длинный. Пожалуйста, сократите его."

        client = openai.Client(
            api_key=self.api_key,
            base_url=self.base_url,
        )

        response = client.chat.completions.create(
            model="openai/gpt-4o-2024-11-20",  # Укажите модель, например, OpenAI GPT-3
            messages=messages,
            temperature=0.4,  # Степень случайности
            max_tokens=1500,  # Максимальное количество токенов в ответе
            top_p=0.3,  # Использование метода nucleus sampling
            frequency_penalty=0.1,  # Штраф за частоту
            presence_penalty=0.1,  # Штраф за присутствие
        )

        return response.choices[0].message.content


# Основная страница для ввода данных
# def create_db_description():
#     st.title("📄 Создание описаний для базы данных")
#     folders = os.listdir(r"db_docs")
#     law = st.selectbox("Выберите документ:", folders)
#     law_name = st.text_input("🔹 Название документа:", placeholder="Введите название документа...")
#     law_description = st.text_input("🔹 Описание документа:", placeholder="Введите описание документа...")
#     if st.button("📌 Сформировать описание для БД"):
#         try:
#             # Чтение существующих данных из файла
#             with open("db_description.json", "r", encoding="utf-8") as json_file:
#                 db_desc = json.load(json_file)
#
#         except FileNotFoundError:
#             # Если файл не существует, создаем его с пустым списком
#             db_desc = {"law_db": []}
#         #     for i in db_desc["law_db_folder"]:
#         #         if i == law:
#         #             st.warning(f"База с законом {law} уже существует!")
#         with open("db_description.json", "r+"):
#             data = {
#                 "law_db": law,
#                 "law_name": law_name,
#                 "law_description": law_description
#             }
#             db_desc["law_db"].append(data)
#
# if __name__ == "__main__":
#     create_db_description()
