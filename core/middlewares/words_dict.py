"""Функция для извлечения слов для словаря программы"""


def extract_words(file):
    words = []
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            w = line.strip().lower()
            words.append(w)
    return words
