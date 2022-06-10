import random
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import mysql.connector as sqlc

from mypfuncs import *

##################################### CONNECTING MySQL ################################

mydb = sqlc.connect(
    host="localhost",
    user="root",
    passwd="root",
)
mycur = mydb.cursor()

##################################### FUNCTIONS ################################

global opt_lp


def createDB():
    mycur.execute("CREATE DATABASE myp;")


def createTbls():
    # CREATING TWO TABLES myp_users and myp_data having a comman row userId
    mycur.execute("USE myp;")
    mycur.execute(
        """CREATE TABLE myp_users (
            userId INT  UNSIGNED PRIMARY KEY AUTO_INCREMENT,
            firstName VARCHAR(225) NOT NULL,
            lastName VARCHAR(225),
            userName VARCHAR(225) NOT NULL UNIQUE KEY,
            eMail VARCHAR(225) NOT NULL UNIQUE KEY,
            masterPass VARCHAR(225) NOT NULL); """
    )

    mycur.execute(
        """CREATE TABLE myp_data (
        passId INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
        website VARCHAR(625),
        loginName VARCHAR(225) NOT NULL,
        loginPass VARCHAR(225) NOT NULL,
        userId INT NOT NULL); """
    )


def insintousers(firstName, lastName, userName, eMail, masterPass):
    # this functions inserts data into the myp_user table
    mycur.execute("USE myp;")
    global passu
    passu = hashcrypt(masterPass)
    action = (
        f"""INSERT INTO myp_users (firstName, lastName, userName, eMail, masterPass)
        VALUES ("""
        + "TRIM('"
        + firstName
        + "'), "
        + "TRIM('"
        + lastName
        + "'), '"
        + userName
        + "', '"
        + eMail
        + "', '"
        + passu
        + "');"
    )
    mycur.execute(action)
    mydb.commit()


def insintodata(website, loginName, loginPass, userId):
    # this functions inserts data into the myp_data table
    mycur.execute("USE myp;")
    action = (
        f"""INSERT INTO myp_data (website, loginName, loginPass, userId) 
        VALUES ('"""
        + website
        + "', '"
        + loginName
        + "', '"
        + loginPass
        + "', '"
        + userId
        + "');"
    )
    mycur.execute(action)
    mydb.commit()


def otpmail(receivermail):
    # sends an otp to the receivermail
    global otp
    recmail = receivermail
    otp = random.randint(100000, 999999)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "OTP for Login"
    msg["From"] = "manageyourpass91@gmail.com"
    msg["To"] = recmail

    html = f"""
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
    </html>"""

    part = MIMEText(html, "html")
    msg.attach(part)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login("manageyourpass91@gmail.com", "Acc3ssGr@nted")
        server.send_message(msg)
        server.quit()
    return otp


def byemail(receivermail):
    # send a bye message to the user who leaves the app
    recmail = receivermail

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Thank you for using the app! "
    msg["From"] = "manageyourpass91@gmail.com"
    msg["To"] = recmail

    html = f"""<html>
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
    </html>"""

    part = MIMEText(html, "html")
    msg.attach(part)

    # context = ssl.create_default_context()
    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465,
    ) as server:  # context=context
        server.login("manageyourpass91@gmail.com", "Acc3ssGr@nted")
        server.send_message(msg)
        server.quit()
