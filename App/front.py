import streamlit as st

from data_reading import extract_text_from_txt, extract_text_from_pdf, extract_text_from_url
from text_analyzer import start_work
from synthesis import create_wav
import os


def delete_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f'Ошибка при удалении файла {file_path}. {e}')


def start():
    st.sidebar.header("REU DS Club")
    st.sidebar.image(image="App/orange_cat.png", use_column_width=True)
    st.title("Сложные темы простым языком")
    st.write("Это сервис, который автоматически создает 'беседы' на русском языке, "
             "превращая статьи или новости в диалог отца и дочери. "
             "Этот подход поможет подросткам понять смысл самых разных тем: "
             "от науки до социальных событий. Один задает вопросы, а другой — отвечает, "
             "направляя и разворачивая сложное содержание простым языком. "
             "Наш сервис логическо, информативно и интерактивно, передает даже непростые темы "
             "доступно и с интересом."
             )

    file_type = st.radio(label="Какого формата будет твой документ ?", options=("txt", "pdf", "url"))

    if file_type == "txt" or file_type == "pdf":
        delete_files_in_folder("App/files")
        user_file = st.file_uploader(f"Загрузи {file_type} здесь", type=[f"{file_type}"])

        if file_type == "txt" and user_file is not None:
            if user_file.name.endswith(".txt"):
                try:
                    with open(f"App/files/{user_file.name}", "wb") as f:
                        f.write(user_file.getbuffer())
                    st.success("File saved")
                    parsed_data = extract_text_from_txt(f"App/files/{user_file.name}")
                except Exception:
                    st.write("Неправильный pdf")
                else:
                    analyze_send(parsed_data, user_file.name[:user_file.name.find('.txt')])
            else:
                st.write("Неправильный формат документа")

        elif user_file is not None:
            if user_file.name.endswith(".pdf"):
                try:
                    with open(f"App/files/{user_file.name}", "wb") as f:
                        f.write(user_file.getbuffer())

                    st.success("File saved")
                    parsed_data = extract_text_from_pdf(f"App/files/{user_file.name}")
                except Exception:
                    st.write("Неправильный pdf")
                else:
                    analyze_send(parsed_data, user_file.name[:user_file.name.find('.pdf')])
            else:
                st.write("Неправильный формат документа")

    elif file_type == "url":
        delete_files_in_folder("App/files")
        url = st.text_area(label="Введи url")
        if url is not None and len(url) != 0:
            try:
                parsed_data = extract_text_from_url(url)
                analyze_send(parsed_data, "url")
            except Exception:
                st.write("Неправильный url")
            else:
                st.success("File saved")


def analyze_send(data, txt_filename):
    data_dad_daughter = start_work(data)
    create_wav(data_dad_daughter)
    with open("App/files/full_dialogue.wav", "rb") as f:
        data_wav = f.read()

    st.title("Скачать:")

    st.download_button(
        label="Скачать txt файл",
        data=data_dad_daughter,
        file_name=f"explanation_{txt_filename}.txt"
    )
    st.download_button(
        label="Скачать wav файл",
        data=data_wav,
        file_name="App/files/full_dialogue.wav"
    )

    st.title("Расшифровка беседы:")
    st.write(data_dad_daughter)


if __name__ == "__main__":
    start()