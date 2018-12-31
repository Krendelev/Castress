from bs4 import BeautifulSoup

with open("test.html", "r", encoding="utf-8") as test:
    html = test.read()

SYMBOL_LIMIT = 2000
accents = {"джуниор": "дж+униор", "Джуниор": "Дж+униор"}


def parse_article(html):
    """
    Извлечь текст
    Аргумент: строка с html
    Результат: текст статьи очищенный от тегов
    """
    soup_text = BeautifulSoup(html, "html.parser")
    # заголовок
    header_with_tags = soup_text.find("title")
    header = header_with_tags.get_text()
    # текст
    text_with_tags = soup_text.find(
        "div", class_="post__text post__text-html js-mediator-article"
    )
    text = text_with_tags.get_text()
    # все вместе
    all_text = ("{0}. {1}").format(header, text)
    all_text = all_text.replace("\n", " ")
    return all_text


def count_insertions(html):
    """
    Посчитать количество вставок (код, картинки) в статье
    Аргумент: строка с html
    Результат: количество картинок в статье
    """
    soup = BeautifulSoup(html, "html.parser")
    article_soup = soup.find(
        "div", class_="post__text post__text-html js-mediator-article"
    )
    article_image = article_soup.find_all("img")
    if article_image:
        count_article_image = len(article_image)
    else:
        count_article_image = 0
    return count_article_image


def the_presence_of_code(html):
    """
    Проверить статью на наличие кода
    Аргумент: строка с html
    Результат: информация о наличии кода в статье
    """

    soup = BeautifulSoup(html, "html.parser")
    tag_code_soup = soup.find(
        "div", class_="post__text post__text-html js-mediator-article"
    )
    code = tag_code_soup.find("code")
    if code:
        return True
    else:
        return False


def saved_synopses(html):
    """
    Сохранить синопсисы
    Аргумент: строка с html
    Результат: текст синопсиса
    """
    soup = BeautifulSoup(html, "html.parser")
    soup_synopsis = soup.find("meta", {"name": "description"})
    if soup_synopsis:
        synopsis = soup_synopsis.get("content")
        return synopsis
    else:
        return None


def place_accents(all_text, accents):
    """
    Расставить ударения
    Аргумент: текст, словарь ударений
    Результат: текст статьи с ударениями в словах
    """
    for word, accented_word in accents.items():
        corrected_text = all_text.replace(word, accented_word)
        all_text = corrected_text
    return all_text


def get_text_chunk(all_text):
    """
    Вырезать фрагмент текста не больше определенного размера
    Аргумент: текст, размер
    Результат: синтаксически полный фрагмент текста
    """
    all_text = all_text.split(". ")
    text_cake = []
    text_cake_len = 0
    for text_piece in all_text:
        if not text_cake_len + len(text_piece) > SYMBOL_LIMIT:
            text_cake_len += len(text_piece)
            text_cake.append(text_piece)
    separator = ". "
    return separator.join(text_cake)


if __name__ == "__main__":
    get_text_chunk(place_accents(parse_article(html), accents))
    count_insertions(html)
    saved_synopses(html)
    the_presence_of_code(html)
