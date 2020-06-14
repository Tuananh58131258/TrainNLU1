from underthesea import sent_tokenize
from underthesea import word_tokenize
data = open('data/thoigian.txt',encoding='utf-8').readlines()
for item in data:
    try:
        sent_tokenize(item)
        word_tokenize(item)
    except:
        print(data.index(item))