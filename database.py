import mysql.connector as sqlc
from mypfuncs import *
from pwinput import pwinput
import os
import sys
import smtplib, ssl, email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import time
from tabulate import tabulate

##################################### CONNECTING MySQL ################################

mydb = sqlc.connect(host='localhost', user='root', passwd='root',)
mycur = mydb.cursor()

##################################### FUNCTIONS ################################

global opt_lp

def createDB():
    mycur.execute("CREATE DATABASE MYP;")

def createTbls():
    #CREATING TWO TABLES myp_users and myp_data having a comman row userId
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
    # this functions inserts data into the myp_user table
    mycur.execute("USE MYP;")
    global passu
    passu = hashcrypt(masterPass)
    action = f"""INSERT INTO myp_users (firstName, lastName, userName, eMail, masterPass)
        VALUES (""" + "TRIM('" + firstName + "'), " + "TRIM('" + lastName + "'), '" + userName + "', '" + eMail + "', '" + passu + "');"
    mycur.execute(action)
    mydb.commit()

def insintodata(website, loginName, loginPass, userId):
    # this functions inserts data into the myp_data table
    mycur.execute("USE MYP;") 
    action = f"""INSERT INTO myp_data (website, loginName, loginPass, userId) 
        VALUES ('""" + website + "', '" + loginName + "', '" + loginPass + "', '" + userId + "');"
    mycur.execute(action)
    mydb.commit()

def retrieve(n: int):
    # this fucntion retrives data from the myp_data table
    # given that the userId is given 
    mycur.execute("USE MYP;")
    mycur.execute("SET @ROW := 0 ;")
    mycur.execute(f"""SELECT @ROW := @ROW + 1 , loginName
    FROM myp_data
    WHERE userId = {n};""") 
    data = mycur.fetchall()

    mycur.execute(f"""SELECT loginPass
    FROM myp_data
    WHERE userId = {n};""") 
    data_ls = mycur.fetchall()
    
    ls = []
    for i in data_ls:
        ls.extend(i)   
    datadict = {}
    for j in range(len(ls)):
        datadict[j+1] = ls[j]

    if datadict != {}:
        print(tabulate(data, headers=['Sl.No.', 'Username'], tablefmt='psql'))
        print("Enter the number corresponding to the website to check the password:")   
        datain = int(input())
        print()
        print()
        print(decrypt(datadict[datain]))
        pyperclip.copy(decrypt(datadict[datain]))
        print()
        print()
        print("YOUR PASSWORD IS COPIED TO YOUR CLIPBOARD🙂")
    else:
        print("THERE ARE NO PASSWORDS SAVED FOR THIS USER.")
    time.sleep(5)
    post_login() 

def deletedata(n: int):
    # this fucntion deletes data from the myp_data table
    # given that the userId is given 
    mycur.execute("USE myp;")
    mycur.execute("SET @ROW := 0")
    mycur.execute(f"""SELECT @ROW := @ROW + 1 , loginName
    FROM myp_data
    WHERE userId = {n};""") 
    data = mycur.fetchall()

    mycur.execute(f"""SELECT passId
    FROM myp_data
    WHERE userId = {n};""") 
    data_ls = mycur.fetchall()
    
    ls = []
    for i in data_ls:
        ls.extend(i)

    datadict = {}
    for j in range(len(ls)):
        datadict[j+1] = ls[j]

    if datadict != {}:
        print(tabulate(data, headers=['Sl.No.', 'Username'], tablefmt='psql'))
        print("Enter the number corresponding to the website to delete the record:")   
        datain = int(input())
        dataout = datadict[datain]
        print()
        action = f"DELETE FROM myp_data WHERE (passId = {dataout});"
        mycur.execute(action)
        mydb.commit()
        print("SUCCESSFULLY DELETED THE SELECTED RECORD")
    else:
        print("THERE ARE NO PASSWORDS SAVED FOR THIS USER.")
    time.sleep(5)
    post_login()

def deleteuser(n: int):
    # this fucntion deletes user from the myp_users table
    print("Are you sure you want to delete your account? ")
    deleinp = input("Y/N ? ")
    if deleinp.upper() == 'Y':
        mycur.execute("USE myp;")

        mycur.execute("USE myp;")
        mycur.execute(f"""SELECT eMail
        FROM myp_users
        WHERE userId = {n}""")
        emaild = mycur.fetchall()

        els = []
        for i in emaild:
            els.extend(i)

        mycur.execute(f"""SELECT passId 
        FROM myp_data 
        WHERE userId = {n};""")
        data = mycur.fetchall()

        ls = []
        for i in data:
            ls.extend(i)
        
        for i in ls:
            mycur.execute(f"""DELETE FROM myp_data
            WHERE (passId = {i});""")
            mydb.commit()
        
        mycur.execute(f"""DELETE FROM myp_users 
        WHERE (userId = {n});""")
        mydb.commit()

        print("Successfully deleted your details and data from our database")
        byemail(els[0])     
        time.sleep(5)
        login_page()

    elif deleinp.upper() == 'N':
            print("Let me tell you a secret..........")
            time.sleep(1)
            print("YOU ARE ALWAYS RIGHT IN MAKING DECISIONS!!")
            print("🙂🙂🙂🙂🙂🙂")   
            time.sleep(5)
            post_login()

