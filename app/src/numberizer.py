import string
from text_to_num import alpha2digit

def numberize(text: str):
    not_sussy = alpha2digit(text, "en")
    return not_sussy.translate(str.maketrans('', '', string.punctuation))
