import re
import random
data = open('data/product_name.txt',encoding='utf-8').readlines()
rom = open('data/rom.txt',encoding='utf-8').readlines()
for i in range(1,10):
    ten = data[random.randint(0,len(data)-1)].strip('\n')
    ten1 = rom[random.randint(0,len(rom)-1)].strip('\n')
    # ten2 = data[random.randint(0,len(data)-1)].strip('\n')
    print('- đặt mua [{}](product_name) [{}](rom)'.format(ten,ten1))
    # print('- máy [{}](product_name) rơi xuống nước có sao không'.format(ten1))
    # print('- [{}](product_name) có chống nước không'.format(ten2))