def insert(usr):
    # this function inserts data into the myp_data table along with the help
    # of inintodata() function 
    web = input("Web address:  ")
    logName = input(f"Enter username in {web}: ")
    logPass = encrypt(pwinput(f"Enter the password for {logName}: "))
        
    #masterpass checking
    uId = str(usr)
    mycur.execute("USE MYP;")
    action = f"""SELECT masterPass FROM myp_users WHERE userId = {uId}"""
    mycur.execute(action)
                
    for i in mycur:
        u = str(i[0])

    hello = False
    while hello is False:
        mp = str(pwinput("Enter your Master Password: "))           
        hash = md5(mp.encode())
        hashd = hash.hexdigest()
        hash_crypt = encrypt(hashd)
        mp_verify = hash_crypt

        if mp_verify == u:
            hello = True
            insintodata(web, logName, logPass, uId)
            
        else:
            print("PLEASE DOUBLE CHECK YOUR PASSWORD AS THERE IS NO USER IN OUR DATABASE WITH THIS PASSWORD")
            hello = False

def otpmail(receivermail):
    # sends an otp to the receivermail  
    global otp
    recmail = receivermail
    otp = random.randint(100000, 999999)

    msg = MIMEMultipart("alternative")
    msg['Subject'] = 'OTP for Login'
    msg['From'] = 'manageyourpass91@gmail.com'
    msg['To'] = recmail

    html = (f"""
    <html>
        <body>
            <p style="font-size:300%; text-align: center;"><b>Verification Code</b></p>
            <h1 style="text-align:center; font-size:300%;">{otp}</h1>
            <p style="font-size:160%; text-align: center;">
            Here is your one time password (OTP) Verification Code to
            login. This OTP is valid for 5 minutes only.
            <br>
            Thank you for trying our password manager.
            Hope you like our product.
            </p>
        </body>
    </html>""")
    
    part = MIMEText(html, "html")
    msg.attach(part)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context ) as server:  
        server.login('manageyourpass91@gmail.com','Acc3ssGr@nted')
        server.send_message(msg)
        server.quit()
    
def byemail(receivermail):
    #send a bye message to the user who leaves the app
    recmail = receivermail

    msg = MIMEMultipart("alternative")
    msg['Subject'] = 'Thank you for using the app! '
    msg['From'] = 'manageyourpass91@gmail.com'
    msg['To'] = recmail

    html = (f"""<html>
        <body>
            <p style="font-size:300%; text-align: center;"><b>SORRY TO SEE YOU GO ☹️☹️</b></p>
            <p style="font-size:160%; text-align: center;">
            Hope you use our app some another day again.
            <br>
            Thank you for trying our password manager.
            Hope you liked our product.
            </p>
            <h1 style="text-align:center; font-size:300%;">THANK YOU!!</h1>
        </body>
    </html>""")
    
    part = MIMEText(html, "html")
    msg.attach(part)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context ) as server:  
        server.login('manageyourpass91@gmail.com','Acc3ssGr@nted')
        server.send_message(msg)
        server.quit()

def login():
    #displays a list of the users singed up
    global user
    os.system('clear')
    mycur.execute("USE MYP;")
    mycur.execute("SET @ROW := 0 ;")
    mycur.execute(f"""SELECT @ROW := @ROW + 1 , userName FROM myp_users;""") 
    data = mycur.fetchall()

    mycur.execute(f"""SELECT userName FROM myp_users""") 
    data_ls = mycur.fetchall()
    
    ls = []
    for i in data_ls:
        ls.extend(i)
    print(ls)   
    datadict = {}
    for j in range(len(ls)):
        datadict[j+1] = ls[j]
    print(datadict)

    # ask the user to select which user wants to sign in
    if datadict != {}:
        print(tabulate(data, headers=['Sl.No.', 'Username'], tablefmt='psql'))
        print("Enter the number corresponding to the user name to login: ")   
        datain = int(input())
        uname_srch = datadict.get(datain)
        mycur.execute(f"SELECT userId FROM myp_users WHERE userName = '{uname_srch}';")
        user_ls = []
        for i in mycur:
            user_ls.extend(i)
        
        user = user_ls[0]
        mycur.execute(f"SELECT masterPass FROM myp_users WHERE userName = '{uname_srch}';")
        
        pass_ls = []
        for i in mycur:
            pass_ls.extend(i)
        
        #asks the masterpass for the selected user
        ch = False
        while ch == False:
            masterPass_check_hash = hashcrypt(pwinput("Password: "))
            if masterPass_check_hash == pass_ls[0]: 
                ch = True 
                post_login()
            else:
                print("Access Denied")
        pass_ls = []

