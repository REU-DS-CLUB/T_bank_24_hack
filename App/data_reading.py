import os
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
import re


def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'([^\S\r\n]+|\n)+', ' ', text)
    return text.strip()


def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return clean_text(text)


def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                # Очищаем текст на случай появления лишних символов
                cleaned_page_text = clean_text(page_text)
                text += cleaned_page_text + " "  # Добавляем пробел между страницами для логичности
    return text.strip()


def extract_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    text = ' '.join([para.get_text() for para in paragraphs])
    return clean_text(text)


def get_text_from_source(source):
    if os.path.isfile(source):
        if source.lower().endswith('.txt'):
            return extract_text_from_txt(source)
        elif source.lower().endswith('.pdf'):
            return extract_text_from_pdf(source)
        else:
            raise ValueError("Неподдерживаемый формат файла. Поддерживаются только .txt и .pdf.")
    elif source.startswith('http://') or source.startswith('https://'):
        return extract_text_from_url(source)
    else:
        raise ValueError("Неправильный источник. Убедитесь, что это путь к файлу или URL.")
