import mysql.connector as sqlc
from PasswFun import *
##################################### CREATING DATABASE ################################

mydb = sqlc.connect(host='localhost', user='root', passwd='root',)
mycur = mydb.cursor()
def createDB():
    mycur.execute("CREATE DATABASE IF NOT EXISTS MYP;")

##################################### CREATING TABLES ################################

def createTbls():
    mycur.execute("USE MYP;") 
    mycur.execute('''CREATE TABLE myp_users (
            userId INT  UNSIGNED PRIMARY KEY AUTO_INCREMENT,
            firstName VARCHAR(225) NOT NULL,
            lastName VARCHAR(225),
            userName VARCHAR(225) NOT NULL UNIQUE KEY,
            eMail VARCHAR(225) NOT NULL UNIQUE KEY,
            masterPass VARCHAR(225) NOT NULL); ''')

    mycur.execute('''CREATE TABLE myp_data (
        passId INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
        website VARCHAR(225),
        loginName VARCHAR(225) NOT NULL,
        loginPass VARCHAR(225) NOT NULL,
        userId INT NOT NULL); ''')

def insintousers(firstName, lastName, userName, eMail, masterPass):
    mycur.execute("USE MYP;")
    global passu
    passu = hashcrypt(masterPass)
    action = f"""INSERT INTO myp_users (firstName, lastName, userName, eMail, masterPass)
        VALUES ('""" + firstName + "', '" + lastName + "', '" + userName + "', '" + eMail + "', '" + passu + "');"
    mycur.execute(action)
    mydb.commit()


def insintodata(website, loginName, loginPass, userId):
    mycur.execute("USE MYP;") 
    global passd
    passd = hashcrypt(loginPass)
    action = f'''INSERT INTO myp_data (website, loginName, loginPass, userId)
        VALUES ({website}, {loginName}, {passd}, {userId});'''
    mycur.execute(action)
    mydb.commit()

