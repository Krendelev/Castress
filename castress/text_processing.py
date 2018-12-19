accents = {"джуниор": "дж+униор", "Джуниор": "Дж+униор"}


def parse_article():
    """
    Извлечь текст
    Аргумент: объект BeautifulSoup
    Результат: текст статьи очищенный от тегов
    """
    pass


def count_insertions():
    """
    Посчитать количество вставок (код, картинки) в статье
    Аргумент: объект BeautifulSoup
    """
    pass


def place_accents(text, accents):
    """
    Расставить ударения
    Аргумент: текст, словарь ударений
    Результат: текст статьи с ударениями в словах
    """
    for word, accented_word in accents.items():
        corrected_text = text.replace(word, accented_word)
        text = corrected_text
    return text


def get_text_chunk():
    """
    Вырезать фрагмент текста не больше определенного размера
    Аргумент: текст, размер
    Результат: синтаксически полный фрагмент текста
    """
    pass
