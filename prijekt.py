import streamlit as st
import fitz  # PyMuPDF
import re
from collections import Counter


def extract_text_from_pdf(uploaded_file):
    """Извлечение текста из PDF файла."""
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def summarize_text(text, num_sentences=3):
    """Создание краткого содержания текста с использованием частотного анализа."""
    # Удаление лишних символов
    text = re.sub(r'\s+', ' ', text)  # Удаляем лишние пробелы
    sentences = text.split('. ')

    # Создание частотного словаря
    words = re.findall(r'\w+', text.lower())
    word_freq = Counter(words)

    # Оценка важности предложений
    sentence_scores = {}
    for sentence in sentences:
        for word in re.findall(r'\w+', sentence.lower()):
            if word in word_freq:
                if sentence in sentence_scores:
                    sentence_scores[sentence] += word_freq[word]
                else:
                    sentence_scores[sentence] = word_freq[word]

    # Сортируем предложения по их оценкам
    summarized_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)

    # Возвращаем краткое содержание
    summary = '. '.join(summarized_sentences[:num_sentences])  # Возвращаем первые num_sentences
    return summary


def main():
    st.title("CognitioAI")

    uploaded_file = st.file_uploader("Загрузите PDF файл", type="pdf")

    if uploaded_file is not None:
        # Извлечение текста
        text = extract_text_from_pdf(uploaded_file)



        # Создание краткого содержания
        if len(text) > 0:
            summary = summarize_text(text, num_sentences=3)  # Извлекаем 3 предложения
            st.write("Краткое содержание:")
            st.text(summary)
        # Выводим текст
            st.write("Полный текст загруженного файла:")
            st.text(text)
        else:
            st.write("Не удалось извлечь текст из PDF.")


if __name__ == "__main__":
    main()
