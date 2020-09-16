def contain_filtered_words(sentence, filtered_words):
    for filter_word in filtered_words:
        if type(filter_word) == list:
            contained_list = [f in sentence for f in filter_word]
            if all(contained_list):
                return True
        else:
            if filter_word in sentence:
                return True

    return False
