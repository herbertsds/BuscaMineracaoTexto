import re
from unidecode import unidecode

def format_text(text):
    text = text.replace('\n', ' ').replace('\r', ' ').replace('  ', ' ')
    text = re.sub(' +', ' ', text)
    text = re.sub(';', '', text)
    return unidecode(text.upper())
