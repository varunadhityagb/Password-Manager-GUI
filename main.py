import csv
from email import message
import sys
import tkinter.ttk as ttk
import tkinter.ttk as tkt
from time import *
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.font import BOLD

import pyautogui as pg

from database import *
from mypfuncs import *

########################## CHECKING AND CREATING DATABASE #############################
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

########################## CHECKING AND CREATING TABLES ###############################
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
else:
    pass
##############################################################################
open("cache.txt", "a")

mysql_password = open("sqlp.txt", "r").read()


def passdget(uid):
    mycur.execute(f"SELECT masterPass FROM myp_users WHERE userId = " + str(uid))
    pass_ls = []
    for i in mycur:
        pass_ls.extend(i)
    return pass_ls


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
            PhotoImage(file="images/3.gif", format="gif -index %i" % (i))
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


def internet_stat(url="https://www.google.com/", timeout=3):
    try:
        r = requests.head(url=url, timeout=timeout)
        return True
    except requests.ConnectionError as e:
        return False


net_stat = internet_stat()


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


def lbk_rootw():
    global lpg
    lpg.destroy()
    rootw()


def sbk_rootw():
    global spg
    spg.destroy()
    rootw()


def ipass_ui():
    lpg.destroy()
    system("python main.py")


def ui(uid):

    global psl
    global pass_btn
    psl = Tk()
    psl.title("Passwords")
    psl.state("zoomed")
    psl.tk.call("source", "sv.tcl")
    psl.tk.call("set_theme", mode)

    global count
    count = 0

    def refresh_tree():
        mycur.execute("SELECT passId FROM myp_data WHERE userId=" + uid)
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

    pvar = IntVar(value=0)

    mycur.execute("USE MYP;")
    my_frm_d = Frame(psl)
    my_frm = Frame(psl, width=250)
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

    refresh_tree()

    def shbtn():
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
        elif hashcrypt(mpass_ent.get()) == str(passdget(uid)[0]):
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

                global count
                my_tree.insert(
                    parent="",
                    index="end",
                    iid=count,
                    text="",
                    value=(
                        pid,
                        web,
                        uname_ent.get(),
                        "•" * len(encrypt(pass_ent.get())),
                    ),
                )
                count += 1

                site_ent.delete(0, END)
                uname_ent.delete(0, END)
                pass_ent.delete(0, END)
                mpass_ent.delete(0, END)
                psl.destroy()

            else:
                messagebox.showerror(
                    "Wrong password", "Please enter correct Master Password"
                )
            system("python main.py")
            psl.destroy()

    def edit_selected():
        add_btn.config(state=DISABLED)
        del_btn.config(state=DISABLED)
        if mpass_ent.get() == "":
            messagebox.showinfo(
                "Missing Password", "Please enter master password to delete data."
            )
            add_btn.config(state=ACTIVE)
            del_btn.config(state=ACTIVE)

        elif str(passdget(uid)[0]) == hashcrypt(mpass_ent.get()):
            try:
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
            except:
                messagebox.showinfo("Internal Error", "Relaunch required")
                psl.destroy()
                system("python main.py")

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
                elif hashcrypt(mpass_ent.get()) == str(passdget(uid)[0]):
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

            save_btn = ttk.Button(psl, text="Save", command=saven)
            revt_btn = ttk.Button(psl, text="Revert", command=revert)
            cancel_btn = ttk.Button(psl, text="Cancel", command=canceler)

            save_btn.grid(row=8, column=8, padx=10, pady=10)
            revt_btn.grid(row=9, column=8, padx=10, pady=10)
            cancel_btn.grid(row=10, column=8, padx=10, pady=10)

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
            if hashcrypt(str(omp_ent.get())) == str(pass_ls[0]):
                nps = hashcrypt(str(nmp_ent.get()))
                mycur.execute(
                    "UPDATE myp_users SET masterPass = '"
                    + nps
                    + "' WHERE userId = "
                    + str(uid)
                )
                mstc.destroy()
                mydb.commit()
            else:
                messagebox.showerror("Wrong OLD Password", "Enter the correct password")

        pass_ls = passdget(uid)

        mstc = Toplevel()
        mstc.wm_attributes("-topmost", True)
        mstc.title("Confirmation")
        place_center(mstc, "420x200", 400, 200)
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

        if mode == "light":
            mstc.config(bg="#9e9e9e")
        else:
            pass

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

    def imp_data():
        pass_ls = passdget(uid)
        if mpass_ent.get() == "":
            messagebox.showinfo(
                "Missing Password", "Please enter master password to delete data."
            )
        elif hashcrypt(mpass_ent.get()) == str(pass_ls[0]):
            mpass_ent.delete(0,END)
            try:
                psl.filename = filedialog.askopenfile(
                    title="Select a file",
                    filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")),
                )
                m = str(psl.filename).split()
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
                    psl.filedir = filedialog.askdirectory(title="Select a folder")
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
                    file = open(psl.filedir + "/export.csv", "w", newline="")
                    csv_w = csv.writer(file)
                    ls = ("name", "url", "username", "password")
                    csv_w.writerow(ls)
                    file.close()
                    file = open(psl.filedir + "/export.csv", "a+", newline="")
                    csv_w = csv.writer(file)
                    for i in range(len(pls_)):
                        csv_w.writerow(globals()[f"expd{i+1}"])
                    file.close()
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
            pass_ls = passdget(uid)
            if hashcrypt(mpass_ent.get()) == str(pass_ls[0]):
                mycur.execute("SELECT email FROM myp_users WHERE userId = " + str(uid))
                els = mycur.fetchall()
                if net_stat == True:
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
                psl.destroy()
                open("cache.txt", "w")
                system("python main.py")
            else:
                messagebox.showerror("Wrong Password", "Enter the correct password")
                mpass_ent.delete(0, END)

    def signout():
        psl.destroy()
        open("cache.txt", "w")
        system("python main.py")

    def me():
        global infowin
        infowin = Toplevel()
        infowin.geometry("500x500")
        infowin.overrideredirect(True)
        place_center(infowin)
        infowin.bind("<Leave>", lambda i: infowin.destroy())
        mepage = ImageTk.PhotoImage(file="images//5.png")
        ttk.Label(infowin, image=mepage, borderwidth=0).pack()
        infowin.mainloop()

    def showp():
        pass_ls = passdget(uid)
        add_btn.config(state=DISABLED)
        del_btn.config(state=DISABLED)
        edit_btn.config(state=DISABLED)
        if hashcrypt(mpass_ent.get()) == str(pass_ls[0]):
            mpass_ent.delete(0, END)
            selected = my_tree.selection()
            try:
                for record in selected:
                    vals = my_tree.item(record, "values")
                    mycur.execute(
                        f"SELECT loginPass FROM myp_data WHERE passId = {vals[0]}"
                    )
                    passl = decrypt(mycur.fetchone()[0])
                    my_tree.item(record, values=(vals[0], vals[1], vals[2], passl))
            except:
                messagebox.showinfo("Internal Error", "Relaunch required")
                psl.destroy()
                system("python main.py")
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
        pass_ls = passdget(uid)
        add_btn.config(state=DISABLED)
        del_btn.config(state=DISABLED)
        edit_btn.config(state=DISABLED)
        mpass_ent.delete(0, END)
        selected = my_tree.selection()
        try:
            for record in selected:
                vals = my_tree.item(record, "values")
                passl = len(vals[3])
                my_tree.item(record, values=(vals[0], vals[1], vals[2], "•" * passl))
        except:
            messagebox.showinfo("Internal Error", "Relaunch required")
            psl.destroy()
            system("python main.py")
        add_btn.config(state=ACTIVE)
        del_btn.config(state=ACTIVE)

    def search(*e):
        req = search_bar.get()
        srch_ls = []
        sls = []
        mycur.execute(f"select passId, website, loginName, loginPass from myp_data where userId = {uid};")
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
        usr = Toplevel()
        usr.wm_attributes("-topmost", True)
        usr.title("User Details")
        place_center(usr, "500x150", 500,500)
        usr.resizable(0, 0)
        usr.iconbitmap("images\\1.ico")
        mycur.execute(f"SELECT concat(firstName, ' ', lastName), eMail from myp_users where userId = {uid};")
        for i in mycur:
            usr_name = i[0]
            usr_email = i[1]

        if usr_email == None:
            usr_email = "-"
        else:
            pass

        usrn_lbl = ttk.Label(usr, text=f'Username: {usr_name}', font = ("", 14, BOLD), anchor=CENTER)
        usre_lbl = ttk.Label(usr, text=f'Email: {usr_email}', font = ("", 14, BOLD), anchor=CENTER)
        signout_btn = ttk.Button(usr, text="Sign Out", command=signout)
        usrn_lbl.place(relx=0.5, rely=0.5, anchor=CENTER)
        usre_lbl.place(relx=0.5, rely=0.65, anchor=CENTER)
        signout_btn.place(relx=0.975, rely=0.025, anchor=NE)
        usr.mainloop()


    global infowin
    global search_btn
    search_bar = ttk.Entry(psl, width=100)
    srch_cancel_btn = ttk.Button(psl, text='X', command=cancel_srch)
    search_btn = ttk.Button(psl, text='Search', command=search)
    search_bar.bind("<Return>", search)
    genpass_btn = ttk.Button(psl, text="Generate Password", command=generpass)
    add_btn = ttk.Button(psl, text="Add", command=lambda: [add_data()])
    del_btn = ttk.Button(psl, text="Delete Selected", command=delete_selected)
    edit_btn = ttk.Button(
        psl, text="Edit Selected", command=edit_selected, state=DISABLED
    )
    if mode == 'dark':
        usr_img = ImageTk.PhotoImage(file="images\\11.png")
    elif mode == 'light':
        usr_img = ImageTk.PhotoImage(file="images\\10.png")
    else:
        pass

    b = ttk.Button(psl, image=usr_img, command=user)

    chanmps_btn = ttk.Button(psl, text="Change Master Password", command=mstrchange)
    import_btn = ttk.Button(psl, text="Import Data", command=imp_data)
    export_btn = ttk.Button(psl, text="Export data", command=exp_data)
    del_usr_btn = ttk.Button(psl, text="Delete User", command=deluser)
    info_btn = ttk.Button(psl, text="About Me", state=DISABLED)
    showp_btn = ttk.Button(
        psl, text="Show Password for Selected", command=showp, state=DISABLED
    )
    hide_btn = ttk.Button(
        psl, text="Hide Password for Selected", command=hidep, state=DISABLED
    )
    my_tree.bind(
        "<Button-1>",
        lambda i: [
            edit_btn.config(state=ACTIVE),
            showp_btn.config(state=ACTIVE),
            hide_btn.config(state=ACTIVE),
        ],
    )

    site_lbl = Label(psl, text="Site: ", font=("", 14, BOLD))
    site_ent = ttk.Entry(psl, width=25)

    uname_lbl = Label(psl, text="Username: ", font=("", 14, BOLD))
    uname_ent = ttk.Entry(psl, width=25)

    pass_lbl = Label(psl, text="Password: ", font=("", 14, BOLD))
    pass_ent = ttk.Entry(psl, width=25, show="•")

    mpass_lbl = Label(psl, text="Master Password: ", font=("", 14, BOLD))
    mpass_ent = ttk.Entry(psl, width=25, show="•")
    showpass_btn = ttk.Checkbutton(
        psl,
        onvalue=1,
        offvalue=0,
        variable=pvar,
        text="Show password",
        command=shbtn,
    )
    search_bar.grid(row=0, column=0, pady=10, columnspan=6, padx=25)
    srch_cancel_btn.place(relx=0.63, rely=0.015)
    search_btn.place(relx=0.66, rely=0.015)
    b.grid(row=1, column=8, padx=12, pady=8)
    my_tree.place(relx=0.001, rely=0.001, width=1170, height=250)
    scr_bar.place(relx=0.982, rely=0.001, height=250)
    my_frm_d.grid(row=1, column=1, pady=10, columnspan=6, rowspan=5, sticky=NSEW)
    my_frm.place(relx=0.001, rely=0.075, width=1195, height=250)

    genpass_btn.grid(row=3, column=8, padx=12, pady=10)
    add_btn.grid(row=4, column=8, padx=12, pady=10)
    edit_btn.grid(row=5, column=8, padx=12, pady=10)
    del_btn.grid(row=6, column=8, padx=12, pady=10)

    chanmps_btn.grid(row=11, column=1, pady=180, sticky=SE)
    import_btn.grid(row=11, column=2, padx=10, pady=180, sticky=SE)
    export_btn.grid(row=11, column=3, padx=10, pady=180, sticky=SE)
    del_usr_btn.grid(row=11, column=4, padx=10, pady=180, sticky=SE)
    info_btn.grid(row=11, column=8, padx=10, pady=180, sticky=SE)
    info_btn.bind("<Enter>", lambda i: me())
    info_btn.bind("<Leave>", lambda i: infowin.destroy())

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

    if mode == "light":
        psl.config(bg="#9e9e9e")
        my_frm.config(bg="#9e9e9e")
        my_frm_d.config(bg="#9e9e9e")
        site_lbl.config(bg="#9e9e9e", fg="black")
        uname_lbl.config(bg="#9e9e9e", fg="black")
        pass_lbl.config(bg="#9e9e9e", fg="black")
        mpass_lbl.config(bg="#9e9e9e", fg="black")
    else:
        pass

    psl.mainloop()


