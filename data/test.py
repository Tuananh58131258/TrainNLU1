import re
import random
price = open('data/price.txt',encoding='utf-8').readlines()
f_p = '{"entity":"price","role":"from_price"}'
t_p = '{"entity":"price","role":"to_price"}'
for i in range(1,10):
    gia = price[random.randint(0,len(price)-1)].strip('\n')
    print("- hơn [{}](price)".format(gia))
    print("- trên [{}](price)".format(gia))
    print("- cao hơn [{}](price)".format(gia))
    print("- [{}](price) hơn".format(gia))
    print("- [{}](price) trở lên".format(gia))
    print("- nhiều hơn [{}](price)".format(gia))
    print("- từ [{}](price) trở lên".format(gia))