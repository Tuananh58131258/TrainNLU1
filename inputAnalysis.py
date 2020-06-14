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
    data = price.lower().strip(" ").replace("mươi", "").replace("lăm", "5").replace(
        "mốt", "1").replace("tư", "4").replace(" ", "").replace(".", ",").replace("rưởi","5")
    word = ['một', 'hai', 'ba', 'bốn', 'năm', 'sáu', 'bảy', 'tám', 'chín']
    for i in range(0, 9):
        data = data.replace(word[i], str(i+1))
    # specialword = ["m","tr","trịu","trieu"]
    # for item in specialword:
        # data = data.replace(item,"triệu")
    if re.match("[1-9]*triệu[1-9]*", data) or re.match("[1-9]*m[1-9]*", data) or re.match("[1-9]*tr[1-9]*", data):
        temp = data.replace("triệu", ".").replace("tr",".").replace("m",".")
        # print(temp)
        num = temp.split(".")
        # print(num)
        if len(num[1]) == 1:
            result = num[0]+"."+num[1]+"00.000"
        if len(num[1]) == 2:
            result = num[0]+"."+num[1]+"0.000"
        if len(num[1]) == 3:
            result = num[0]+"."+num[1]+".000"
        return result
    elif re.match("[1-9]*,[1-9]*triệu", data) or re.match("[1-9]*,[1-9]*m", data) or re.match("[1-9]*,[1-9]*tr", data):
        temp = data.replace("triệu", "").replace("tr",".").replace("m",".")
        num = temp.split(".")
        # print(len(num[1]))
        if len(num[1]) == 1:
            result = num[0]+"."+num[1]+"00.000"
        if len(num[1]) == 2:
            result = num[0]+"."+num[1]+"0.000"
        if len(num[1]) == 3:
            result = num[0]+"."+num[1]+".000"
        return result
    elif re.match("[1-9]*triệu", data) or re.match("[1-9]*m", data) or re.match("[1-9]*tr", data):
        temp = data.replace("triệu", "").replace("tr",".").replace("m",".")
        # num = temp.split(".")
        # # print(len(num[1]))
        # if len(num[1])==1:
        #     result = num[0]+"."+num[1]+"00.000"
        # if len(num[1])==2:
        #     result = num[0]+"."+num[1]+"0.000"
        # if len(num[1])==3:
        result = temp+".000.000"
        return result

    return data


print(priceAnalysis("3.500"))
