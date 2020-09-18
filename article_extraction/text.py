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


def contains_business_hours(text):
    business_hours = re.findall(r"\d{1,2}：\d{1,2}", text)

    return len(business_hours) >= 2


def contains_phone_numbers(text):
    input_text = text
    for ch in ["（", "）", " ", "-"]:
        input_text = input_text.replace(ch, "")

    # Referecne: https://zh.wikipedia.org/wiki/%E4%B8%AD%E8%8F%AF%E6%B0%91%E5%9C%8B%E9%95%B7%E9%80%94%E9%9B%BB%E8%A9%B1%E5%8D%80%E8%99%9F%E8%A1%A8
    phone_numbers = re.findall(
        r"02\d{8}"  # Taipei
        r"|037\d{6}"  # Miaoli
        r"|03\d{7}"  # Taoyuan / Hsinchu / Hualien / Yilan
        r"|04\d{8}"  # Taichung
        r"|04\d{7}"  # Changhua
        r"|049\d{6}"  # Nantou
        r"|05\d{7}"  # Chiayi / Yunlin
        r"|06\d{7}"  # Tainan / Penghu
        r"|07\d{7}"  # Kaohsiung
        r"|08\d{7}"  # Pingtung
        r"|089\d{6}"  # Taitung
        r"|082\d{6}"  # Kinmen
        r"|0836\d{5}",  # Matsu
        input_text
    )

    return len(phone_numbers) >= 1
