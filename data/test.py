import re
# data = "samsung galaxy z flip"

# data = re.sub(r"^ip+(?=[\s])","iphone",data)
# print(data)
data = {"a1":"abc1","a2":"abc2","a3":"abc3","a4":"abc4","a5":"abc5"}
for item in data:
    print(data.__getitem__(item))