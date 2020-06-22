# This is a simple module to fetch data from MySQL db.
# python -m pip install mysql-connector //run this command if you face import error
# references: https://www.w3schools.com/python/python_mysql_getstarted.asp

import mysql.connector
import traceback
import json


def getData(query:str):
        """
         @query: sql query that needs to be executed.
         returns the data being executed in "List" format
        """

        try:

            # Setup the connection.
            # Pass your database details here
            # mydb = mysql.connector.connect(
            #     host="localhost",
            #     user="root",
            #     passwd="1649",
            #     database="FPTShop",
            #     auth_plugin='caching_sha2_password'
            #     )
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database="fptshop",
                auth_plugin='caching_sha2_password'
                )
            # set up the cursor to execute the query
            cursor = mydb.cursor()
            cursor.execute(query)
            columns = cursor.description 
            results = [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
            # fetch all rows from the last executed statement using `fetchall method`.
            # results = cursor.fetchall()
            # row = dict(zip(cursor.column_names, cursor.fetchone()))
            # return row
            return results
        except:
            print("Error occured while connecting to database or fetching data from database. Error Trace: {}".format(traceback.format_exc()))
            return []

# test the file before integrating with the bot by uncommenting the below line.
obj = getData("SELECT * FROM fptshop.dienthoai;")
# count = 0
# total = len(obj)
# data = obj[48]['label'].split(':/')
# allin = list(data)
# data = obj[0]['data']
data = []
dem = 0
for item in obj:
    temp = item['label'].split(':/')
    if len(temp) >0:
        for i in temp:
            for item2 in data:
                if len(i) >=3 and i == item2:
                    dem = 1
                    break

            if dem == 0:
                data.append(i)
            else: dem = 0
print(len(data))
for item  in data:
    print(item)

# print(len(allin))
# print(obj[48]['ten'])
#         count = count + 1
# print("có {} sản phẩm có bảo hành tên {} sản phẩm".format(count,total))
# fobi = open('data/temp.txt','a',encoding='utf-8')
# for item in obj:
#     # print(obj[i]['ten'])
#     fobi.write(item['ten']+'\n')

# print(stri)