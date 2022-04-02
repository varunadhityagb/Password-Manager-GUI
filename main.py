import PasswFun
import mysql.connector as sqlc

mydb = sqlc.connect(host='localhost', user='root', passwd='root', database = 'mypusers')
mycur = mydb.cursor()