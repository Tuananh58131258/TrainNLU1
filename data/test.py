import keyboard
import os
answer = open('data/temp.txt',encoding='utf-8').readlines()
question = open('data/data2.txt',encoding='utf-8').readlines()
# for item in data:
#     if item.find("return \"") >-1:
#         dat = item.strip(' ').split(" ")
#         res = dat[1].replace("\"","").strip('\n')
#         print("- {}\n{}".format(res,data[data.index(item)-2]))

# if 1 != 2:
#     print("dúng")
result = open("storie.txt",'a',encoding='utf-8')
temp = -1
index = 0
for item in answer:
    # strtemp = item.replace("action_","")
    index = temp
    for i in range(index + 1 ,len(question)-1):
        print(item)
        print(question[i])
        if keyboard.read_key() == 'y':
            result.write("## storie {0} * {0}  - {1}".format(question[i],item))
            temp = i
            os.system('cls')
            break

result.close()
print(len("Cấu hình của iphone 11 pro max 64 GB"))