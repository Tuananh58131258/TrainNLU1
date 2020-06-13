import random
# truoc = ['máy có','máy này có','điện thoại này có']
# sau = ['không ạ','ko vậy','không','không ad']
# fobj = open('data/hardware.txt',encoding='utf-8')
# def printresult(index:str,TF:str,temp:str):
#     template = {"màn hình+":{"có":"ở đây có {}".format(temp),"không":"ở đây không có {}".format(temp)},
#                 "b-":{"có":"ở đây có {}".format(temp),"không":"ở đây không có {}".format(temp)},
#                 "c":{"có":"ở đây có {}".format(temp),"không":"ở đây không có {}".format(temp)}}
    # return template[index][TF]
    # asjhdaskdasd

# print(printresult('màn hình+','không',"wifi"))
# data = ['wifi','vào mạng được','3G','4G']

# for i in range(1,13):
#     res = "\n{0} tháng\n{0}t\n{0} thang".format(i)
#     fobj.write(res)
# fobj.close()
fobj = open('data/product_name.txt',encoding='utf-8')
ram = open('data/temp.txt',encoding='utf-8').readlines()
# rom = open('data/rom.txt',encoding='utf-8').readlines()
begin = ['có','có bản','ở đây có','ad ơi có']
data = fobj.readlines()
# ka = ['chíp','chip','cpu','chíp xử lý','chip xử lý','CPU','chíp đồ họa','card đồ họa','chíp đồ họa','card','gpu','GPU']
end = ["không","không vậy","không nhỉ"]
for i in range(1,30):
    first = begin[random.randint(0,len(begin)-1)]
    ra = ram[random.randint(0,len(ram)-1)].strip('\n')
    # ro = rom[random.randint(0,len(rom)-1)].strip('\n')
    last = end[random.randint(0,len(end)-1)]
    ten = data[random.randint(0,len(data))].strip('\n')
    # KAA= ka[random.randint(0,len(ka)-1)]
    # entity1 = '{"entity":"camera","role":"front"}'
    # entity2 = '{"entity":"camera","role":"behind"}'
    # entity = '{"entity":"hardware","role":"WHQ"}'
    result = '- {} [{}](product_name) {} {}'.format(first,ten,ra,last)
    # n = random.randint(1,4)
    # if n == 1:
    #     result = '- [cam trước](camera) {} [{}](product_name) {}'.format(first,ten,last)
    # if n == 2:
    #     result = '- [camera trước](camera) {} [{}](product_name) {}'.format(first,ten,last)
    # if n == 3:
    #     result = '- [cam sau](camera) {} [{}](product_name) {}'.format(first,ten,last)
    # if n == 4:
    #     result = '- [camera sau](camera) {} [{}](product_name) {}'.format(first,ten,last)
    print(result.replace("  "," "))
fobj.close()
# count = 0
# data = open('data/nlu.md',encoding='utf-8').readlines()
# for item in data:
#     if item.find("intent") > -1:
#         count = count +1
#         intent = item.split(":")
#         res = "- {}".format(intent[1])
#         print(res.strip('\n'))

# print(count)