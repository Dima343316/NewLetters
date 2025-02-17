import os
from datetime import datetime
from docx import Document

import openai
import streamlit as st
from dotenv import load_dotenv
from minions import letter_to_text

load_dotenv()


class LlamaModel:
    """Класс для работы с моделью GPT (например, Llama)."""

    def __init__(self):
        self.api_key = os.getenv("OPENAI_TOKEN_API")
        self.base_url = os.getenv("BASE_OPENAI_URL")
        self.max_input_tokens = 2048
        self.max_response_tokens = 2048

    def count_tokens(self, messages):
        return sum(len(message["content"].split()) for message in messages)

    def get_response(self, message):
        messages = [{"role": "user", "content": message}]

        if self.count_tokens(messages) > self.max_input_tokens:
            return "Ваш вопрос слишком длинный. Пожалуйста, сократите его."

        client = openai.Client(api_key=self.api_key, base_url=self.base_url)
        response = client.chat.completions.create(
            model="openai/gpt-4o-2024-11-20",
            messages=messages,
            temperature=0.4,
            max_tokens=1500,
            top_p=0.3,
            frequency_penalty=0.1,
            presence_penalty=0.1,
        )
        return response.choices[0].message.content


class PasteValues:
    """Класс для обработки шаблона документа и замены значений."""

    def __init__(self, template_path, data):
        self.template_path = template_path
        self.data = data

    def change_values(self, letter_body):
        current_datetime = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"docs/result/result_{current_datetime}.docx"
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        doc = Document(self.template_path)

        for p in doc.paragraphs:
            for key, value in self.data.items():
                placeholder = f"${{{key}}}"
                if placeholder in p.text:
                    for run in p.runs:
                        run.text = run.text.replace(placeholder, value)

        for p in doc.paragraphs:
            if "${letter_body}" in p.text:
                for run in p.runs:
                    run.text = run.text.replace("${letter_body}", letter_body)

        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for key, value in self.data.items():
                        placeholder = f"${{{key}}}"
                        if placeholder in cell.text:
                            for paragraph in cell.paragraphs:
                                for run in paragraph.runs:
                                    run.text = run.text.replace(placeholder, value)

        doc.save(filename)
        return filename


def create_letter_page():
    st.title("📄 Генерация писем")

    fio_recipient = st.text_input("🔹 ФИО получателя:", placeholder="Введите ФИО...")
    position_recipient = st.text_input("🔹 Должность получателя:", placeholder="Введите должность...")
    laws = st.text_area("⚖ Основные законы:", placeholder="Перечислите законы через запятую...")
    comments = st.text_area("📝 Комментарии:", placeholder="Укажите комментарии к письму...")
    topic_body = st.text_input("📝 Основная тема письма:", placeholder="Введите тему письма...")
    fio_sender = st.text_input("✍ ФИО отправителя:", placeholder="Введите ваше ФИО...")
    doc_date = st.date_input("📅 Дата создания документа:", value=datetime.today())

    incoming_letter = st.file_uploader("Загрузите входящее письмо", type=["pdf", "docx", "txt", "odt"])
    flag_incoming = False

    if incoming_letter and st.button("📌 Загрузить входящее письмо"):
        flag_incoming = True
        text_of_doc = letter_to_text.extract_text_from_file(incoming_letter)
        llama_model = LlamaModel()
        incoming_gpt = f"""
            Извлеките из следующего письма следующую информацию:
            1. Имя отправителя
            2. Организация отправителя
            3. Должность отправителя
            4. Основная часть письма

            Вот текст письма: {text_of_doc}

            Пожалуйста, извлеките только указанную информацию в виде списка без добавления дополнительных фраз.
        """
        doc_incoming = llama_model.get_response(incoming_gpt)
        st.text_area("Результат анализа входящего письма", doc_incoming, height=400)

    if st.button("📌 Сформировать письмо"):
        llama_model = LlamaModel()
        gpt_input = f"""
            Составьте официальное письмо на основе следующих данных.
            Письмо должно быть оформлено в строгом деловом стиле, без вступлений и заключений.

            1. Законы: {laws}
            2. Тема: {topic_body}
            3. Комментарии: {comments}
        """

        if flag_incoming:
            gpt_input = f"""
                Составьте ответ на входящее письмо {doc_incoming}.

                1. Законы: {laws}
                2. Тема: {topic_body}
                3. Комментарии: {comments}
            """

        letter_body = llama_model.get_response(gpt_input)

        data = {
            "fio_recipient": fio_recipient,
            "position_recipient": position_recipient,
            "laws": laws,
            "topic_body": topic_body,
            "fio_sender": fio_sender,
            "doc_date": str(doc_date),
            "letter_body": letter_body,
        }

        paste_values = PasteValues("docs/sample/docx_sample.docx", data)
        generated_filename = paste_values.change_values(letter_body)

        with open(generated_filename, "rb") as f:
            st.download_button(
                label="Скачать письмо",
                data=f,
                file_name=generated_filename,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )


if __name__ == "__main__":
    create_letter_page()
