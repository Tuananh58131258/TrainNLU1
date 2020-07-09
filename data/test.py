import re
import random
# price = open('data/ram.txt',encoding='utf-8').readlines()
# f_p = '{"entity":"price","role":"from_price"}'
# t_p = '{"entity":"price","role":"to_price"}'
# for i in range(1,5):
#     rom = price[random.randint(0,len(price)-1)].strip('\n')
#     print("- điện thoại ram [{}](ram)".format(rom))
#     print("- dien thoai ram [{}](ram)".format(rom))
#     print("- điện thoại có ram [{}](ram)".format(rom))
#     print("- khoảng [{}](price) trở xuống".format(gia))
#     print("- khoảng dưới [{}](price)".format(gia))
#     print("- [{}](price) trở xuống".format(gia))
#     print("- ít hơn [{}](price)".format(gia))
#     print("- từ [{}](price) quay đầu".format(gia))
# text = 'điện     thoại 8   củ'
# text = re.sub(r'củ|trieu|cu','triệu',text)
# print(re.sub(r'\s\s+',' ',text))
text ="giá của zphlip"
temp= re.search(r"\bip[^h]",text)
print(temp)