######################## IMPORTING MODULES ############################
import csv
from turtle import bgcolor
import mysql.connector as sqlc
import pyautogui as pg
import random
import requests
import smtplib
import ssl
import sv_ttk as sv 
import sys
import time
import tkinter.ttk as ttk
from email import message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from hashlib import *
from os import system
from string import ascii_letters, ascii_lowercase, ascii_uppercase, digits
from tkinter import *
from PIL import ImageTk, Image
from tkinter.font import Font as fnt
from tkinter import filedialog, messagebox
from tkinter.font import BOLD



# ProjectbyVarunAdhityaGB
#########################   VARIABLES   ##############################

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
              'M','L','W','U','Z','C','H','A','N','J','O','P','I','S',
              'T','D','G','K','X','E','B','Y','R','Q','V','F'
              ]
ucase_crypt = [
              'm','w','f','l','s','n','o','i','d','a','g','e','u','h',
              'p','r','y','k','q','c','x','b','v','z','j','t'
              ]
num_crypt = [
            '6', '4', '7', '8', '5', '2', '0', '3', '1', '9'
            ]
charst_crypt = lcase_crypt + ucase_crypt + num_crypt

########################### GLOBAL ####################################
global otp_lp
global mysql_password
global mode

#######################################################################
try:
    f = open("mode.txt", "r")
    mode = f.read()
    f.close()
except:
    f = open("mode.txt", "w")
    f.write("dark")
    f.close()
    mode = "dark"


try:
    with open('cache.txt') as file:
        file.close()
except:
    with open('cache.txt', 'w') as file:
        file.close()


try:
    p1 = open("sqlp.txt", "r")
    p1.close()

except:
    p = open("sqlp.txt", "w+")
    p.close()


#########################   FUNCTIONS   ##############################
def shuffle(strg):
    # takes input as string and shuffles
    ls = list(strg)
    random.shuffle(ls)


