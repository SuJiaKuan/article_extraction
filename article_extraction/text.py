import re


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
