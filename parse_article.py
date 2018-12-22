from bs4 import BeautifulSoup


def parse_article(html):
    """
    Извлечь текст
    Аргумент: объект BeautifulSoup
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
    all_text = (" {0} {1}").format(header, text)
    return all_text


if __name__ == "__main__":
    parse_article(html)
