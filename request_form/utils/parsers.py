import re


def text_has_cyrillic_characters(text):
    return bool(re.search("[\u0400-\u04FF]", text))
