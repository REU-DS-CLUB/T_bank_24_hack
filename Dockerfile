FROM python:3.12.3

# Устанавливаем Poetry
RUN pip install poetry

# Копируем файл pyproject.toml и poetry.lock в контейнер
COPY pyproject.toml poetry.lock ./

# Запускаем установку зависимостей через Poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

# Устанавливаем зависимости для PortAudio
RUN apt-get update && apt-get install -y libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 ffmpeg

# Установка pyaudio без использования PEP 517
RUN pip install --upgrade pip setuptools wheel
RUN pip install pyaudio

COPY ./App ./App

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "App/front.py"]