def login_page():
    mycur.execute("SELECT userName FROM myp_users")
    data_ls = mycur.fetchall()
    ls = ["Select a Username"]

    for i in data_ls:
        ls.extend(i)

    if ls == ["Select a Username"]:
        messagebox.showinfo("Sign Up Please", "Create your account.")
    else:
        root.destroy()
        global lpg
        global user
        lpg = Tk()

        if mode == "light":
            lpg.config(bg="#9e9e9e")
        else:
            pass

        lpg.title("Login")
        place_center(lpg, "450x300", 450, 300)
        lpg.resizable(0, 0)
        lpg.iconbitmap("images\\1.ico")
        passkey = StringVar()
        cbvar = IntVar(value=0)

        lpg.tk.call("source", "sv.tcl")

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
                with open("cache.txt", "a") as fileerite:
                    fileerite.write(str(user))
                    fileerite.write("\n")

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
                        ch = True
                        ipass_ui()
                    else:
                        msgbox = messagebox.showwarning("ERROR", "WRONG PASSWORD!!")
                        if msgbox == "ok":
                            break
                pass_ls = []

        ################# STYLES ##########################################

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

        if mode == "light":
            bk_arrow = ImageTk.PhotoImage(Image.open("images\\4.png"))
            lpg.tk.call("set_theme", "light")
        elif mode == "dark":
            bk_arrow = ImageTk.PhotoImage(Image.open("images\\2.png"))
            lpg.tk.call("set_theme", "dark")

        showpass_cb = ttk.Checkbutton(
            lpg,
            text="Show Password",
            variable=cbvar,
            onvalue=1,
            offvalue=0,
            command=lambda: shbtn(cbvar, pass_ent),
            style="R.TCheckbutton",
        )
        bk_btn = ttk.Button(lpg, image=bk_arrow, command=lbk_rootw)

        # SHOWING THEM
        usern_lbl.place(relx=0.2, rely=0.3, anchor=CENTER)
        pass_lbl.place(relx=0.2, rely=0.45, anchor=CENTER)
        pass_ent.place(relx=0.7, rely=0.45, anchor=CENTER)
        showpass_cb.place(relx=0.85, rely=0.6, anchor=CENTER)
        in_btn.place(relx=0.5, rely=0.7, anchor=CENTER)
        bk_btn.place(relx=0.1, rely=0.1, anchor=CENTER)

        if ls == []:
            response = messagebox.showinfo("Info", "No users found!!")
            Label(lpg, text=response).pack()
        else:
            usern_dm = ttk.Combobox(lpg, value=ls, font=("", 14))
            usern_dm.current(0)
            usern_dm.place(relx=0.7, rely=0.3, anchor=CENTER)

        lpg.mainloop()


