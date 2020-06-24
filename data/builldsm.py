import random
ten = open('data/product_name.txt',encoding='utf-8').readlines()
ram = open('data/ram.txt',encoding='utf-8').readlines()
rom = open('data/rom.txt',encoding='utf-8').readlines()

for i in range(0,30):
    n = random.randint(1,3)
    if n == 1:
        res = "- đặt mua [{}](product_name) [{}](rom)".format(ten[random.randint(0,len(ten)-1)].strip('\n'),rom[random.randint(0,len(rom)-1)].strip('\n'))
    if n == 2:
        res = "- đặt mua [{}](product_name) [{}](ram)".format(ten[random.randint(0,len(ten)-1)].strip('\n'),ram[random.randint(0,len(ram)-1)].strip('\n'))
    if n == 3:
        res = "- đặt mua [{}](product_name) [{}](rom) [{}](ram)".format(ten[random.randint(0,len(ten)-1)].strip('\n'),rom[random.randint(0,len(rom)-1)].strip('\n'),ram[random.randint(0,len(ram)-1)].strip('\n'))
        res = "- đặt mua [{}](product_name) [{}](ram) [{}](rom)".format(ten[random.randint(0,len(ten)-1)].strip('\n'),ram[random.randint(0,len(ram)-1)].strip('\n'),rom[random.randint(0,len(rom)-1)].strip('\n'))
    print(res)