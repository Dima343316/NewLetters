# Используем официальный образ Python как базовый
FROM python:3.10-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы проекта в рабочую директорию контейнера
COPY . /app

# Обновляем pip
RUN pip install --upgrade pip

# Устанавливаем все зависимости из requirements.txt
RUN pip install -r requirements.txt

# Устанавливаем дополнительные пакеты, если нужны (например, libpq-dev для PostgreSQL)
RUN apt-get update && apt-get install -y libpq-dev

# Открываем порт 8501 для Streamlit
EXPOSE 8501

# Определяем команду для запуска Streamlit приложения
# Используем официальный образ Python как базовый
FROM python:3.10-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы проекта в рабочую директорию контейнера
COPY . /app

# Обновляем pip
RUN pip install --upgrade pip

# Устанавливаем все зависимости из requirements.txt
RUN pip install -r requirements.txt

# Устанавливаем дополнительные пакеты, если нужны (например, libpq-dev для PostgreSQL)
RUN apt-get update && apt-get install -y libpq-dev

# Открываем порт 8501 для Streamlit
EXPOSE 8501

# Определяем команду для запуска Streamlit приложения
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.enableCORS=false"]
