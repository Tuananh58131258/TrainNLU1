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
# for i in range(1,30):
#     TR = truoc[random.randint(0,len(truoc)-1)]
#     S = sau[random.randint(0,len(sau)-1)]
#     mid = data[random.randint(0,len(data)-1)].strip('\n')
#     res = "- {} [{}](hardware) {}".format(TR,mid,S)
#     print(res)

# begin = ['sản phẩm này có','máy này có','điện thoại này có','máy có','có','dùng được']
# data =['wifi','gprs','3g','4g','edge','nfc','bluetooth','gps','đèn pin','đèn flash']
# end = ["không","không ạ","không vậy","không ad"]
# for i in range(1,30):
#     I = begin[random.randint(0,len(begin)-1)]
#     II = data[random.randint(0,len(data)-1)]
#     III = end[random.randint(0,len(end)-1)]
#     IV = '{"entity":"hardware","role":"YorN"}'
#     result = '- {} [{}]{} {}'.format(I,II,IV,III)
#     print(result)

data = open('data/nlu.md',encoding='utf-8').readlines()
for item in data:
    if item.find("intent") > -1:
        intent = item.split(":")
        res = "- {}".format(intent[1])
        print(res.strip('\n'))

