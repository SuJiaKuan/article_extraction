import bs4

from article_extraction.io import read_text
from article_extraction.const import TERMINAL_COLOR


class Sentence(object):

    def __init__(self, text, idx):
        self.text = text
        self.idx = idx
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

    def __init__(self, sentences, idx):
        self.sentences = sentences
        self.idx = idx

    def delete(self):
        for sentence in self.sentences:
            sentence.delete()

    def get_text(self, color=False, deleted=True):
        out_sentences = []
        for sentence in self.sentences:
            if deleted or not sentence.is_deleted:
                out_sentences.append(sentence.get_text(color=color))

        return "\n".join(out_sentences)


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

        sentence_texts = []
        for p in article_body.find_all("p"):
            sentence_text = p.getText(strip=True)

            # Skip the case that the whole sentence text is a link.
            if len(sentence_text) > 1:
                anchor_child = p.find("a")
                if anchor_child is not None:
                    if sentence_text == anchor_child.getText(strip=True):
                        continue

            sentence_texts.append(sentence_text)

        paragraphs = []
        paragraph_sentences = []

        sentence_idx = 0
        paragraph_idx = 0

        for sentence_text in sentence_texts:
            if len(sentence_text) <= 1:
                if paragraph_sentences:
                    paragraphs.append(Paragraph(
                        paragraph_sentences,
                        paragraph_idx,
                    ))
                    paragraph_idx += 1
                    sentence_idx = 0
                    paragraph_sentences = []
            else:
                paragraph_sentences.append(Sentence(
                    sentence_text,
                    sentence_idx,
                ))
                sentence_idx += 1

        if paragraph_sentences:
            paragraphs.append(Paragraph(paragraph_sentences, paragraph_idx))

        return title, author_name, paragraphs

    def get_text(self, color=False, deleted=True, compact=False):
        text = "\n\n".join([p.get_text(color=color, deleted=deleted)
                            for p in self.paragraphs])

        if compact:
            text = text.replace("\n", "")

        return text