def password(n: int):
    # takes in a the number of digits and returns the password of 
    # length digits
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
        api_key = "live_fe8e78cfed4ff5262291"
        email = strg
        response = requests.get(
            "https://api.emailable.com/v1/verify",
            params={"email": email, "api_key": api_key},
        )
        status = response.json()['state']
        if status == "deliverable":
            return True
        elif (status == "undeliverable") or (status == "risky") or (status == "unknown"):
            return False
        else:
            messagebox.showerror("Sorry for the inconvenience", 
                                 "Please try tomorrow🙏🏼")
    except Exception:
        messagebox.showerror(
            "Network", "Please ensure that you are connected to the \
            internet."
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


def insintousers(firstName, lastName, userName, masterPass, eMail):
    # this functions inserts data into the myp_user table
    mycur.execute("USE myp;")
    global passu
    passu = hashcrypt(masterPass)
    action = (
        f"""INSERT INTO myp_users (firstName, lastName, userName, eMail,
        masterPass)
        VALUES ("""
        + "TRIM('"
        + firstName
        + "'), "
        + "TRIM('"
        + lastName
        + "'), '"
        + str(userName)
        + "', '"
        + str(eMail)
        + "', '"
        + passu
        + "');"
    )
    mycur.execute(action)
    mydb.commit()


def insintousers_eno(firstName, lastName, userName, masterPass):
    # this functions inserts data into the myp_user table
    mycur.execute("USE myp;")
    global passu
    passu = hashcrypt(masterPass)
    action = (
        f"""INSERT INTO myp_users (firstName, lastName, userName,
          masterPass)
        VALUES ("""
        + "TRIM('"
        + firstName
        + "'), "
        + "TRIM('"
        + lastName
        + "'), '"
        + userName
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
    mycur.execute("SELECT LAST_INSERT_ID();")
    p = mycur.fetchone()[0]
    mydb.commit()
    return p


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

            Please ignore if otp not requested🙏🏼.
            </p>
        </body>
    </html>"""

    part = MIMEText(html, "html")
    msg.attach(part)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login("manageyourpass91@gmail.com", "mokktrqhxujqrrtd")
        server.send_message(msg)
        server.quit()
    print(otp)
    ts = time.strftime('%M')
    return otp, ts


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
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login("manageyourpass91@gmail.com", "mokktrqhxujqrrtd")
        server.send_message(msg)
        server.quit()


def place_center(
    root, resol="500x500", x1=500, y1=500
):  # Placing the window in the center of the screen
    global x, y
    reso = pg.size()
    rx = reso[0]
    ry = reso[1]
    x = int((rx / 2) - (x1 / 2))
    y = int((ry / 2) - (y1 / 2))
    root.geometry(resol + f"+{x}+{y}")


def change_mode():
    global usr_img
    if sv.get_theme() == "dark":
        sv.set_theme("light")
        with open('mode.txt', 'w') as file:
            file.write("light")
        usr_img = ImageTk.PhotoImage(file="images\\3.png")
        user_btn.config(image = usr_img)

    elif sv.get_theme() == "light":
        sv.set_theme("dark")
        with open('mode.txt', 'w') as file:
            file.write("dark")
        usr_img = ImageTk.PhotoImage(file="images\\4.png")
        user_btn.config(image = usr_img)

    else:
        pass


def passdget(uid):
    mycur.execute(f"SELECT masterPass FROM myp_users WHERE userId = " + str(uid))
    pass_ls = []
    for i in mycur:
        pass_ls.extend(i)
    return pass_ls


def login_check():
    if (open('cache.txt').read()) == "":
        search_btn.config(state = DISABLED)
        search_bar.config(state = DISABLED) 
        srch_cancel_btn.config(state = DISABLED)
        genpass_btn.config(state = DISABLED)
        add_btn.config(state = DISABLED) 
        del_btn.config(state = DISABLED) 
        edit_btn.config(state = DISABLED) 
        chanmps_btn.config(state = DISABLED)
        import_btn.config(state = DISABLED)
        export_btn.config(state = DISABLED)
        del_usr_btn.config(state = DISABLED)
        showp_btn.config(state = DISABLED)
        hide_btn.config(state = DISABLED)
        site_ent.config(state = DISABLED)
        uname_ent.config(state = DISABLED)
        pass_ent.config(state = DISABLED)
        mpass_ent.config(state = DISABLED)
    else:
        try:
            search_btn.config(state = NORMAL)
            search_bar.config(state = NORMAL) 
            srch_cancel_btn.config(state = NORMAL)
            genpass_btn.config(state = NORMAL)
            add_btn.config(state = NORMAL) 
            del_btn.config(state = NORMAL) 
            edit_btn.config(state = NORMAL) 
            chanmps_btn.config(state = NORMAL)
            import_btn.config(state = NORMAL)
            export_btn.config(state = NORMAL)
            del_usr_btn.config(state = NORMAL)
            showp_btn.config(state = NORMAL) 
            hide_btn.config(state = NORMAL)
            site_ent.config(state = NORMAL)
            uname_ent.config(state = NORMAL)
            pass_ent.config(state = NORMAL)
            mpass_ent.config(state = NORMAL)
            
        except: 
            pass


def internet_stat(url="https://www.google.com/", timeout=3):
    try:
        r = requests.head(url=url, timeout=timeout)
        return True
    except requests.ConnectionError as e:
        return False


class loading_screen:
    def __init__(self, root, time):
        global top
        top = Toplevel()
        top.wm_attributes("-topmost", True)
        top.overrideredirect(1)
        x = root.winfo_x()
        y = root.winfo_y()
        top.geometry("+%d+%d" % (x + 120, y + 200))
        top.lift()
        top.after(time, lambda: top.destroy())
        frameCnt = 20
        frames = [
            PhotoImage(file="images/2.gif", format="gif -index %i" % (i))
            for i in range(frameCnt)
        ]

        def update(ind):

            frame = frames[ind]
            ind += 1
            if ind == frameCnt:
                ind = 0
            label.configure(image=frame)
            top.after(100, update, ind)

        label = ttk.Label(top)
        label.pack()
        top.after(0, update, 0)





#######################################################################


global root
global pass_btn
root = Tk()
sv.set_theme(mode)
root.title(" Password Manager")
root.iconbitmap("1.ico")
root.state("zoomed")

global count
count = 0

def refresh_tree():
    try:
        for items in my_tree.get_children():
            my_tree.delete(items)
    except:
        pass

    if (open('cache.txt').read()) == "":
        pass
    else:
        try:
            mycur.execute("SELECT passId FROM myp_data WHERE userId=" + (open('cache.txt').read()))
            uiddata = mycur.fetchall()
            uidls = []
            for i in uiddata:
                uidls.extend(i)

            uls = []
            for uidn in uidls:
                mycur.execute(
                "SELECT website, loginName, loginPass, passId FROM myp_data WHERE passId="
                + str(uidn)
                )
                for data in mycur.fetchall():
                    uls.append(data)

            global count    
            for i in range(len(uls)):   
                p = decrypt(str(uls[i][2]))
                my_tree.insert( 
                    parent="",  
                    iid=count,  
                    index="end",    
                    text=count+1,   
                    values=(
                        uls[i][3],
                        uls[i][0],
                        uls[i][1],
                        "•" * len(p),
                    ),
                )
                count += 1
        except:
            pass

pvar = IntVar(value=0)

my_frm_d = Frame(root)
my_frm = Frame(root, width=250)
my_tree = ttk.Treeview(my_frm)
scr_bar = ttk.Scrollbar(my_frm, orient=VERTICAL, command=my_tree.yview)

my_tree.configure(yscroll=scr_bar.set)

my_tree["columns"] = ("id", "site", "uname", "passwd")
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("id", anchor=CENTER, width=80)
my_tree.column("site", anchor=CENTER, width=120)
my_tree.column("uname", anchor=CENTER, width=120)
my_tree.column("passwd", anchor=CENTER, width=120)

my_tree.heading("#0", anchor=CENTER, text="")
my_tree.heading("id", anchor=CENTER, text="Id")
my_tree.heading("site", anchor=CENTER, text="Website")
my_tree.heading("uname", anchor=CENTER, text="Username")
my_tree.heading("passwd", anchor=CENTER, text="Password")

def shbtn_og():
    if (pvar.get()) == 1:
        pass_ent.configure(show="")
        mpass_ent.configure(show="")
    elif (pvar.get()) == 0:
        pass_ent.configure(show="•")
        mpass_ent.configure(show="•")


def delete_selected():
    if mpass_ent.get() == "":
        messagebox.showinfo(
            "Missing Password", "Please enter master password to delete data."
        )
    elif hashcrypt(mpass_ent.get()) == str(passdget(open('cache.txt').read())[0]):
        selected = my_tree.selection()
        for record in selected:
            values = my_tree.item(record, "values")
            mycur.execute(f"DELETE FROM MYP_DATA WHERE passID={values[0]}")
            mydb.commit()
            my_tree.delete(record)
            mpass_ent.delete(0, END)
    else:
        messagebox.showerror(
            "Wrong password", "Please enter correct Master Password"
        )


def add_data():
    if mpass_ent.get() == site_ent.get() == pass_ent.get() == "":
        messagebox.showinfo(
            "Data Not Found", "Enter the values in the entry boxes."
        )
    else:
        uid = open('cache.txt').read()
        pass_ls = passdget(uid)

        if hashcrypt(mpass_ent.get()) == str(pass_ls[0]):
            if ".com" in str(site_ent.get()):
                if str(site_ent.get()).startswith("https://") == True:
                    web = str(site_ent).get()
                else:
                    web = "https://" + str(site_ent.get())
            else:
                web = str(site_ent.get())
            
            pid = insintodata(web, uname_ent.get(), encrypt(pass_ent.get()), uid)

            site_ent.delete(0, END)
            uname_ent.delete(0, END)
            pass_ent.delete(0, END)
            mpass_ent.delete(0, END)
            refresh_tree()  

        else:
            messagebox.showerror(
                "Wrong password", "Please enter correct Master Password"
            )


def edit_selected():
    add_btn.config(state=DISABLED)
    del_btn.config(state=DISABLED)
    if mpass_ent.get() == "":
        messagebox.showinfo(
            "Missing Password", "Please enter master password to delete data."
        )
        add_btn.config(state=ACTIVE)
        del_btn.config(state=ACTIVE)

    elif str(passdget(open('cache.txt').read())[0]) == hashcrypt(mpass_ent.get()):
        mpass_ent.delete(0, END)
        selected = my_tree.selection()[0]
        values = my_tree.item(selected, "values")
        mycur.execute(
            f"SELECT loginPass from myp_data where passId = {values[0]}"
        )
        for i in mycur:
            passwd1 = decrypt(i[0])

        t0, t1, t2, t3 = values[0], values[1], values[2], passwd1
        site_ent.insert(0, values[1])
        uname_ent.insert(0, values[2])
        pass_ent.insert(0, passwd1)

        def revert():
            site_ent.delete(0, END)
            uname_ent.delete(0, END)
            pass_ent.delete(0, END)
            site_ent.insert(0, t1)
            uname_ent.insert(0, t2)
            pass_ent.insert(0, t3)

        def saven():
            if mpass_ent.get() == "":
                messagebox.showinfo(
                    "Missing Password",
                    "Please enter master password to delete data.",
                )
            elif hashcrypt(mpass_ent.get()) == str(passdget(open('cache.txt').read())[0]):
                selected = my_tree.selection()
                v1, v2, v3 = (
                    site_ent.get(),
                    uname_ent.get(),
                    encrypt(pass_ent.get()),
                )
                my_tree.item(selected, values=(t0, v1, v2, "•" * len(v3)))
                mycur.execute(
                    "UPDATE myp_data SET website = '"
                    + v1
                    + "', loginName = '"
                    + v2
                    + "', loginPass = '"
                    + v3
                    + "' WHERE passId = "
                    + str(t0)
                )

                mydb.commit()
                save_btn.destroy()
                revt_btn.destroy()
                cancel_btn.destroy()
                add_btn.config(state=ACTIVE)
                del_btn.config(state=ACTIVE)
                site_ent.delete(0, END)
                uname_ent.delete(0, END)
                pass_ent.delete(0, END)
                mpass_ent.delete(0, END)

            else:
                messagebox.showerror(
                    "Wrong password", "Please enter correct Master Password"
                )

        def canceler():
            save_btn.destroy()
            revt_btn.destroy()
            cancel_btn.destroy()
            add_btn.config(state=ACTIVE)
            del_btn.config(state=ACTIVE)
            site_ent.delete(0, END)
            uname_ent.delete(0, END)
            pass_ent.delete(0, END)
            mpass_ent.delete(0, END)

        save_btn = ttk.Button(root, text="Save", command=saven)
        revt_btn = ttk.Button(root, text="Revert", command=revert)
        cancel_btn = ttk.Button(root, text="Cancel", command=canceler)

        save_btn.grid(row=8, column=8, padx=80, pady=10)
        revt_btn.grid(row=9, column=8, padx=80, pady=10)
        cancel_btn.grid(row=10, column=8, padx=80, pady=10)

    else:
        messagebox.showerror(
            "Wrong password", "Please enter correct Master Password"
        )
        add_btn.config(state=ACTIVE)
        del_btn.config(state=ACTIVE)


def generpass():
    pass_ent.delete(0, END)
    gvar = password(12)
    pass_ent.insert(0, gvar)


def mstrchange():
    cbvar = IntVar(value=0)

    def shbtn():
        if (cbvar.get()) == 1:
            omp_ent.config(show="")
            nmp_ent.config(show="")
        else:
            omp_ent.config(show="•")
            nmp_ent.config(show="•")

    def mc_check(*e):
        omp = omp_ent.get()
        nmp = nmp_ent.get()
        if hashcrypt(str(omp)) == str(pass_ls[0]):
            nps = hashcrypt(str(nmp))
            mycur.execute(
                "UPDATE myp_users SET masterPass = '"
                + nps
                + "' WHERE userId = "
                + str(open('cache.txt').read())
            )
            mydb.commit()
            mstc.destroy()
            messagebox.showinfo("SUCCESS", f"Your master password has been changed from \
                                {len(omp)*'•'} to {len(nmp)*'•'} successfully")
        else:
            messagebox.showerror("Wrong OLD Password", "Enter the correct password")

    pass_ls = passdget(open('cache.txt').read())

    mstc = Toplevel()
    mstc.wm_attributes("-topmost", True)
    mstc.title("Confirmation")
    place_center(mstc, "420x200", -400, 200)
    mstc.resizable(0, 0)
    mstc.iconbitmap("images\\1.ico")

    omp_lbl = ttk.Label(
        mstc,
        text="Old Master Password :",
        font=("", 14, BOLD),
    )

    omp_lbl.grid(row=1, column=1, padx=10, pady=10)
    omp_ent = ttk.Entry(mstc, show="•")
    omp_ent.grid(row=1, column=2, padx=10, pady=10)

    nmp_lbl = ttk.Label(
        mstc,
        text="New Master Password :",
        font=("", 14, BOLD),
    )
    nmp_lbl.grid(row=2, column=1, padx=10, pady=10)

    nmp_ent = ttk.Entry(mstc, show="•")
    nmp_ent.grid(row=2, column=2, padx=10, pady=10)
    nmp_ent.bind("<Return>", mc_check)


    showpass_cb = ttk.Checkbutton(
        mstc,
        text="Show Password",
        variable=cbvar,
        onvalue=1,
        offvalue=0,
        command=shbtn,
        style="R.TCheckbutton",
    )
    showpass_cb.grid(row=3, column=2)

    change_btn = ttk.Button(
        mstc,
        text="Change",
        command=mc_check,
    )
    change_btn.grid(row=4, column=1, columnspan=2, padx=10, pady=10)
    mstc.mainloop()


def imp_data():
    uid = open('cache.txt').read()
    pass_ls = passdget(uid)
    if mpass_ent.get() == "":
        messagebox.showinfo(
            "Missing Password", "Please enter master password to delete data."
        )
    elif hashcrypt(mpass_ent.get()) == str(pass_ls[0]):
        mpass_ent.delete(0,END)
        try:
            root.filename = filedialog.askopenfile(
                title="Select a file",
                filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")),
            )
            m = str(root.filename).split()
            m.remove("<_io.TextIOWrapper")
            m.remove("encoding='cp1252'>")
            m.remove("mode='r'")
            n = " ".join(m)
            final_path = n.split("=")[1]
            final_path = final_path.replace("'", "")
            final_path = final_path.strip()

            file = open(final_path, "r")
            csv_r = csv.reader(file)
            ls = []
            for i in csv_r:
                ls.append(i)

            ls.reverse()
            ls.pop()
            ls.reverse()
            if len(ls) > 20:
                messagebox.showinfo("Please be patient", "This might take sometime")
            try:
                for i in range(len(ls)):
                    global count
                    web = ls[i][1]
                    logn = ls[i][2]
                    logp = encrypt(str(ls[i][3]))
                    pid = insintodata(web, logn, logp, uid)
                    mydb.commit()
                    my_tree.insert(
                        parent="",
                        index="end",
                        iid=count,
                        text="",
                        value=(pid, web, logn, "•" * len(logp)),
                    )
                    count += 1  
                messagebox.showinfo("Success", "Successfuly imported!!")
            except:
                messagebox.showinfo("Failure", "Failed to to import!!")
        except:
            pass
    else:
        messagebox.showerror("Wrong Password", "Enter the correct password")


def exp_data():
    if mpass_ent.get() == "":
        messagebox.showinfo(
            "Missing Password", "Please enter master password to delete data."
        )
    else:
        uid = open('cache.txt').read()
        pass_ls = passdget(uid)
        if hashcrypt(str(mpass_ent.get())) == str(pass_ls[0]):
            mycur.execute(
                "SELECT SUBSTR(website, 9)'name', website, loginName FROM myp_data WHERE userId = "
                + str(uid)
            )
            ls = mycur.fetchall()

            if ls == []:
                messagebox.showinfo("Nothing to Export", "No data found")
            else:
                root.filedir = filedialog.askdirectory(title="Select a folder")
                for i in range(len(ls)):
                    globals()[f"expd{i+1}"] = list(ls[i])
                mycur.execute(
                    "SELECT loginPass FROM myp_data WHERE userId = " + str(uid)
                )
                pls = mycur.fetchall()
                pls_ = []
                for i in pls:
                    pls_.extend(i)
                for i in range(len(pls_)):
                    globals()[f"expd{i+1}"].insert(3, decrypt(str(pls_[i])))
                try:
                    file = open(root.filedir + "/export.csv", "w", newline="")
                    csv_w = csv.writer(file)
                    ls = ("name", "url", "username", "password")
                    csv_w.writerow(ls)
                    file.close()
                    file = open(root.filedir + "/export.csv", "a+", newline="")
                    csv_w = csv.writer(file)
                    for i in range(len(pls_)):
                        csv_w.writerow(globals()[f"expd{i+1}"])
                    file.close()
                except PermissionError:
                    pass
                mpass_ent.delete(0, END)
        else:
            messagebox.showerror("Wrong Password", "Enter the correct password")
            mpass_ent.delete(0, END)


def deluser():
    if mpass_ent.get() == "":
        messagebox.showinfo(
            "Missing Password", "Please enter master password to delete data."
        )
    else:
        uid = open('cache.txt').read()
        pass_ls = passdget(uid)
        if hashcrypt(mpass_ent.get()) == str(pass_ls[0]):
            mycur.execute("SELECT email FROM myp_users WHERE userId = " + str(uid))
            els = mycur.fetchall()
            if internet_stat() == True:
                for i in els:
                    if i == (None,):
                        continue
                    else:
                        byemail(i[0])
            else:
                pass
            mycur.execute(
                "SELECT passId FROM myp_data WHERE userId = " + str(uid)
            )
            dells = []
            for i in mycur.fetchall():
                dells.extend(i)
            if dells != []:
                for pid in dells:
                    mycur.execute(
                        " DELETE FROM myp_data WHERE passId = " + str(pid)
                    )
                mydb.commit()
            else:
                pass
            mycur.execute("DELETE FROM myp_users WHERE userId = " + str(uid))
            mydb.commit()
            with open("cache.txt", "w") as file:
                file.close()
            site_ent.delete(0, END)
            uname_ent.delete(0, END)
            pass_ent.delete(0, END)
            mpass_ent.delete(0, END)
            signout()
        else:
            messagebox.showerror("Wrong Password", "Enter the correct password")
            mpass_ent.delete(0, END)


def signout():
    site_ent.delete(0, END)
    uname_ent.delete(0, END)
    pass_ent.delete(0, END)
    mpass_ent.delete(0, END)
    with open("cache.txt", "w") as file:
        file.close()
    refresh_tree()
    login_check()
    try:
        usr1.destroy()
    except:
        print("error")
    messagebox.showinfo("SUCCESS", "Sign Out Successful!!")


def showp():
    pass_ls = passdget(open('cache.txt').read())
    add_btn.config(state=DISABLED)
    del_btn.config(state=DISABLED)
    edit_btn.config(state=DISABLED)
    if hashcrypt(mpass_ent.get()) == str(pass_ls[0]):
        mpass_ent.delete(0, END)
        selected = my_tree.selection()
        for record in selected:
            vals = my_tree.item(record, "values")
            mycur.execute(
                f"SELECT loginPass FROM myp_data WHERE passId = {vals[0]}"
            )
            passl = decrypt(mycur.fetchone()[0])
            my_tree.item(record, values=(vals[0], vals[1], vals[2], passl))

        add_btn.config(state=ACTIVE)
        del_btn.config(state=ACTIVE)

    elif mpass_ent.get() == "":
        messagebox.showinfo("Password Missing", "Enter Master Password")
        add_btn.config(state=ACTIVE)
        del_btn.config(state=ACTIVE)

    else:
        messagebox.showerror(
            "Wrong password", "Please enter correct Master Password"
        )


def hidep():
    pass_ls = passdget(open('cache.txt').read())
    add_btn.config(state=DISABLED)
    del_btn.config(state=DISABLED)
    edit_btn.config(state=DISABLED)
    mpass_ent.delete(0, END)
    selected = my_tree.selection()

    for record in selected:
        vals = my_tree.item(record, "values")
        passl = len(vals[3])
        my_tree.item(record, values=(vals[0], vals[1], vals[2], "•" * passl))
    
    add_btn.config(state=ACTIVE)
    del_btn.config(state=ACTIVE)


def search(*e):
    req = search_bar.get()
    srch_ls = []
    sls = []
    mycur.execute(f"select passId, website, loginName, loginPass from myp_data where userId = {open('cache.txt').read()};")
    for i in mycur:
        srch_ls.append(i)
    for item in my_tree.get_children():
        my_tree.delete(item)
    for j in srch_ls:
        if (req in j[1]) or (req in j[2]):
            sls.append(j)
    if sls == []:
        search_bar.delete(0, END)
        messagebox.showinfo("Info", "No data found.")
        refresh_tree()
    else:
        for k in sls:
            global count
            my_tree.insert(
                parent="",
                index="end",
                iid=count,
                text="",
                value=(
                    k[0],
                    k[1],
                    k[2],
                    "•" * len(k[3]),
                ),
            )
            count += 1


def cancel_srch():
    search_bar.delete(0, END)
    for item in my_tree.get_children():
        my_tree.delete(item)
    refresh_tree()


def user():
    if (open('cache.txt').read() == ""):
        global usr
        usr = Toplevel()
        usr.wm_attributes("-topmost", True)
        usr.title(" Password Manager ")
        usr.iconbitmap("images\\1.ico")
        place_center(usr, "500x150", 500, 500)
        login_btn = ttk.Button(usr, text="Login", width=8, command=login_page)
        signup_btn = ttk.Button(usr, text="Sign Up", width=8, command=signup_page)

        login_btn.place(relx=0.3, rely=0.5, anchor=CENTER)
        signup_btn.place(relx=0.7, rely=0.5, anchor=CENTER)
        usr.mainloop()
    else:
        global usr1
        usr1 = Toplevel()
        usr1.wm_attributes("-topmost", True)
        usr1.title("User Details")
        place_center(usr1, "500x150", 500,500)
        usr1.resizable(0, 0)
        usr1.iconbitmap("images\\1.ico")
        mycur.execute(f"SELECT concat(firstName, ' ', lastName), eMail from myp_users where userId = {open('cache.txt').read()};")
        for i in mycur:
            usr_name = i[0]
            usr_email = i[1]

        if usr_email == None:
            usr_email = "-"
        else:
            pass

        usrn_lbl = ttk.Label(usr1, text=f'Username: {usr_name}', font = ("", 14, BOLD), anchor=CENTER)
        usre_lbl = ttk.Label(usr1, text=f'Email: {usr_email}', font = ("", 14, BOLD), anchor=CENTER)
        signout_btn = ttk.Button(usr1, text="Sign Out", command=signout)
        usrn_lbl.place(relx=0.5, rely=0.5, anchor=CENTER)
        usre_lbl.place(relx=0.5, rely=0.65, anchor=CENTER)
        signout_btn.place(relx=0.975, rely=0.025, anchor=NE)
        usr1.mainloop()


def bar(*e):
    global size, value
    value = 0
    size = 15
    search_btn.destroy()
    search_bar.grid(row=0, column=0, pady=10, columnspan=6, padx=25)
    srch_cancel_btn.place(relx=0.63, rely=0.015)


def expand(*e):
    global size, value
    while value < 45:
        size += 2
        value += 1
        search_btn.config(width=size)
    root.after(100, bar)


def login_page():
    usr.destroy()
    mycur.execute("SELECT userName FROM myp_users")
    data_ls = mycur.fetchall()
    ls = ["Select a Username"]

    for i in data_ls:
        ls.extend(i)

    if ls == ["Select a Username"]:
        messagebox.showinfo("Sign Up Please", "Create your account.")
    else:
        global lpg
        global user
        lpg = Toplevel()
        lpg.title("Login")
        lpg.wm_attributes('-topmost', True)
        place_center(lpg, "450x300", -400, 300)
        lpg.resizable(0, 0)
        lpg.iconbitmap("images\\1.ico")
        passkey = StringVar()
        cbvar = IntVar(value=0)



        def login(*event):
            global lpg
            mycur.execute("USE myp;")

            uname_srch = usern_dm.get()
            if uname_srch == "Select a Username":
                messagebox.showerror(
                    "User Not Selected", "Select an user from the dropdown menu."
                )
            else:
                mycur.execute(
                    f"SELECT userId FROM myp_users WHERE userName = '{uname_srch}';"
                )
                user_ls = []
                for i in mycur:
                    user_ls.extend(i)

                global user
                user = user_ls[0]

                mycur.execute(
                    f"SELECT masterPass FROM myp_users WHERE userName = '{uname_srch}';"
                )
                pass_ls = []
                for i in mycur:
                    pass_ls.extend(i)

                ch = False
                while ch == False:
                    masterPass_check_hash = hashcrypt(passkey.get())
                    if masterPass_check_hash == pass_ls[0]:
                        with open("cache.txt", "w") as fileerite:
                            fileerite.write(str(user))
                        refresh_tree()
                        login_check()
                        lpg.destroy()
                        messagebox.showinfo("SUCCESS", "Login Successful!!")
                        break
                    else:
                        msgbox = messagebox.showwarning("ERROR", "WRONG PASSWORD!!")
                        if msgbox == "ok":
                            break
                pass_ls = []

        def shbtn():
            if (cbvar.get()) == 1:
                pass_ent.config(show="")
            else:
                pass_ent.config(show="•")

        ###WIDGETS
        usern_lbl = ttk.Label(
            lpg,
            text="Username:",
            font=("", 14, BOLD),
        )
        pass_lbl = ttk.Label(
            lpg,
            text="Password:",
            font=("", 14, BOLD),
        )
        pass_ent = ttk.Entry(lpg, textvariable=passkey, show="•", width=30)
        pass_ent.bind("<Return>", login)
        in_btn = ttk.Button(lpg, text="Sign In", command=login, width=20)

        showpass_cb = ttk.Checkbutton(
            lpg,
            text="Show Password",
            variable=cbvar,
            onvalue=1,
            offvalue=0,
            command=shbtn,
            style="R.TCheckbutton",
        )

        # SHOWING THEM
        usern_lbl.place(relx=0.2, rely=0.3, anchor=CENTER)
        pass_lbl.place(relx=0.2, rely=0.45, anchor=CENTER)
        pass_ent.place(relx=0.7, rely=0.45, anchor=CENTER)
        showpass_cb.place(relx=0.85, rely=0.6, anchor=CENTER)
        in_btn.place(relx=0.5, rely=0.7, anchor=CENTER)

        if ls == []:
            response = messagebox.showinfo("Info", "No users found!!")
            Label(lpg, text=response).pack()
        else:
            usern_dm = ttk.Combobox(lpg, value=ls, font=("", 14))
            usern_dm.current(0)
            usern_dm.place(relx=0.68, rely=0.3, anchor=CENTER)

        lpg.mainloop()
    


def signup_page():
    usr.destroy()
    global spg

    spg = Toplevel()
    spg.title("Sign Up")
    place_center(spg, "450x600", -400, 650)
    spg.resizable(0, 0)
    spg.wm_attributes("-topmost", True)
    spg.iconbitmap("images\\1.ico")


    passkey = StringVar()
    repasskey = StringVar()
    cbvar = IntVar(value=0)

    def signup(*event):
        def upass_ui():
            intst = internet_stat()
            if intst == True:
                insintousers(
                    firstName=str(f_name_ent.get()),
                    lastName=str(l_name_ent.get()),
                    userName=str(u_name_ent.get()),
                    eMail=str(email_ent.get()),
                    masterPass=str(upass_ent.get()),
                )
            else:
                insintousers_eno(
                    firstName=str(f_name_ent.get()),
                    lastName=str(l_name_ent.get()),
                    userName=str(u_name_ent.get()),
                    masterPass=str(upass_ent.get()),
                )
            messagebox.showinfo(
                "Successfully Signed Up", "You have successfull created your account\nLogin to continue using the app."
            )
            
            spg.destroy()
            login_check()
            refresh_tree()

        if urepass_ent.get() != upass_ent.get():
            messagebox.showerror(
                "Password Mismatch", "Please make sure that your passwords match."
            )
        elif len(upass_ent.get()) < 8:
            messagebox.showerror(
                "Password Not Satisfying Requirements",
                "The password should be atleast a minimum of 8 characters.",
            )
        else:
            upass_ui()

    def unamec(*event):
        def cbshow():
            if (cbvar.get()) == 1:
                upass_ent.config(show="")
                urepass_ent.config(show="")
            else:
                upass_ent.config(show="•")
                urepass_ent.config(show="•")

        if internet_stat() == True:

            def emailc(*event):
                def otpc(*event):
                    nts = time.strftime('%M')
                    if (int(nts)-int(ts)) > 5:
                        messagebox.showinfo("OTP EXPIRED", "Click on resend OTP.")
                    else:
                        global otp
                        global urepass_ent
                        global upass_ent

                        js = eval(otp_ent.get())
                        if js == otp:
                            resend.destroy()
                            global upass_lbl
                            upass_lbl = ttk.Label(
                                spg,
                                text="Master Password:",
                                font=("", 14, BOLD),
                            )
                            global upass_ent
                            upass_ent = ttk.Entry(
                                spg, textvariable=passkey, show="•", width=20
                            )
                            global urepass_lbl
                            urepass_lbl = ttk.Label(
                                spg,
                                text="Re-Enter Password:",
                                font=("", 14, BOLD),
                            )
                            global urepass_ent
                            urepass_ent = ttk.Entry(
                                spg, textvariable=repasskey, show="•", width=20
                            )
                            urepass_ent.bind("<Return>", signup)
                            global showpass_cb
                            showpass_cb = ttk.Checkbutton(
                                spg,
                                text="Show Password",
                                variable=cbvar,
                                onvalue=1,
                                offvalue=0,
                                command=cbshow,
                            )
                            global up_btn
                            up_btn = ttk.Button(
                                spg, text="Sign Up", command=signup, width=16
                            )

                            upass_lbl.grid(row=8, column=1, padx=10, pady=10)
                            upass_ent.grid(row=8, column=2, padx=10, pady=10)
                            urepass_lbl.grid(row=9, column=1, padx=10, pady=10)
                            urepass_ent.grid(row=9, column=2, padx=10, pady=10)
                            showpass_cb.grid(row=10, column=2, padx=10, sticky=E)
                            up_btn.grid(
                                row=11, column=1, columnspan=2, padx=20, pady=10, ipadx=100
                            )
                        else:
                            messagebox.showerror(
                                "Wrong OTP",
                                "The entered otp is wrong.\nPlease check again.",
                            )

                res = emailvalidation(email_ent.get())

                if res == False:
                    messagebox.showerror(
                        "Invalid E-Mail", "This is not an valid e-mail address."
                    )
                else:
                    ress = emailcheck(email_ent.get())
                    if ress == False:
                        messagebox.showinfo(
                            "Duplicate Found",
                            "This is email address is assosiated with another user.",
                        )
                    else:
                        loading_screen(spg, 4000)

                        def rentered(*e):
                            resend.config(fg = "light blue")
                        
                        def rexit(*e):
                            resend.config(fg= "white")
                        
                        def resendp(*e):
                            global otp, ts
                            otp, ts = otpmail(email_ent.get())

                        global otp, ts
                        otp, ts = otpmail(email_ent.get())
                        global otp_lbl
                        otp_lbl = ttk.Label(
                            spg,
                            text="OTP:      ",
                            font=("", 14, BOLD),
                        )
                        global otp_ent
                        otp_ent = ttk.Entry(spg, width=20)
                        otp_ent.bind("<Return>", otpc)

                        resend = Label(spg, text="Resend OTP", font=("", 9, BOLD))

                        otp_lbl.grid(row=7, column=1, padx=10, pady=10)
                        otp_ent.grid(row=7, column=2, padx=10, pady=10)
                        resend.place(relx=0.5, rely=0.559)

                        resend.bind("<Enter>", rentered)
                        resend.bind("<Button-1>", resendp)
                        resend.bind("<Leave>", rexit)

            res = unamecheck(u_name_ent.get())

            if res == False:
                messagebox.showerror("Duplicate found", "This username already exits!")
            else:
                if f_name_ent.get() == "":
                    messagebox.showerror(
                        "Fill Everything", "Please enter a First name."
                    )
                elif u_name_ent.get() == "":
                    messagebox.showerror("Fill Everything", "Please enter a username.")
                else:

                    global email_lbl
                    email_lbl = ttk.Label(
                        spg,
                        text="E-Mail:   ",
                        font=("", 14, BOLD),
                    )
                    global email_ent
                    email_ent = ttk.Entry(spg, width=20)
                    email_ent.bind("<Return>", emailc)

                    email_lbl.grid(row=6, column=1, padx=10, pady=10)
                    email_ent.grid(row=6, column=2, padx=10, pady=10)
        else:
            res = unamecheck(u_name_ent.get())

            if res == False:
                messagebox.showerror("Duplicate found", "This username already exits!")
            else:
                if f_name_ent.get() == "":
                    messagebox.showerror(
                        "Fill Everything", "Please enter a First name."
                    )
                elif u_name_ent.get() == "":
                    messagebox.showerror("Fill Everything", "Please enter a username.")
                else:
                    global upass_lbl
                    upass_lbl = ttk.Label(
                        spg,
                        text="Master Password:",
                        font=("", 14, BOLD),
                    )
                    global upass_ent
                    upass_ent = ttk.Entry(spg, textvariable=passkey, show="•", width=20)
                    global urepass_lbl
                    urepass_lbl = ttk.Label(
                        spg,
                        text="Re-Enter Password:",
                        font=("", 14, BOLD),
                    )
                    global urepass_ent
                    urepass_ent = ttk.Entry(
                        spg, textvariable=repasskey, show="•", width=20
                    )
                    urepass_ent.bind("<Return>", signup)
                    global showpass_cb
                    showpass_cb = ttk.Checkbutton(
                        spg,
                        text="Show Password",
                        variable=cbvar,
                        onvalue=1,
                        offvalue=0,
                        command=cbshow,
                    )

                    global up_btn
                    up_btn = ttk.Button(spg, text="Sign Up", command=signup, width=16)

                    upass_lbl.grid(row=8, column=1, padx=10, pady=10)
                    upass_ent.grid(row=8, column=2, padx=10, pady=10)
                    urepass_lbl.grid(row=9, column=1, padx=10, pady=10)
                    urepass_ent.grid(row=9, column=2, padx=10, pady=10)
                    showpass_cb.grid(row=10, column=2, padx=10, sticky=E)
                    up_btn.grid(
                        row=11, column=1, columnspan=2, padx=10, pady=10, ipadx=100
                    )

    global f_name_ent
    f_name_lbl = ttk.Label(
        spg,
        text="First Name:",
        font=("", 14, BOLD),
    )
    f_name_ent = ttk.Entry(spg, width=20)
    global l_name_ent
    l_name_lbl = ttk.Label(
        spg,
        text="Last Name:",
        font=("", 14, BOLD),
    )
    l_name_ent = ttk.Entry(spg, width=20)
    global u_name_ent
    u_name_lbl = ttk.Label(
        spg,
        text="Create Username:",
        font=("", 14, BOLD),
    )
    u_name_ent = ttk.Entry(spg, width=20)
    u_name_ent.bind("<Return>", unamec)

    f_name_lbl.grid(row=3, column=1, padx=10, pady=10)
    l_name_lbl.grid(row=4, column=1, padx=10, pady=10)
    u_name_lbl.grid(row=5, column=1, padx=10, pady=10)

    f_name_ent.grid(row=3, column=2, padx=10, pady=10)
    l_name_ent.grid(row=4, column=2, padx=10, pady=10)
    u_name_ent.grid(row=5, column=2, padx=10, pady=10)

    spg.mainloop()


global infowin
global search_btn
global size, value

size = 15
value = 0
search_bar = ttk.Entry(root, width=100)
srch_cancel_btn = ttk.Button(root, text='X', command=cancel_srch)
search_btn = ttk.Button(root, text='Search', command=expand, width=size,)
search_bar.bind("<Return>", search)
genpass_btn = ttk.Button(root, text="Generate Password", command=generpass)
add_btn = ttk.Button(root, text="Add", command=lambda: [add_data()])
del_btn = ttk.Button(root, text="Delete Selected", command=delete_selected)
edit_btn = ttk.Button(
    root, text="Edit Selected", command=edit_selected, state=DISABLED
)
if mode == 'dark':
    usr_img = ImageTk.PhotoImage(file="images\\4.png")
elif mode == 'light':
    usr_img = ImageTk.PhotoImage(file="images\\3.png")
else:
    pass

mode_img = ImageTk.PhotoImage(file="images\\5.png")

user_btn = ttk.Button(root, image=usr_img, command=user)

chanmps_btn = ttk.Button(root, text="Change Master Password", command=mstrchange)
import_btn = ttk.Button(root, text="Import Data", command=imp_data)
export_btn = ttk.Button(root, text="Export data", command=exp_data)
del_usr_btn = ttk.Button(root, text="Delete User", command=deluser)
mode_btn = ttk.Button(root, image=mode_img, command=change_mode)
showp_btn = ttk.Button(
    root, text="Show Password for Selected", command=showp, state=DISABLED
)
hide_btn = ttk.Button(
    root, text="Hide Password for Selected", command=hidep, state=DISABLED
)
my_tree.bind(
    "<Button-1>",
    lambda i: [
        edit_btn.config(state=ACTIVE),
        showp_btn.config(state=ACTIVE),
        hide_btn.config(state=ACTIVE),
    ],
)

site_lbl = Label(root, text="Site: ", font=("", 14, BOLD))
site_ent = ttk.Entry(root, width=25)

uname_lbl = Label(root, text="Username: ", font=("", 14, BOLD))
uname_ent = ttk.Entry(root, width=25)

pass_lbl = Label(root, text="Password: ", font=("", 14, BOLD))
pass_ent = ttk.Entry(root, width=25, show="•")

mpass_lbl = Label(root, text="Master Password: ", font=("", 14, BOLD))
mpass_ent = ttk.Entry(root, width=25, show="•")
showpass_btn = ttk.Checkbutton(
    root,
    onvalue=1,
    offvalue=0,
    variable=pvar,
    text="Show password",
    command=shbtn_og,
)
search_btn.grid(row=0, column=0, pady=10, columnspan=6)
user_btn.grid(row=1, column=8, padx=80, pady=8)
my_tree.place(relx=0.001, rely=0.001, width=1170, height=250)
scr_bar.place(relx=0.982, rely=0.001, height=250)
my_frm_d.grid(row=1, column=1, pady=10, columnspan=6, rowspan=5, sticky=NSEW)
my_frm.place(relx=0.001, rely=0.075, width=1195, height=250)

genpass_btn.grid(row=3, column=8, padx=80, pady=10)
add_btn.grid(row=4, column=8, padx=80, pady=10)
edit_btn.grid(row=5, column=8, padx=80, pady=10)
del_btn.grid(row=6, column=8, padx=80, pady=10)

chanmps_btn.grid(row=11, column=1, pady=180, sticky=SE)
import_btn.grid(row=11, column=2, padx=10, pady=180, sticky=SE)
export_btn.grid(row=11, column=3, padx=10, pady=180, sticky=SE)
del_usr_btn.grid(row=11, column=4, padx=10, pady=180, sticky=SE)
mode_btn.grid(row=11, column=8, padx=80, pady=180, sticky=SE)

site_lbl.grid(row=7, column=1, padx=10)
site_ent.grid(row=8, column=1, padx=10)

uname_lbl.grid(row=7, column=2, padx=10)
uname_ent.grid(row=8, column=2, padx=10)

pass_lbl.grid(row=7, column=3, padx=10)
pass_ent.grid(row=8, column=3, padx=10)

mpass_lbl.grid(row=7, column=4, padx=10)
mpass_ent.grid(row=8, column=4, padx=10)

showpass_btn.grid(row=8, column=5, padx=10, pady=10)
showp_btn.grid(row=8, column=6, padx=10, pady=10)
hide_btn.grid(row=9, column=6, padx=10, pady=10)

login_check()

try:
    mydb = sqlc.connect(
        host="localhost", user="root", 
        passwd=str(open('sqlp.txt').read()))
    mycur = mydb.cursor()
    mycur.execute("USE myp;")
except Exception as e:
    def shbtn_pass(mps_cbvar, mps_ent):
        if (mps_cbvar.get()) == 1:
            mps_ent.configure(show="")
        elif (mps_cbvar.get()) == 0:
            mps_ent.configure(show="•")
    
    def mps_enter(*e):
        global mysql_password
        global mydb
        global mycur
        try:
            mysql_password = mps_ent.get()
            mydb = sqlc.connect(
                host="localhost",
                user="root",
                passwd=mysql_password,
            )
            mycur=mydb.cursor()
            v1 = open("sqlp.txt", "w")
            v1.write(mysql_password)
            v1.flush()
            v1.close()
            mycur.execute("USE MYP;")
            getpass_sql.destroy()

        except:
            messagebox.showerror("Authentication Error", "Wrong MYSQL Password!!")
            mps_ent.delete(0, END)

    getpass_sql = Toplevel()
    getpass_sql.wm_attributes("-topmost", True)
    getpass_sql.title("MySQL Password")
    getpass_sql.geometry("550x150")
    getpass_sql.resizable(0, 0)
    getpass_sql.iconbitmap("1.ico")


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
        command=lambda: shbtn_pass(mps_cbvar, mps_ent),
        style="R.TCheckbutton",
    )

    mps_ent.bind("<Return>", mps_enter)

    mps_lbl.grid(row=0, column=0, padx=10, pady=10)
    mps_ent.grid(row=0, column=1, padx=10, pady=10)
    mps_showpass_cb.grid(row=1, column=1, padx=10)
    mps_btn.grid(row=2, column=0, columnspan=2, pady=10, padx=10)

    getpass_sql.mainloop()
    
refresh_tree()

########################## CHECKING AND CREATING DATABASE #############
mycur.execute("SHOW SCHEMAS;")
db_ls = []

for i in mycur:
    db_ls.extend(i)
# ProjectbyVarunAdhityaGB
if "myp" in db_ls:
    mycur.execute("USE myp;")
elif "myp" in db_ls:
    mycur.execute("USE myp;")
else:
    mycur.execute("CREATE DATABASE myp;")
    mycur.execute("USE myp;")


########################## CHECKING AND CREATING TABLES ###############
mycur.execute("SHOW TABLES;")
tb_ls = []

for i in mycur:
    tb_ls.extend(i)
if tb_ls == []:
    mycur.execute("USE myp;")
    mycur.execute(
        """CREATE TABLE myp_users (
            userId INT  UNSIGNED PRIMARY KEY AUTO_INCREMENT,
            firstName VARCHAR(225) NOT NULL,
            lastName VARCHAR(225),
            userName VARCHAR(225) NOT NULL UNIQUE KEY,
            eMail VARCHAR(225) UNIQUE KEY,
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

root.mainloop()