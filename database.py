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
    mycur.execute("CREATE DATABASE myp;")

def createTbls():
    #CREATING TWO TABLES myp_users and myp_data having a comman row userId
    mycur.execute("USE myp;") 
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
    mycur.execute("USE myp;")
    global passu
    passu = hashcrypt(masterPass)
    action = f"""INSERT INTO myp_users (firstName, lastName, userName, eMail, masterPass)
        VALUES (""" + "TRIM('" + firstName + "'), " + "TRIM('" + lastName + "'), '" + userName + "', '" + eMail + "', '" + passu + "');"
    mycur.execute(action)
    mydb.commit()

def insintodata(website, loginName, loginPass, userId):
    # this functions inserts data into the myp_data table
    mycur.execute("USE myp;") 
    action = f"""INSERT INTO myp_data (website, loginName, loginPass, userId) 
        VALUES ('""" + website + "', '" + loginName + "', '" + loginPass + "', '" + userId + "');"
    mycur.execute(action)
    mydb.commit()

def retrieve(n: int):
    pass

def deletedata(n: int):
    pass

def deleteuser(n: int):
    pass

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

    #context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:  #, context=context 
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

    #context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465,) as server:  #context=context
        server.login('manageyourpass91@gmail.com','Acc3ssGr@nted')
        server.send_message(msg)
        server.quit()

def signup():
    #asks users their details and a masterpass for signing up
    w = 't'
    fName = input("Enter your first name:")
    lName = input("Enter your last name:")
        
    ############ USER NAME CHECK
    mycur.execute("USE myp;")
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
    #login()
