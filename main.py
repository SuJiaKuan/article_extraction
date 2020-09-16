from article_extraction.article import Article
from article_extraction.util import contain_filtered_words
from article_extraction.const import FILTERED_WORDS


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
        for pargraph in article.paragraphs:
            for sentence in pargraph.sentences:
                if contain_filtered_words(sentence.text, FILTERED_WORDS):
                    sentence.delete()

        print(article.title)
        print(article.author_name)
        print(article.get_text(color=True))


if __name__ == "__main__":
    main()
