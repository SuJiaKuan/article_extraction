import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text


_SENTENCE_EMBEDDING_MODEL = \
    'https://tfhub.dev/google/universal-sentence-encoder-multilingual/3'


class SentenceEncoder(object):

    def __init__(self):
        # UniversalSentenceEncoder must be run in eager mode, so we turn it on
        # manually.
        tf.enable_eager_execution()

        self._encoder = hub.load(_SENTENCE_EMBEDDING_MODEL)

    def encode(self, text):
        return self._encoder(text)[0]
