import re
import random
price = open('data/price.txt',encoding='utf-8').readlines()
f_p = '{"entity":"price","role":"from_price"}'
t_p = '{"entity":"price","role":"to_price"}'
for i in range(1,10):
    gia = price[random.randint(0,len(price)-1)].strip('\n')
    print("- dưới [{}](price)".format(gia))
    print("- từ [{}](price) trở lại".format(gia))
    print("- khoảng [{}](price) trở xuống".format(gia))
    print("- khoảng dưới [{}](price)".format(gia))
    print("- [{}](price) trở xuống".format(gia))
    print("- ít hơn [{}](price)".format(gia))
    print("- từ [{}](price) quay đầu".format(gia))