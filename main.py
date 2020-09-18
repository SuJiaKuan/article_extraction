import pandas as pd

from article_extraction.article import Article
from article_extraction.text import contains
from article_extraction.text import remove_continuous_tokens
from article_extraction.text import de_emojify
from article_extraction.text import replace
from article_extraction.text import contains_business_hours
from article_extraction.text import contains_phone_numbers
from article_extraction.const import FILTERED_WORDS
from article_extraction.const import REPLACEMENT_MAPPING
from article_extraction.const import SENTENCE_END_TOKENS
from article_extraction.const import NO_CONTINUOUS_TOKENS
from article_extraction.const import PARAGRAPH_END_TOKENS
from article_extraction.const import TAIWAN_COUNTRIES


DELETE_DIRECTLY_THRESHOLD = 0.5


def process_article(article):
    # TODO (SuJiaKuan): Apply copying before processing the article.

    for paragraph in article.paragraphs:
        num_deleted = 0
        num_sentences = len(paragraph.sentences)

        for sentence in paragraph.sentences:
            sentence.text = de_emojify(sentence.text)
            sentence.text = replace(
                sentence.text,
                REPLACEMENT_MAPPING,
            )
            sentence.text = remove_continuous_tokens(
                sentence.text,
                NO_CONTINUOUS_TOKENS,
            )

            while sentence.text.endswith('~'):
                sentence.text = sentence.text[0:-1]

            if sentence.text:
                if num_sentences == 1 or sentence.idx < num_sentences - 1:
                    if not sentence.text.endswith(SENTENCE_END_TOKENS):
                        sentence.text += "，"
                else:
                    if not sentence.text.endswith(PARAGRAPH_END_TOKENS):
                        sentence.text += "。"

            is_business_hours = contains_business_hours(sentence.text)
            is_phone_numbers = contains_phone_numbers(sentence.text)

            should_delete = \
                len(sentence.text) == 0 \
                or contains(sentence.text, FILTERED_WORDS) \
                or contains(sentence.text, TAIWAN_COUNTRIES) \
                or is_business_hours \
                or is_phone_numbers
            if should_delete:
                sentence.delete()
                num_deleted += 1

        num_deleted = len([s for s in paragraph.sentences if s.is_deleted])
        ratio_deleted = num_deleted / num_sentences
        if ratio_deleted >= DELETE_DIRECTLY_THRESHOLD:
            paragraph.delete()

    # Delete last graph of an article because it is not useful in most
    # cases.
    article.paragraphs[-1].delete()

    return article


def main():
    output_path = ''
    # output_path = 'output.csv'

    info_path = "./data/777.csv"

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
    '''
    html_paths = ['./data/html/777/{}.html'.format(str(i).zfill(4))
                  for i in range(0, 10)]
    '''
    html_paths = [
       "./data/html/samples/dama.html",
    ]

    info_df = pd.read_csv(info_path)
    abstracts = list(info_df["摘要"])

    articles = [Article(p) for p in html_paths]

    output = {
        "content": [],
        "abstract": [],
    }

    for article_idx, article in enumerate(articles):
        article_id = str(article_idx).zfill(4)

        print("============== {} ==============".format(article_id))

        article = process_article(article)

        content_pretty = article.get_text(color=True)
        content_compact = article.get_text(compact=True, deleted=False)

        if not content_compact.endswith("。"):
            content_compact = content_compact[0:-1] + "。"

        if output_path:
            abstract = abstracts[article_idx]

            output["content"].append(content_compact)
            output["abstract"].append(abstract)

            print("Sucess to process article: {}".format(article_id))
        else:
            print("[TITLE]", article.title)
            print("[AUTHOR]", article.author_name)
            print("[CONTENT : PRETTY]")
            print(content_pretty)
            print("[CONTENT : COMPACT]")
            print(content_compact)

    if output_path:
        df = pd.DataFrame(output)
        df.to_csv(output_path)

        print("Result saved in {}".format(output_path))


if __name__ == "__main__":
    main()