def signup():
    #asks users their details and a masterpass for signing up
    w = 't'
    fName = input("Enter your first name:")
    lName = input("Enter your last name:")
        
    ############ USER NAME CHECK
    mycur.execute("USE MYP;")
    username_ls = []
    mycur.execute("SELECT userName FROM myp_users;")
    for i in mycur:
        username_ls.extend(i)

    if username_ls == []:
        uName = input("Enter your username:")
    else:
        usName = input("Enter your username:")
        while unamecheck(usName) is False:
            print("THIS USERNAME ALREADY EXISTS !!!")
            usName = input("Enter another username: ")

        uName = usName
        
    ############ EMAIL CHECK
    email_ls = []
    mycur.execute("SELECT eMail FROM myp_users;")
    for i in mycur:
        email_ls.extend(i)
    
    if email_ls == []:
        eMail = input("Enter your e-mail address:")
        while emailvalidation(eMail) is False:
            print('INVALID EMAIL ID !!')
            eMail = input("Enter a vaild e-mail address:") 
    else:        
        e_Mail = input("Enter your e-mail address:")
        while emailvalidation(e_Mail) is False:
            print('INVALID EMAIL ID !!')
            e_Mail = input("Enter a vaild e-mail address:") 

        if emailcheck(e_Mail) is False:
            print("There is another account linked with this e-mail address")
            eMail = input("Enter your e-mail address: ")
        else:
            eMail = e_Mail

    #optmail() function is triggered
    # to check whether the given mail is the user's mail
    otpmail(eMail)
    otp_opt = False
    otp_count = 0 
    while otp_opt == False:
        otp_check = int(input("Enter the OTP recieved on your registered email: "))
        if otp_check != otp:
            otp_count += 1
            otp_check = int(input("Please double check your OTP: "))
            if otp_count > 1:
                os.system('clear')
                print('Resend OTP?')
                c = int(input("1.Yes\n2.No\n3.Exit"))
                if c == 1:
                    otpmail(fName + ' ' + lName, eMail)
                elif c == 2:
                    otp_check = int(input("Enter the correct OTP: "))
                else:
                    sys.exit
            elif otp_count > 3:
                print("Need help?")
                print('Forgot your registered email address?')
                d = int(input("1.Yes\n2.No"))
                if d == 1:
                    print(f"Your email address is {eMail}")
                    otp_check = int(input("Now enter the correct OTP: "))
                else:
                    otp_check = int(input("Enter the correct OTP: "))
        else:
            otp_opt = True
    

    ############ password
    while w == 't':
        masterPass = pwinput("New Password: ")
        masterPass_check = pwinput("Re-enter Password: ")
        print(""" REMEMBER !!!!!!
        THIS IS YOUR MASTER PASSWORD
        IF YOU FORGET THIS PASSWORD YOU KNOW WHAT HAPPENS😐""")
        if masterPass_check == masterPass:    
            insintousers(fName, lName, uName, eMail, masterPass)
            break
        else:
            print("YOUR PASSWORDS DON'T MATCH!")

    time.sleep(9)
    os.system('clear')
    login()

def login_page():
    # this is the first page when u run the program
    # it asks the user whether they are signing in or creating their account
    os.system('clear')

    print('''-----------MENU-----------
    1. Login
    2. Sign Up
    3. Exit''')

    opt_lp = int(input(""))
    
    if opt_lp == 1:
        login()
        
    elif opt_lp == 2:
        signup()        

    elif opt_lp == 3:
        os.system('clear')
        sys.exit            

def post_login():

    # as the functions name defines this is the second page post login
    os.system('clear')

    print('''-----------MENU-----------
    1. Retrieve Password\t2. Store Password
    3. Generate Password\t4. Remove Passwords
    5. Log Out\t\t\t6. Delete User
    7. Exit''')

    opt = int(input())
    if opt == 1:
        os.system('clear')
        retrieve(user)

    elif opt == 2:
        insert(user)

        time.sleep(2)
        post_login()

    elif opt == 3:
        os.system('clear')
        print("""-----------MENU-----------
    1. Only generate password?
    2. Or save it too?
    3. Go Back
    4. Exit""")

        opt_lp = int(input())
        if opt_lp == 1:
            generate_pass()

            time.sleep(7)
            post_login()
            
        elif opt_lp == 2:
            insert(user)

            time.sleep(7)
            post_login()

        elif opt_lp == 3:
            post_login()

        elif opt_lp == 4:
            sys.exit
    
    elif opt == 4:
        deletedata(user)

        time.sleep(7)
        post_login()
    
    elif opt == 5:
        os.system('clear')
        login_page()

    elif opt == 7:
        os.system('clear')   
        sys.exit
    
    elif opt == 6:
        deleteuser(user)