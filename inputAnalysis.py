import re


def productNameAnalysis(productName: str):
    data = productName.lower()
    if data.find("ip") > -1 and data.find("iphone") == -1:
        temp = data.replace("ip", "iphone")
        return temp
    elif data.find("ss") > -1 and data.find("galaxy") == -1:
        temp = data.replace("ss", "samsung galaxy")
        return temp
    elif data.find("samsung") > -1 and data.find("galaxy") == -1:
        temp = data.replace("samsung", "samsung galaxy")
        return temp
    elif data.find("ss") > -1 and data.find("galaxy") > -1:
        temp = data.replace("ss", "samsung")
        return temp

    return data


def romramAnalysis(rom: str):
    data = rom.lower()
    if data.find("gb") > -1 and data.find(" ") == -1:
        temp = data.replace("gb", " gb")
        return temp

    if data.find("gb") == -1 and data.find(" ") == -1 and data.find("g") > -1:
        temp = data.replace("g", " gb")
        return temp
    return data


def priceAnalysis(price: str):
    data = price.lower().strip(" ").replace("lăm", "5").replace("mốt", "1").replace("tư", "4").replace(" ", "").replace(".", ",").replace("rưởi","5")
    word = ['một', 'hai', 'ba', 'bốn', 'năm', 'sáu', 'bảy', 'tám', 'chín']
    result = 0
    for i in range(0, 9):
        data = data.replace(word[i], str(i+1))
    # specialword = ["m","tr","trịu","trieu"]
    # for item in specialword:
        # data = data.replace(item,"triệu")
    if re.match("[0-9]mươi[0-9].", data):
        data = data.replace('mươi','')
    if re.match("[0-9]mươi[^0-9]",data):
        data = data.replace('mươi','0')

    if re.match("[0-9]+triệu[0-9]+", data) or re.match("[0-9]+m[0-9]+", data) or re.match("[0-9]+tr[0-9]+", data):
        temp = data.replace("triệu", ".").replace("tr",".").replace("m",".")
        # print(temp)
        num = temp.split(".")
        # print(num)
        if len(num[1]) == 1:
            result = int(num[0])*1000000+int(num[1])*100000
        if len(num[1]) == 2:
            result = int(num[0])*1000000+int(num[1])*10000
        if len(num[1]) == 3:
            result = int(num[0])*1000000+int(num[1])*1000
        return result
    elif re.match("[0-9]+,[0-9]+triệu", data) or re.match("[0-9]+,[0-9]+m", data) or re.match("[0-9]+,[0-9]+tr", data):
        temp = data.replace("triệu", "").replace("tr",".").replace("m",".")
        num = temp.split(".")
        # print(len(num[1]))
        if len(num[1]) == 1:
            result = int(num[0])*1000000+int(num[1])*100000
        if len(num[1]) == 2:
            result = int(num[0])*1000000+int(num[1])*10000
        if len(num[1]) == 3:
            result = int(num[0])*1000000+int(num[1])*1000
        return result
    elif re.match("[0-9]+triệu", data) or re.match("[0-9]+m", data) or re.match("[0-9]+tr", data):
        temp = data.replace("triệu", "").replace("tr","").replace("m","")
        # num = temp.split(".")
        # # print(len(num[1]))
        # if len(num[1])==1:
        #     result = num[0]+"."+num[1]+"00.000"
        # if len(num[1])==2:
        #     result = num[0]+"."+num[1]+"0.000"
        # if len(num[1])==3:
        result = int(temp)*1000000
        return result

    return data

def PrepayPercent(temp:str):
    res_tmp = temp.replace(" ","").replace("%","").strip('\n')
    res = int(res_tmp)
    return res

def InstallmentPaymentPeriod(temp:str):
    res = int(temp.isdigit())
    return res

def RoundNum(temp:int):
    res = round(temp/10000)*10000
    return res
# print("{:,}".format(priceAnalysis("0 mươi  2 triệu")))
# print(RoundNum(809216))