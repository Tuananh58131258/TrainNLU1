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
# fobj = open('data/price.txt',encoding='utf-8')
# ram = open('data/temp.txt',encoding='utf-8').readlines()
# rom = open('data/rom.txt',encoding='utf-8').readlines()
# begin = ['điện thoại','máy','']
# data = fobj.readlines()
# ka = ['chíp','chip','cpu','chíp xử lý','chip xử lý','CPU','chíp đồ họa','card đồ họa','chíp đồ họa','card','gpu','GPU']
# end = ["chơi được liên quân không","chơi được pubg mobile không","chơi pubg ổn không","chơi liên quân mượt không"]
# end = ['gì đó','gì thôi','thôi']
# for i in range(1,15):
    # first = begin[random.randint(0,len(begin)-1)]
    # ra = ram[random.randint(0,len(ram)-1)].strip('\n')
    # ro = rom[random.randint(0,len(rom)-1)].strip('\n')
    # last = end[random.randint(0,len(end)-1)]
    # ten = data[random.randint(0,len(data))].strip('\n')
    # p1 = data[random.randint(0,len(data))].strip('\n')
    # p2 = data[random.randint(0,len(data))].strip('\n')
    # KAA= ka[random.randint(0,len(ka)-1)]
    # entity1 = '{"entity":"camera","role":"front"}'
    # entity2 = '{"entity":"camera","role":"behind"}'
    # entity = '{"entity":"hardware","role":"WHQ"}'
    # e1 = {"entity":"price","role":"from_price"}
    # e2 ={"entity":"price","role":"to_price"}
    # result = '- [{}]{} hay [{}]{} {}'.format(p1,e1,p2,e2,last)
    # n = random.randint(1,4)
    # if n == 1:
    #     result = '- [cam trước](camera) {} [{}](product_name) {}'.format(first,ten,last)
    # if n == 2:
    #     result = '- [camera trước](camera) {} [{}](product_name) {}'.format(first,ten,last)
    # if n == 3:
    #     result = '- [cam sau](camera) {} [{}](product_name) {}'.format(first,ten,last)
    # if n == 4:
    #     result = '- [camera sau](camera) {} [{}](product_name) {}'.format(first,ten,last)
    # print(result.replace("  "," "))
# fobj.close()
# count = 0
# pc = ['Iphone','Sanmsung','Oppo','Huawei','Xiaomi','Realme','Nokia','Vsmart','Vivo','Masstel','Itel','Energizer','ss','ip']
# data = open('data/temp.txt',encoding='utf-8').readlines()
# p1 = ['có điện thoại','có','có cái']
# for item in data:
#     if item.find("intent") > -1:
#         i = data.index(item)
#         intent = item.split(":")
#         res = "- {}".format(intent[1])
#         note = data[i+1].replace("<!--","# ").replace("-->","")
#         print(res.strip('\n'))
#         print(note.strip('\n'))
# for item in data:
    # sss = p1[random.randint(0,2)]
    # psc = pc[random.randint(0,len(pc)-1)]
    # end = data[random.randint(0,len(data)-1)]
    # res = "- {} [{}](product_company) {}".format(sss,psc,item.strip('\n'))
    # print(res)
# print(count)
# res = ''
# obj = open('data/stmm.txt','a',encoding='utf-8')
# for item in data:
    # temp = item.strip('\n').split(":")
    # res = res + '{} = scrapy.Field()\n'.format(temp[1])
    # obj.write(res.strip('\n'))

# obj.close()
# print(res)
sdt = open('data/phonenum.txt').readlines()
ten = open('data/fullname.txt',encoding='utf-8').readlines()
p =['họ tên:','tên:','họ và tên:','']
m =['sđt:','sdt:','','số điện thoại:','đt:','dt:','điện thoại:']
# a = ["059","099","092","056","058","082","081","085","084","083","094","091","088","089","090","093","070","079","077","076","078","033","034","035","036","037","038","039","032","098","097","096","086"]
for i in range(1,200):
    phonenum = sdt[random.randint(0,len(sdt)-1)].strip('\n')
    name = ten[random.randint(0,len(ten)-1)].strip('\n')
    res = "- {} [{}](customer_name) {} [{}](phone_num)".format(p[random.randint(0,len(p)-1)],name,m[random.randint(0,len(m)-1)],phonenum)
    print(res.replace("  "," "))