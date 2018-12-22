from bs4 import BeautifulSoup


def count_insertions(html):
    """
    Посчитать количество вставок (код, картинки) в статье
    Аргумент: объект BeautifulSoup
    """
    soup = BeautifulSoup(html, "html.parser")
    article_soup = soup.find(
        "div", class_="post__text post__text-html js-mediator-article"
    )
    article_image = article_soup.find_all("img")
    count_article_image = len(article_image)
    return count_article_image


if __name__ == "__main__":
    count_insertions(html)