def signup_page():
    root.destroy()
    global spg

    spg = Tk()

    if mode == "light":
        spg.config(bg="#9e9e9e")
    else:
        pass

    spg.title("Sign Up")
    place_center(spg, "450x600", 450, 600)
    spg.resizable(0, 0)
    spg.iconbitmap("images\\1.ico")

    spg.tk.call("source", "sv.tcl")

    if mode == "light":
        bk_arrow = ImageTk.PhotoImage(Image.open("images\\4.png"))
        spg.tk.call("set_theme", "light")
    elif mode == "dark":
        bk_arrow = ImageTk.PhotoImage(Image.open("images\\2.png"))
        spg.tk.call("set_theme", "dark")

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
                "Successfully Signed Up", "You have successfull created your account"
            )
            okres = messagebox.showinfo("Reload Required", "Click ok to reload.")
            if okres == "ok":
                spg.destroy()
                system("python main.py")

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

        if net_stat == True:

            def emailc(*event):
                def otpc(*event):
                    nts = time.strftime('%M')
                    if (int(nts)-int(ts)) > 0:
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

    bk_btn = ttk.Button(
        spg,
        image=bk_arrow,
        command=sbk_rootw,
    )

    f_name_lbl.grid(row=3, column=1, padx=10, pady=10)
    l_name_lbl.grid(row=4, column=1, padx=10, pady=10)
    u_name_lbl.grid(row=5, column=1, padx=10, pady=10)

    f_name_ent.grid(row=3, column=2, padx=10, pady=10)
    l_name_ent.grid(row=4, column=2, padx=10, pady=10)
    u_name_ent.grid(row=5, column=2, padx=10, pady=10)
    bk_btn.grid(row=1, column=1, padx=10, pady=20)

    spg.mainloop()


