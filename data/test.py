import re
data = "samsung galaxy z flip"

data = re.sub(r"^ip+(?=[\s])","iphone",data)
print(data)