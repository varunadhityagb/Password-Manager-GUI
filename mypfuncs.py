######################## IMPORTING MODULES ###############################################
import random
from hashlib import *
from string import ascii_letters, ascii_lowercase, ascii_uppercase, digits
from tkinter import messagebox
import tkinter.ttk as ttk
from tkinter import *
from PIL import Image, ImageTk
import mysql.connector as sqlc
import requests
from os import system

# ProjectbyVarunAdhityaGB
######################## SQL Password ###############################################
def shbtn(cbvar, pass_ent):
    if (cbvar.get()) == 1:
        pass_ent.config(show="")
    else:
        pass_ent.config(show="•")


global mysql_password


def mysql_passd():
    def mps_enter(*e):
        global mysql_password
        try:
            mysql_password = mps_ent.get()
            mydb = sqlc.connect(
                host="localhost",
                user="root",
                passwd=mysql_password,
            )
            v1 = open("sqlp.txt", "w")
            v1.write(mysql_password)
            v1.flush()
            v1.close()
            getpass_sql.destroy()
            system("python main.py")

        except:
            messagebox.showerror("Authentication Error", "Wrong MYSQL Password!!")
            mps_ent.delete(0, END)

    getpass_sql = Tk()
    getpass_sql.wm_attributes("-topmost", True)
    getpass_sql.config(bg="#1e1e1e")
    getpass_sql.title("MySQL Password")
    getpass_sql.geometry("550x150")
    getpass_sql.resizable(0, 0)
    getpass_sql.iconbitmap("images\\1.ico")

    getpass_sql.tk.call('source', 'sv.tcl')
    getpass_sql.tk.call('set_theme', 'dark')

    mps_passkey = StringVar()
    mps_cbvar = IntVar(value=0)
    mps_lbl = ttk.Label(getpass_sql, text="Enter your MySQL Password :", font=("", 14))
    mps_ent = ttk.Entry(getpass_sql, textvariable=mps_passkey, show="•", font=("", 14))
    mps_btn = ttk.Button(
        getpass_sql,
        text="Enter",
        width=15,
        command=mps_enter,
    )
    mps_showpass_cb = ttk.Checkbutton(
        getpass_sql,
        text="Show Password",
        variable=mps_cbvar,
        onvalue=1,
        offvalue=0,
        command=lambda: shbtn(mps_cbvar, mps_ent),
        style="R.TCheckbutton",
    )

    mps_ent.bind("<Return>", mps_enter)

    mps_lbl.grid(row=0, column=0, padx=10, pady=10)
    mps_ent.grid(row=0, column=1, padx=10, pady=10)
    mps_showpass_cb.grid(row=1, column=1, padx=10)
    mps_btn.grid(row=2, column=0, columnspan=2, pady=10, padx=10)

    getpass_sql.mainloop()


try:
    p1 = open("sqlp.txt", "r")
    p1.close()

except:
    p = open("sqlp.txt", "w+")
    p.close()


######################## CONNECTING SQL ###############################################
try:
    p = open("sqlp.txt", "r")
    q = p.read()
    mydb = sqlc.connect(
        host="localhost",
        user="root",
        passwd=q,
    )
    mycur = mydb.cursor()

except:
    mysql_passd()


#########################   VARIABLES   ##################################################

# characters
lcase, ucase, num, alpha, pun = (
    list(ascii_lowercase),
    list(ascii_uppercase),
    list(digits),
    list(ascii_letters),
    ["!", "@", "#", "$", "%", "^", "&", "*", "-", "_", "/"],
)
charst = lcase + ucase + num

# defining encryption variables
lcase_crypt = [
    'M','L','W','U','Z','C','H','A','N','J','O','P','I','S','T','D','G','K','X','E','B','Y','R','Q','V','F'
    ]
ucase_crypt = [
    'm','w','f','l','s','n','o','i','d','a','g','e','u','h','p','r','y','k','q','c','x','b','v','z','j','t'
    ]
num_crypt = [
    '6', '4', '7', '8', '5', '2', '0', '3', '1', '9'
    ]
charst_crypt = lcase_crypt + ucase_crypt + num_crypt

#########################   FUNCTIONS   ##################################################
def shuffle(strg):
    # takes input as string and shuffles
    ls = list(strg)
    random.shuffle(ls)


def password(n: int):
    # takes in a the number of digits and returns the password of length digits
    char = [lcase, ucase, num, alpha, pun]

    # generating the password
    passwd = (
        random.choice(pun)
        + random.choice(lcase)
        + random.choice(ucase)
        + random.choice(alpha)
        + random.choice(num)
    )
    for i in range(n - 6):
        passwd += random.choice(random.choice(char))

    # Separating the password AND Checking
    passwd_l = list(passwd)

    if pun not in passwd_l:
        passwd_l.append(random.choice(pun))
    elif ucase not in passwd_l:
        passwd_l.append(random.choice(ucase))
    elif num not in passwd_l:
        passwd_l.append(random.choice(num))

    # shuffling the password
    shuffle(passwd_l)

    # Joining the password
    passwd = "".join(passwd_l)

    return passwd


def encrypt(strg: str):
    # takes input a string and returns a encrypted passwd
    str_ls = list(strg)
    for i in str_ls:

        if i in charst:
            i_pos = str_ls.index(i)
            c_pos = charst.index(i)
            str_ls[i_pos] = charst_crypt[c_pos]
        else:
            pass

    strg = "".join(str_ls)
    return strg


def decrypt(strg: str):
    ## takes input a string and returns a encrypted passwd
    str_ls = list(strg)
    for i in str_ls:

        if i in charst:
            i_pos = str_ls.index(i)
            c_pos = charst_crypt.index(i)
            str_ls[i_pos] = charst[c_pos]
        else:
            pass

    strg = "".join(str_ls)
    return strg


def hashcrypt(var: str):
    # it is a one time conversion which cannot be reverted back
    hash = md5(var.encode())
    hashc = hash.hexdigest()
    hash_crypt = encrypt(hashc)
    return hash_crypt


def emailvalidation(strg):
    """this functions checks whether the e-mail really exists
    with a help of a tool by isitrealemail.com"""
    try:
        api_key = "00209c5b-b82b-4c80-8db2-5621a90ff038"
        email = strg
        response = requests.get(
            "https://isitarealemail.com/api/email/validate",
            params={"email": email},
            headers={"Authorization": "Bearer" + api_key},
        )
        status = response.json()["status"]
        if status == "valid":
            return True
        elif status == "invalid":
            return False
        else:
            messagebox.showerror("Sorry for the inconvenience", "Please try tomorrow🙏🏼")
    except Exception:
        messagebox.showerror(
            "Network", "Please ensure that you are connected to the internet."
        )


def unamecheck(strg):
    """this function checks whether this username already exists,
    if it exists it tell the user to try a different username"""
    mycur.execute("USE myp;")
    username_ls = []
    mycur.execute("SELECT userName FROM myp_users;")

    for i in mycur:
        username_ls.extend(i)
    if (strg.upper() in username_ls) or (strg.lower() in username_ls):
        return False
    else:
        return True


def emailcheck(strg):
    """this functions checks whether the email address is already
    used ot not in our database"""
    mycur.execute("USE myp;")
    email_ls = []
    mycur.execute("SELECT eMail FROM myp_users;")
    data = mycur.fetchall()

    for i in data:
        email_ls.extend(i)

    if strg in email_ls:
        return False
    else:
        return True