def rootw():
    global root
    global mode

    def change_mode():
        global mode

        def darks():
            global mode
            with open("mode.txt", "w") as f:
                f.write("dark")

            q = messagebox.askokcancel(
                "Reload",
                "Reload Required\nClick OK to Reload.\nClick Cancel to reload mannually later.\nNOTE:THEME WILL CHANGE ONLY AFTER RELOAD.",
            )
            if q == True:
                mode = "dark"
                chngm.destroy()
                root.destroy()
                system("python main.py")
            elif q == False:
                pass
            else:
                pass

        def lights():
            global mode
            with open("mode.txt", "w") as f:
                f.write("light")

            q = messagebox.askokcancel(
                "Reload",
                "Reload Required\nClick OK to Reload.\nClick Cancel to reload mannually later.\nNOTE:THEME WILL CHANGE ONLY AFTER RELOAD.",
            )
            if q == True:
                mode = "light"
                chngm.destroy()
                root.destroy()
                system("python main.py")
            elif q == False:
                pass
            else:
                pass

        chngm = Toplevel()
        chngm.title("Theme")
        chngm.iconbitmap("images\\1.ico")
        place_center(chngm, "150x150", 150, 150)
        if mode == "light":
            lgt = ImageTk.PhotoImage(file="images//8.png")
            bgt = ImageTk.PhotoImage(file="images//9.png")
        if mode == "dark":
            lgt = ImageTk.PhotoImage(file="images//6.png")
            bgt = ImageTk.PhotoImage(file="images//7.png")

        lgt_btn = ttk.Button(chngm, image=lgt, command=lights)
        bgt_btn = ttk.Button(chngm, image=bgt, command=darks)
        lgt_btn.place(relx=0.5, rely=0.3, anchor=CENTER)
        bgt_btn.place(relx=0.5, rely=0.7, anchor=CENTER)
        chngm.mainloop()

    root = Tk()

    if mode == "light":
        root.config(bg="#9e9e9e")
    else:
        pass

    root.title("Password Manager")
    place_center(root, "300x300", 300, 300)
    root.iconbitmap("images\\1.ico")
    root.resizable(0, 0)

    root.tk.call("source", "sv.tcl")
    root.tk.call("set_theme", mode)

    signin_btn = ttk.Button(root, text="Sign In", command=login_page, width=8)
    signup_btn = ttk.Button(root, text="Sign Up", command=signup_page, width=8)
    exit_btn = ttk.Button(root, text="Exit", command=lambda: [sys.exit()], width=8)
    mode_btn = ttk.Button(root, text="Mode", command=lambda: [change_mode()])

    signin_btn.place(
        relx=0.5,
        rely=0.35,
        anchor=CENTER,
    )
    signup_btn.place(relx=0.5, rely=0.5, anchor=CENTER)
    exit_btn.place(relx=0.5, rely=0.65, anchor=CENTER)
    mode_btn.place(relx=0.975, rely=0.025, anchor=NE)

    root.mainloop()


########################## TKINTER MAIN ###############################

check = open("cache.txt", "r", newline="\n")
ls = check.readlines()
check.close()

global mode
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
    check_n = ls[-1]
    ui(check_n)
except:
    rootw()

# thanks to github:@rdbende for the sv_ttk theme