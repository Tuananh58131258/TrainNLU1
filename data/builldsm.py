import random
import re
ten = open('data/product_name.txt',encoding='utf-8').readlines()
# gia = open('data/price.txt',encoding='utf-8').readlines()
# ram = open('data/ram.txt',encoding='utf-8').readlines()
# rom = open('data/rom.txt',encoding='utf-8').readlines()

# for i in range(0,30):
#     n = random.randint(1,3)
#     if n == 1:
#         res = "- đặt mua [{}](product_name) [{}](rom)".format(ten[random.randint(0,len(ten)-1)].strip('\n'),rom[random.randint(0,len(rom)-1)].strip('\n'))
#     if n == 2:
#         res = "- đặt mua [{}](product_name) [{}](ram)".format(ten[random.randint(0,len(ten)-1)].strip('\n'),ram[random.randint(0,len(ram)-1)].strip('\n'))
#     if n == 3:
#         res = "- đặt mua [{}](product_name) [{}](rom) [{}](ram)".format(ten[random.randint(0,len(ten)-1)].strip('\n'),rom[random.randint(0,len(rom)-1)].strip('\n'),ram[random.randint(0,len(ram)-1)].strip('\n'))
#         res = "- đặt mua [{}](product_name) [{}](ram) [{}](rom)".format(ten[random.randint(0,len(ten)-1)].strip('\n'),ram[random.randint(0,len(ram)-1)].strip('\n'),rom[random.randint(0,len(rom)-1)].strip('\n'))
#     print(res)
# e1 = '{"entity":"price","role":"from_price"}'
# e2 = '{"entity":"price","role":"to_price"}'
for i in range(1,5):
    temp1 = ten[random.randint(0,len(ten)-1)].strip('\n')
    # temp2 = gia[random.randint(0,len(gia)-1)].strip('\n')
    # res = '- khoảng [{}]{}  [{}]{}'.format(temp1,e1,temp2,e2)
    res = '- đặt mua [{}](product_name) có được giao hàng không'.format(temp1)
    print(res)
for i in range(1,9):
    print(i*1000)
    print(i*1000000)
    print(i*1000+990)
    print(i*1000000+990)
    print(i*1000+500)
    print(i*1000+390)