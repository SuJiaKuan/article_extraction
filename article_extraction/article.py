import bs4

from article_extraction.io import read_text
from article_extraction.const import TERMINAL_COLOR


class Sentence(object):

    def __init__(self, text):
        self.text = text
        self.is_deleted = False

    def delete(self):
        self.is_deleted = True

    def get_text(self, color=False):
        if color:
            if self.is_deleted:
                text = self.text
            else:
                text = "{}{}{}".format(
                    TERMINAL_COLOR.OKGREEN,
                    self.text,
                    TERMINAL_COLOR.ENDC,
                )
        else:
            text = self.text

        return text


class Paragraph(object):

    def __init__(self, sentences):
        self.sentences = sentences

    def delete(self):
        for sentence in self.sentences:
            sentence.delete()

    def get_text(self, color=False):
        return "\n".join([s.get_text(color=color) for s in self.sentences])


class Article(object):

    def __init__(self, html_path):
        self.html_path = html_path

        self.title, self.author_name, self.paragraphs = \
            self._read_html(self.html_path)

    def _read_html(self, html_path):
        html_text = read_text(html_path)
        soup = bs4.BeautifulSoup(html_text, features="lxml")

        title = soup.find("title").getText()

        author_name = soup.findAll("div", {"class": "author-profile__name"})
        if not author_name:
            author_name = soup.findAll("a", {"class": "author-profile__name"})
        author_name = author_name[0].getText()

        article_body = soup.findAll("div", {"class": "article-body"})[0]

        sentence_texts = [x.getText(strip=True)
                          for x in article_body.find_all("p")]

        paragraphs = []
        paragraph_sentences = []

        for sentence_text in sentence_texts:
            if len(sentence_text) <= 1:
                if paragraph_sentences:
                    paragraphs.append(Paragraph(paragraph_sentences))
                    paragraph_sentences = []
            else:
                paragraph_sentences.append(Sentence(sentence_text))

        if paragraph_sentences:
            paragraphs.append(Paragraph(paragraph_sentences))

        return title, author_name, paragraphs

    def get_text(self, color=False):
        return "\n\n".join([p.get_text(color=color) for p in self.paragraphs])
