from article_extraction.article import Article


def main():
    html_paths = [
       "./data/html/samples/dama.html",
       "./data/html/samples/shuba.html",
       "./data/html/samples/shaoro.html",
       "./data/html/samples/logue.html",
       "./data/html/samples/victorial_steak.html",
       "./data/html/samples/lenin.html",
       "./data/html/samples/double_fat.html",
       "./data/html/samples/korea_soup.html",
       "./data/html/samples/ah_cheng.html",
    ]

    articles = [Article(p) for p in html_paths]

    for article in articles:
        print(article.title)
        print(article.author_name)
        print(article.get_text())


if __name__ == "__main__":
    main()
