import re
from typing import Any, Dict, List, Text
from rasa.nlu.tokenizers.tokenizer import Token, Tokenizer
from rasa.nlu.training_data import Message

from rasa.nlu.constants import TOKENS_NAMES, MESSAGE_ATTRIBUTES
from underthesea import word_tokenize
text = "Cấu hình của Xiaomi Mi Note 10 Pro 8GB-256GB??????"
text = text.lower()
text = re.sub(r"(?<=[^\s])\-+(?<=[^\s])"," - ",text)
text = re.sub("\++","+",text)
text = re.sub(r"(?<=[^0-9])[\.|\,]+(?=[^0-9\s])|\.\s|\,\s|\s\,|\s\.|[^\,\+\.\-\s\%\w]"," ",text,)
text = text.strip('\n')

# print(text)
words = word_tokenize(text)
print(word_tokenize(text,format="text"))
print

