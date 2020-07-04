# This is a simple module to fetch data from MySQL db.
# python -m pip install mysql-connector //run this command if you face import error
# references: https://www.w3schools.com/python/python_mysql_getstarted.asp

import mysql.connector
import traceback
import json
import re

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
# data = open('data/product_name.txt','a',encoding='utf-8')
# obj = getData("select * from dienthoai where idDienThoai  = 19")
# temp = ""
# for item in obj:
    # temp = item['ten'].replace('-',' ')
    # x = re.findall(r'[0-9]{1,3}GB', temp)
    # for i in x:
        # temp =  temp.replace(i,"")
    # # try:
    # data.write(temp.replace("pp",'p').strip(' ')+'\n')
    # data.write(temp.strip(' ').replace('Xiaomi','')+'\n')
    #     data.write(temp.strip(' ').replace('Galaxy','')+'\n')
    # except:
    #     print("không ghi đc {}".format(temp))
    # print(temp.strip(' '))
    # print(temp.strip(' ').replace('Samsung Galaxy','ss')+'\n')
    # print(temp.strip(' ').replace('Galaxy','')+'\n')
# data.close()


