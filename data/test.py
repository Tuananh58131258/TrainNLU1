
data = open('data/temp.txt',encoding='utf-8').readlines()
for item in data:
    if item.find("return \"") >-1:
        dat = item.strip(' ').split(" ")
        res = dat[1].replace("\"","").strip('\n')
        print("- {}\n{}".format(res,data[data.index(item)-2]))