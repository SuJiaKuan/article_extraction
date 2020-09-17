import re


def contains(text, words):
    for word in words:
        if type(word) == list:
            contained_list = [f in text for f in word]
            if all(contained_list):
                return True
        else:
            if word in text:
                return True

    return False


def de_emojify(text):
    pattern = (
        u"["
        u"\U0001F600-\U0001F64F"  # emotions
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"]+"
    )
    regrex_pattern = re.compile(pattern=pattern, flags=re.UNICODE)
    text_out = regrex_pattern.sub(r'', text)

    return text_out


def replace(text, mapping):
    text_out = text

    for before, after in mapping.items():
        text_out = text_out.replace(before, after)

    return text_out


def remove_continuous_tokens(text, tokens):
    text_out = text

    for token in tokens:
        text_out = re.sub("[{}]+".format(token), token, text_out)

    return text_out
