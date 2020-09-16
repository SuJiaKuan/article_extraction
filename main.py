import numpy as np

from article_extraction.article import Article
from article_extraction.model import SentenceEncoder
from article_extraction.const import FILTERED_WORDS


START_SIMILARITY_RATIO = 0.5
SIMILARITY_THRESHOLD = 0.5

DELETE_DIRECTLY_THRESHOLD = 0.5


def main():
    '''
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
    '''
    html_paths = [
       "./data/html/samples/dama.html",
    ]

    sentence_encoder = SentenceEncoder()

    articles = [Article(p) for p in html_paths]

    for article in articles:
        title_vec = sentence_encoder.encode(article.title)

        start_similarity_idx = len(article.paragraphs) * START_SIMILARITY_RATIO

        # Delete last graph of an article because it is not useful in most
        # cases.
        article.paragraphs[-1].delete()

        # Handle for each paragraph (except last paragraph).
        for paragraph in article.paragraphs[0:-1]:
            for sentence in paragraph.sentences:
                if sentence.contains(FILTERED_WORDS):
                    sentence.delete()
                elif paragraph.idx >= start_similarity_idx:
                    sentence_vec = sentence_encoder.encode(sentence.text)
                    similarity = np.dot(title_vec, sentence_vec)
                    if similarity >= SIMILARITY_THRESHOLD:
                        sentence.delete()

            num_deleted = len([s for s in paragraph.sentences if s.is_deleted])
            ratio_deleted = num_deleted / len(paragraph.sentences)
            if ratio_deleted >= DELETE_DIRECTLY_THRESHOLD:
                paragraph.delete()

        print("[TITLE]", article.title)
        print("[AUTHOR]", article.author_name)
        print("[CONTENT]")
        print(article.get_text(color=True))
        print("==============================")


if __name__ == "__main__":
    main()
