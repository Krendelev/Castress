accents = {"джуниор": "дж+униор", "Джуниор": "Дж+униор"}


def get_articles_urls():
    """
    Собрать url статей
    Аргумент: url раздела
    Результат: список url статей из заданного раздела
    """
    pass


def save_articles_url():
    """
    Сохранить url в базу
    Аргумент: список url
    """
    pass


def is_url_processed():
    """
    Проверить наличие url в базе
    Аргумент: url
    """
    pass


def get_article():
    """
    Скачать статью
    Аргумент: url
    Результат: объект BeautifulSoup со статьей
    """
    pass


def count_insertions():
    """
    Посчитать количество вставок (код, картинки) в статье
    Аргумент: объект BeautifulSoup
    """
    pass


def parse_article():
    """
    Извлечь текст
    Аргумент: объект BeautifulSoup
    Результат: текст статьи очищенный от тегов
    """
    pass


def place_accents(text):
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


def get_audio():
    """
    Получить аудиоверсию текста
    Аргумент: текст
    Результат: объект с аудио
    """
    pass


def join_audio():
    """
    Соединить фрагменты аудио
    Аргумент: массив объектов с аудио
    Результат: объект с аудио
    """
    pass


def save_audio():
    """
    Сохранить аудиофайл
    Аргумент: объект с аудио
    Результат: файл на диске или в базе
    """
    pass
