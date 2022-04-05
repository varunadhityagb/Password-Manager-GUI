from mypfuncs import *
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
    action = f"""INSERT INTO myp_users (website, loginName, loginPass, userId) 
        VALUES ('""" + website + "', '" + loginName + "', '" + passd + "', '" + userId + "');"
    mycur.execute(action)
    mydb.commit()

def login_page():
    print('''-----------MENU-----------
    1. Login
    2. Sign Up
    3. Exit''')

    opt = int(input(""))
    os.system('clear')
    if opt == 1:
        pass
    elif opt == 2:
        w = 't'
        fName = input("Enter your first name:")
        lName = input("Enter your last name:")
        uName = input("Enter your username:")
        while unamecheck(uName) is False:
            print("Please enter valid characters. \n Only @ and _ are the special characters allowed.")
            uName = input("Enter your username:")
        eMail = input("Enter your first name:")
        while w == 't':
            masterPass = getpass("New Password: ")
            masterPass_check = getpass("Re-enter Password: ")
            if masterPass_check == masterPass:    
                insintousers(fName, lName, uName, eMail, masterPass)
                break
            else:
                print("Your passwords don't match!")
    elif opt == 3:
        sys.exit            



