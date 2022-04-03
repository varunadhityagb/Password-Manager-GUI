import mysql.connector as sqlc

mydb = sqlc.connect(host='localhost', user='root', passwd='root',)
mycur = mydb.cursor()
mycur.execute("CREATE DATABASE IF NOT EXISTS MYP;")




