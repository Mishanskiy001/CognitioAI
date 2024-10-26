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
    text = re.sub(r'\s+', ' ', text)  
    sentences = text.split('. ')

    words = re.findall(r'\w+', text.lower())
    word_freq = Counter(words)

    sentence_scores = {}
    for sentence in sentences:
        for word in re.findall(r'\w+', sentence.lower()):
            if word in word_freq:
                if sentence in sentence_scores:
                    sentence_scores[sentence] += word_freq[word]
                else:
                    sentence_scores[sentence] = word_freq[word]

    summarized_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)


    summary = '. '.join(summarized_sentences[:num_sentences])  
    return summary


def main():
    st.title("CognitioAI")

    uploaded_file = st.file_uploader("Загрузите PDF файл", type="pdf")

    if uploaded_file is not None:

        text = extract_text_from_pdf(uploaded_file)




        if len(text) > 0:
            summary = summarize_text(text, num_sentences=3) 
            st.write("Краткое содержание:")
            st.text(summary)
            st.write("Полный текст загруженного файла:")
            st.text(text)
        else:
            st.write("Не удалось извлечь текст из PDF.")


if __name__ == "__main__":
    main()
