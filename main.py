import csv
import requests
import tkinter.ttk as ttk
from os import system
from time import *
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.font import BOLD
from database import *
from mypfuncs import *
from PIL import Image, ImageTk
import webbrowser as wb


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


########################## CLASS ###############################


class passwordmenu:
    def __init__(self, root, uid, close, open_e):
        def openthat(*e):
            mycur.execute("SELECT passId FROM myp_data WHERE userId = " + str(uid))
            passids = mycur.fetchall()
            passid_ls = []
            for i in passids:
                passid_ls.extend(i)

            passid_dict = {}

            for j in range(len(passid_ls)):
                passid_dict[j + 1] = passid_ls[j]

            command = "select website from myp_data where passId =" + str(
                passid_dict[int(ent.get())]
            )
            mycur.execute(command)
            site_ls = []
            for i in mycur:
                site_ls.append(i)
            site = str(site_ls[0])[2:-3]
            print(site)
            wb.open(site)
            link_win.destroy()

        def link_click():
            global link_win
            global ent
            link_win = Toplevel()
            link_win.config(bg="#1e1e1e")
            link_win.title("Password Manager")
            link_win.iconbitmap("images\\1.ico")
            link_win.geometry("400x50")
            link_win.wm_attributes('-topmost', True)
            link_win.resizable(0, 0)

            lbl = Label(
                link_win, text="Enter the ID: ", bg="#1e1e1e", fg="white", font=("", 14)
            )
            ent = Entry(
                link_win, font=("", 14), bg="#28282E", fg="white", borderwidth=0
            )

            lbl.grid(row=1, column=1, padx=10, pady=10)
            ent.grid(row=1, column=2, padx=10, pady=10)
            ent.bind("<Return>", openthat)

            link_win.mainloop()

        global len_1
        mycur.execute("USE myp;")
        root.wm_attributes("-transparentcolor", "red")
        self.img = ImageTk.PhotoImage(file="images//6.png")

        self.main_canvas = Canvas(
            root, borderwidth=0, width=1350, height=650, background="#1e1e1e"
        )
        self.main_canvas.grid(row=0, column=0)

        self.hscroll = Scrollbar(
            root, orient=HORIZONTAL, command=self.main_canvas.xview
        )
        self.hscroll.grid(row=1, column=0, sticky=EW)

        self.scroll = Scrollbar(root, orient=VERTICAL, command=self.main_canvas.yview)
        self.scroll.grid(row=0, column=2, sticky=NS)

        self.main_canvas.configure(yscrollcommand=self.scroll.set)
        self.main_canvas.configure(xscrollcommand=self.hscroll.set)
        self.main_canvas.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(
                scrollregion=self.main_canvas.bbox("all")
            ),
        )

        self.second_frame = Frame(
            self.main_canvas,
            borderwidth=0,
            background="red",
            width=1340,
            height=650,
        )
        self.main_canvas.create_window((0, 0), window=self.second_frame)
        imglbl = Label(self.second_frame, image=self.img)
        imglbl.place(x=0, y=0)
        self.num_header = Label(
            self.second_frame, text="Id", font=("", 14, BOLD), bg="#332537", fg="white"
        )
        self.site_header = Label(
            self.second_frame,
            text="Website",
            font=("", 14, BOLD),
            bg="#332537",
            fg="white",
        )
        self.uname_header = Label(
            self.second_frame,
            text="Username",
            font=("", 14, BOLD),
            bg="#332537",
            fg="white",
        )
        self.pass_header = Label(
            self.second_frame,
            text="Password",
            font=("", 14, BOLD),
            bg="#332537",
            fg="white",
        )

        self.num_header.grid(row=0, column=1, padx=20, pady=10, sticky=E)
        self.site_header.grid(row=0, column=2, padx=20, pady=10, sticky=W)
        self.uname_header.grid(row=0, column=4, padx=20, pady=10, sticky=W)
        self.pass_header.grid(row=0, column=6, padx=20, pady=10)

        mycur.execute("SELECT passId FROM myp_data WHERE userId=" + str(uid))
        self.uiddata = mycur.fetchall()
        self.uidls = []
        for i in self.uiddata:
            self.uidls.extend(i)

        self.uls = []

        for uidn in self.uidls:
            mycur.execute(
                "SELECT website, loginName, loginPass, passId FROM myp_data WHERE passId="
                + str(uidn)
            )
            for data in mycur.fetchall():
                self.uls.append(data)

            for i in range(len(self.uls)):
                self.p = decrypt(str(self.uls[i][2]))
                self.p_len = len(str(self.uls[i][2]))

                self.num_lbl = Label(
                    self.second_frame,
                    text=i + 1,
                    font=("", 12),
                    fg="white",
                    bg="#1e1e1e",
                    borderwidth=0,
                )
                self.site_lbl = Button(
                    self.second_frame,
                    text=self.uls[i][0],
                    font=("", 12),
                    fg="white",
                    bg="#1e1e1e",
                    activebackground="#1e1e1e",
                    borderwidth=0,
                    width=30,
                    command=link_click,
                )
                self.uname_l = Label(
                    self.second_frame,
                    text=self.uls[i][1],
                    font=("", 12),
                    fg="white",
                    bg="#1e1e1e",
                )
                self.pass_ent = Entry(
                    self.second_frame,
                    font=("", 12),
                    fg="black",
                    bg="#28282E",
                    borderwidth=0,
                    show="•",
                )

                self.num_lbl.grid(row=i + 1, column=1, padx=20, pady=10, sticky=E)
                self.site_lbl.grid(row=i + 1, column=2, padx=10, pady=10, sticky=W)
                self.uname_l.grid(row=i + 1, column=4, padx=30, pady=10, sticky=W)
                self.pass_ent.grid(row=i + 1, column=6, padx=120, pady=10)

                self.pass_ent.insert(0, (self.p))
                self.pass_ent.configure(state="readonly")

        len_1 = len(self.uls) + 2

        self.showpass_btn = Button(
            self.second_frame,
            image=close,
            borderwidth=0,
            bg="#1e1e1e",
            activebackground="#1e1e1e",
        )

        self.showpass_btn.configure(command=lambda: showpass(open_e, self.showpass_btn))

        if len(self.uls) == 0:
            self.showpass_btn.configure(state="disabled")
        else:
            self.showpass_btn.grid(row=1, column=7, rowspan=5, padx=10, pady=10)

        def showpass(open_e, widget):

            mc_ls = passdget(uid)
            if widget.cget("image") == "pyimage2":
                widget.configure(image=close)
                self.uidls1 = []
                for i in self.uiddata:
                    self.uidls1.extend(i)

                self.uls1 = []

                for uidn in self.uidls:
                    mycur.execute(
                        "SELECT website, loginName, loginPass, passId FROM myp_data WHERE passId="
                        + str(uidn)
                    )
                    for data in mycur.fetchall():
                        self.uls1.append(data)
                    for i in range(len(self.uls)):
                        p2 = decrypt(str(self.uls[i][2]))
                        text1 = Entry(
                            self.second_frame,
                            font=("", 12),
                            fg="black",
                            show="•",
                            bg="#28282E",
                            borderwidth=0,
                        )
                        text1.grid(row=i + 1, column=6, padx=120, pady=10)
                        text1.insert(0, (p2))
                        text1.configure(state="readonly")

            elif widget.cget("image") == "pyimage1":

                def mcp_check(e):
                    if hashcrypt(str(ent.get())) == str(mc_ls[0]):
                        widget.configure(image=open_e)

                        self.uidls1 = []
                        for i in self.uiddata:
                            self.uidls1.extend(i)

                        self.uls1 = []

                        for uidn in self.uidls:
                            mycur.execute(
                                "SELECT website, loginName, loginPass, passId FROM myp_data WHERE passId="
                                + str(uidn)
                            )
                            for data in mycur.fetchall():
                                self.uls1.append(data)
                            for i in range(len(self.uls)):
                                p1 = decrypt(str(self.uls[i][2]))
                                text2 = Entry(
                                    self.second_frame, font=("", 12), fg="black"
                                )
                                text2.grid(row=i + 1, column=6, padx=120, pady=10)
                                text2.insert(0, (p1))
                                text2.configure(state="readonly")
                        masterc.destroy()
                    else:
                        messagebox.showerror(
                            "Wrong Password", "Enter the correct password"
                        )
                        masterc.destroy()

                masterc = Toplevel()
                masterc.title("Verification")
                masterc.wm_attributes('-topmost', True)
                masterc.iconbitmap("images\\1.ico")
                masterc.configure(bg="#1e1e1e")

                lbl = Label(
                    masterc,
                    text="Enter Master Password: ",
                    font=("", 13),
                    fg="white",
                    bg="#1e1e1e",
                )
                lbl.grid(row=1, column=1, padx=10, pady=10)

                ent = Entry(
                    masterc,
                    font=("", 13),
                    show="•",
                    bg="#28282E",
                    fg="white",
                    borderwidth=0,
                )
                ent.grid(row=1, column=2, padx=10, pady=10)

                ent.bind("<Return>", mcp_check)

                masterc.mainloop()


class addedit:
    def __init__(self, uid, psl, open_e, close, addr, editr):
        def adds():
            if ".com" in str(site_ent.get()):
                if str(site_ent.get()).startswith("https://") == True:
                    web = str(site_ent).get()
                else:
                    web = "https://" + str(site_ent.get())
            else:
                web = str(site_ent.get())

            un = str(usern_ent.get())
            ps = encrypt(str(pass_ent.get()))
            reps = encrypt(str(repass_ent.get()))
            mps = str(mpass_ent.get())

            if reps == ps:
                pass_ls = passdget(uid)

                if hashcrypt(mps) == str(pass_ls[0]):
                    insintodata(web, un, ps, str(uid))
                    mydb.commit()
                    messagebox.showinfo("Success", "Data added successfully")
                    adk.destroy()
                    psl.destroy()
                    system("python main.py")

                else:
                    messagebox.showerror(
                        "Wrong password", "Please enter correct Master Password"
                    )
            else:
                messagebox.showerror("Unsuccessful", "Passwords don't match!")

        def generpass():
            pass_ent.delete(0, END)
            repass_ent.delete(0, END)
            gvar = password(12)
            pass_ent.insert(0, gvar)
            repass_ent.insert(0, gvar)

        mycur.execute("SELECT passId FROM myp_data WHERE userId = " + str(uid))
        passids = mycur.fetchall()
        passid_ls = []
        for i in passids:
            passid_ls.extend(i)

        passid_dict = {}

        for j in range(len(passid_ls)):
            passid_dict[j + 1] = passid_ls[j]

        if (editr == "yes") and (addr == "no"):

            def editing(*event):
                try:
                    passid_int = int(id_ent.get())
                    passid = ent.get()
                    pass_ls = passdget(uid)

                    if hashcrypt(passid) == str(pass_ls[0]):
                        if passid_int not in passid_dict.keys():
                            messagebox.showerror(
                                "Enter proper Id",
                                "Enter only Id's that are visible on the menu.",
                            )
                            edid.destroy()
                        else:

                            def edits():
                                web = "https://" + str(site_ent.get())
                                un = str(usern_ent.get())
                                ps = encrypt(str(pass_ent.get()))
                                reps = encrypt(str(repass_ent.get()))
                                mps = str(mpass_ent.get())

                                if reps == ps:
                                    pass_ls = passdget(uid)

                                    if hashcrypt(mps) == str(pass_ls[0]):
                                        mycur.execute(
                                            "UPDATE myp_data SET website = '"
                                            + web
                                            + "', loginName = '"
                                            + un
                                            + "', loginPass = '"
                                            + ps
                                            + "' WHERE passId = "
                                            + str(ele)
                                        )
                                        mydb.commit()
                                        messagebox.showinfo(
                                            "Success", "Data edited successfully"
                                        )
                                        adk.destroy()
                                        psl.destroy()
                                        system("python main.py")
                                    else:
                                        messagebox.showerror(
                                            "Wrong password",
                                            "Please enter correct Master Password",
                                        )
                                else:
                                    messagebox.showerror(
                                        "Unsuccessful", "Passwords don't match!"
                                    )

                            def revert():
                                mycur.execute(
                                    "SELECT website, loginName, loginPass FROM myp_data WHERE passId="
                                    + str(ele)
                                )
                                editdata = []
                                for i in mycur.fetchall():
                                    editdata.extend(i)

                                site_ent.delete(0, END)
                                usern_ent.delete(0, END)
                                pass_ent.delete(0, END)
                                repass_ent.delete(0, END)

                                site_ent.insert(0, str(editdata[0][8:]))
                                usern_ent.insert(0, str(editdata[1]))
                                pass_ent.insert(0, decrypt(str(editdata[2])))
                                repass_ent.insert(0, decrypt(str(editdata[2])))

                            adk = Toplevel()
                            adk.title("Edit Data")
                            adk.wm_attributes("-topmost", True)
                            adk.iconbitmap("images\\1.ico")
                            adk.configure(bg="#1e1e1e")

                            site_lbl = Label(
                                adk,
                                text="Website:",
                                font=("", 13),
                                bg="#1e1e1e",
                                fg="white",
                            )
                            site_lbl.grid(row=1, column=1, padx=10, pady=10, sticky=W)

                            site_ent = Entry(
                                adk,
                                font=("", 13),
                                bg="#28282E",
                                fg="white",
                                borderwidth=0,
                            )
                            site_ent.grid(row=1, column=2, padx=10, pady=10)

                            usern_lbl = Label(
                                adk,
                                text="Username:",
                                font=("", 13),
                                bg="#1e1e1e",
                                fg="white",
                            )
                            usern_lbl.grid(row=2, column=1, padx=10, pady=10, sticky=W)

                            usern_ent = Entry(
                                adk,
                                font=("", 13),
                                bg="#28282E",
                                fg="white",
                                borderwidth=0,
                            )
                            usern_ent.grid(row=2, column=2, padx=10, pady=10)

                            pass_lbl = Label(
                                adk,
                                text="Password:",
                                font=("", 13),
                                bg="#1e1e1e",
                                fg="white",
                            )
                            pass_lbl.grid(row=3, column=1, padx=10, pady=10, sticky=W)

                            pass_ent = Entry(
                                adk,
                                font=("", 13),
                                bg="#28282E",
                                fg="white",
                                borderwidth=0,
                            )
                            pass_ent.grid(row=3, column=2, padx=10, pady=10)

                            repass_lbl = Label(
                                adk,
                                text="Re-Enter Password:",
                                font=("", 13),
                                bg="#1e1e1e",
                                fg="white",
                            )
                            repass_lbl.grid(row=4, column=1, padx=10, pady=10, sticky=W)

                            repass_ent = Entry(
                                adk,
                                font=("", 13),
                                bg="#28282E",
                                fg="white",
                                borderwidth=0,
                            )
                            repass_ent.grid(row=4, column=2, padx=10, pady=10)

                            mpass_lbl = Label(
                                adk,
                                text="Master Password:",
                                font=("", 13),
                                bg="#1e1e1e",
                                fg="white",
                            )
                            mpass_lbl.grid(row=5, column=1, padx=10, pady=10, sticky=W)

                            mpass_ent = Entry(
                                adk,
                                font=("", 13),
                                show="•",
                                bg="#28282E",
                                fg="white",
                                borderwidth=0,
                            )
                            mpass_ent.grid(row=5, column=2, padx=10, pady=10)
                            addedit_btn = Button(
                                adk,
                                font=("", 13),
                                bg="#1e1e1e",
                                fg="white",
                                command=edits,
                                text="Save",
                            )
                            addedit_btn.grid(
                                row=6, column=1, columnspan=2, padx=10, pady=20
                            )

                            revert_btn = Button(
                                adk,
                                text="Revert",
                                font=("", 13),
                                bg="#1e1e1e",
                                fg="white",
                                command=revert,
                            )
                            revert_btn.grid(row=6, column=2, padx=10, pady=20)

                            Label(
                                adk,
                                text="(Master Password cannot be edited here. Enter the correct Master Password)",
                                font=("", 12),
                                bg="#1e1e1e",
                                fg="white",
                            ).grid(row=7, column=1, columnspan=2, pady=20)

                            adk.focus_force

                            global ele
                            ele = passid_dict[passid_int]
                            mycur.execute(
                                "SELECT website, loginName, loginPass FROM myp_data WHERE passId="
                                + str(ele)
                            )
                            editdata = []
                            for i in mycur.fetchall():
                                editdata.extend(i)
                            edid.destroy()
                            site_ent.insert(0, str(editdata[0][8:]))
                            usern_ent.insert(0, str(editdata[1]))
                            pass_ent.insert(0, decrypt(str(editdata[2])))
                            repass_ent.insert(0, decrypt(str(editdata[2])))

                    else:
                        messagebox.showerror(
                            "Wrong password", "Please enter correct Master Password"
                        )
                        edid.destroy()

                except ValueError:
                    messagebox.showerror("Invalid Entry", "Please enter only numbers.")
                    edid.destroy()
                    adk.destroy()

            edid = Toplevel()
            edid.title("Edit Data")
            edid.wm_attributes('-topmost', True)
            edid.iconbitmap("images\\1.ico")
            edid.configure(bg="#1e1e1e")

            lbl = Label(
                edid,
                text="Enter Master Password: ",
                font=("", 13),
                fg="white",
                bg="#1e1e1e",
            )
            ent = Entry(
                edid, font=("", 13), show="•", bg="#28282E", fg="white", borderwidth=0
            )

            id_lbl = Label(
                edid,
                text="Enter the Id : ",
                font=("", 13),
                bg="#1E1E1E",
                fg="white",
                borderwidth=0,
            )
            id_ent = Entry(edid, font=("", 13), bg="#28282E", fg="white", borderwidth=0)

            lbl.grid(row=1, column=1, padx=10, pady=10)
            ent.grid(row=1, column=2, padx=10, pady=10)
            id_lbl.grid(row=2, column=1, padx=10, pady=10)
            id_ent.grid(row=2, column=2, padx=10, pady=10)

            id_ent.bind("<Return>", editing)

            edid.mainloop()

        elif (addr == "yes") and (editr == "no"):
            adk = Toplevel()
            adk.title("Add Data")
            adk.wm_attributes('-topmost', True)
            adk.iconbitmap("images\\1.ico")
            adk.configure(bg="#1e1e1e")

            site_lbl = Label(
                adk, text="Website:", font=("", 13), bg="#1e1e1e", fg="white"
            )
            site_lbl.grid(row=1, column=1, padx=10, pady=10, sticky=W)

            site_ent = Entry(
                adk, font=("", 13), bg="#28282E", fg="white", borderwidth=0
            )
            site_ent.grid(row=1, column=2, padx=10, pady=10)

            usern_lbl = Label(
                adk, text="Username:", font=("", 13), bg="#1e1e1e", fg="white"
            )
            usern_lbl.grid(row=2, column=1, padx=10, pady=10, sticky=W)

            usern_ent = Entry(
                adk, font=("", 13), bg="#28282E", fg="white", borderwidth=0
            )
            usern_ent.grid(row=2, column=2, padx=10, pady=10)

            pass_lbl = Label(
                adk, text="Password:", font=("", 13), bg="#1e1e1e", fg="white"
            )
            pass_lbl.grid(row=3, column=1, padx=10, pady=10, sticky=W)

            pass_ent = Entry(
                adk, font=("", 13), bg="#28282E", fg="white", borderwidth=0
            )
            pass_ent.grid(row=3, column=2, padx=10, pady=10)

            repass_lbl = Label(
                adk, text="Re-Enter Password:", font=("", 13), bg="#1e1e1e", fg="white"
            )
            repass_lbl.grid(row=4, column=1, padx=10, pady=10, sticky=W)

            repass_ent = Entry(
                adk, font=("", 13), bg="#28282E", fg="white", borderwidth=0
            )
            repass_ent.grid(row=4, column=2, padx=10, pady=10)

            mpass_lbl = Label(
                adk, text="Master Password:", font=("", 13), bg="#1e1e1e", fg="white"
            )
            mpass_lbl.grid(row=5, column=1, padx=10, pady=10, sticky=W)

            mpass_ent = Entry(
                adk, font=("", 13), show="•", bg="#28282E", fg="white", borderwidth=0
            )
            mpass_ent.grid(row=5, column=2, padx=10, pady=10)
            addedit_btn = Button(
                adk, text="none", font=("", 13), bg="#1e1e1e", fg="white"
            )
            addedit_btn.grid(row=6, column=1, columnspan=2, padx=10, pady=20)

            addedit_btn.configure(command=adds, text="Add")
            optional = Label(
                adk,
                text="(Generating Password is completely optioal.)",
                font=("", 12),
                bg="#1e1e1e",
                fg="white",
            )
            optional.grid(row=7, column=1, padx=10, pady=10)
            gen_pass_btn = Button(
                adk,
                text="Generate Password",
                font=("", 13),
                bg="#1e1e1e",
                fg="white",
                command=generpass,
            )
            gen_pass_btn.grid(row=3, column=3)

            adk.mainloop()


class loading_screen:
    def __init__(self, root, time):
        global top
        top = Toplevel()
        top.wm_attributes('-topmost', True)
        top.overrideredirect(1)
        x = root.winfo_x()
        y = root.winfo_y()
        top.geometry("+%d+%d" % (x + 500, y + 200))
        top.lift()
        top.after(time, lambda: top.destroy())
        frameCnt = 20
        frames = [
            PhotoImage(file="images/5.gif", format="gif -index %i" % (i))
            for i in range(frameCnt)
        ]

        def update(ind):

            frame = frames[ind]
            ind += 1
            if ind == frameCnt:
                ind = 0
            label.configure(image=frame)
            top.after(100, update, ind)

        label = Label(top)
        label.pack()
        top.after(0, update, 0)


########################## FUNCTIONS ###############################
def internet_stat(url="https://www.google.com/", timeout=3):
    try:
        r = requests.head(url=url, timeout=timeout)
        return True
    except requests.ConnectionError as e:
        return False


net_stat = internet_stat()


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
    psl.destroy()


def ui(uid):
    def signout():
        psl.destroy()
        open("cache.txt", "w")
        rootw()

    def delete(e):
        try:
            pass_ls = passdget(uid)
            if hashcrypt(ent_p.get()) == str(pass_ls[0]):
                passid_int = int(ent.get())
                if passid_int not in passid_dict.keys():
                    messagebox.showerror(
                        "Enter proper Id",
                        "Enter only Id's that are visible on the menu.",
                    )
                    ddk.destroy()
                else:
                    dele = passid_dict[passid_int]
                    mycur.execute("DELETE FROM myp_data WHERE passId = " + str(dele))
                    mydb.commit()
                    ddk.destroy()
                    psl.destroy()
                    system("python main.py")
            else:
                messagebox.showerror(
                    "Wrong password", "Please enter correct Master Password"
                )
                ddk.destroy()

        except ValueError:
            messagebox.showerror("Invalid Entry", "Please enter only numbers.")
            ddk.destroy()

    def deletedata():
        global ent
        global ent_p
        global passid_dict
        global ddk
        mycur.execute("SELECT passId FROM myp_data WHERE userId = " + str(uid))
        passids = mycur.fetchall()
        passid_ls = []
        for i in passids:
            passid_ls.extend(i)

        passid_dict = {}

        for j in range(len(passid_ls)):
            passid_dict[j + 1] = passid_ls[j]

        mydb.commit()

        ddk = Tk()
        ddk.title("Delete Data")
        ddk.wm_attributes('-topmost', True)
        ddk.iconbitmap("images\\1.ico")
        ddk.configure(bg="#1e1e1e")

        lbl = Label(
            ddk, text="Enter the Id : ", font=("", 13), bg="#1e1e1e", fg="white"
        )
        lbl.grid(row=2, column=1, padx=10, pady=10)

        ent = Entry(ddk, font=("", 13), bg="#28282E", fg="white", borderwidth=0)
        ent.grid(row=2, column=2, padx=10, pady=10)

        lbl_p = Label(
            ddk, text="Enter Master Password: ", font=("", 13), fg="white", bg="#1e1e1e"
        )
        ent_p = Entry(
            ddk, font=("", 13), show="•", bg="#28282E", fg="white", borderwidth=0
        )

        lbl_p.grid(row=1, column=1, padx=10, pady=10)
        ent_p.grid(row=1, column=2, padx=10, pady=10)

        ent.bind("<Return>", delete)

        ddk.mainloop()

    y = "yes"
    n = "no"

    def editdata():
        addedit(str(uid), psl, open_e, close, n, y)

    def adddata():
        addedit(str(uid), psl, open_e, close, y, n)

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
        mstc.wm_attributes('-topmost', True)
        mstc.title("Confirmation")
        mstc.iconbitmap("images\\1.ico")
        mstc.configure(bg="#1e1e1e")

        cb_style = ttk.Style()
        cb_style.configure("R.TCheckbutton", foreground="white", background="#1e1e1e")

        omp_lbl = Label(
            mstc, text="Old Master Password :", font=("", 13), bg="#1e1e1e", fg="white"
        )
        omp_lbl.grid(row=1, column=1, padx=10, pady=10)

        omp_ent = Entry(
            mstc, font=("", 13), show="•", bg="#28282E", fg="white", borderwidth=0
        )
        omp_ent.grid(row=1, column=2, padx=10, pady=10)

        nmp_lbl = Label(
            mstc, text="New Master Password :", font=("", 13), bg="#1e1e1e", fg="white"
        )
        nmp_lbl.grid(row=2, column=1, padx=10, pady=10)

        nmp_ent = Entry(
            mstc, font=("", 13), show="•", bg="#28282E", fg="white", borderwidth=0
        )
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

        change_btn = Button(
            mstc,
            text="Change",
            font=("", 13),
            bg="#1e1e1e",
            fg="white",
            command=mc_check,
        )
        change_btn.grid(row=4, column=1, columnspan=2, padx=10, pady=10)

    def imp_data():
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
        ls.remove(["name", "url", "username", "password"])
        try:
            for i in range(len(ls)):
                web = ls[i][1]
                logn = ls[i][2]
                logp = encrypt(str(ls[i][3]))
                insintodata(web, logn, logp, uid)
            messagebox.showinfo("Success", "Successfuly imported!!")
            messagebox.showinfo("Reload Required", "Click Ok to reload")
            psl.destroy()
            system("python main.py")
        except:
            psl.destroy()
            system("python main.py")

    def exp_data():
        def mc_check(*e):
            if hashcrypt(str(ent.get())) == str(pass_ls[0]):
                des.destroy()
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
            else:
                messagebox.showerror("Wrong Password", "Enter the correct password")
                des.destroy()

        pass_ls = passdget(uid)

        des = Toplevel()
        des.title("Verification")
        des .wm_attributes('-topmost', True)
        des.iconbitmap("images\\1.ico")
        des.configure(bg="#1e1e1e")

        lbl = Label(
            des, text="Master Password :", font=("", 13), bg="#1e1e1e", fg="white"
        )
        lbl.grid(row=1, column=1, padx=10, pady=10)

        ent = Entry(
            des, font=("", 13), show="•", bg="#28282E", fg="white", borderwidth=0
        )
        ent.grid(row=1, column=2, padx=10, pady=10)

        ent.bind("<Return>", mc_check)

    def deluser():
        def mc_check(e):
            if hashcrypt(str(ent.get())) == str(pass_ls[0]):
                des.destroy()
                mycur.execute("SELECT email FROM myp_users WHERE userId = " + str(uid))
                els = mycur.fetchall()
                for i in els:
                    if i == (None,):
                        continue
                    else:
                        byemail(i[0])
                mycur.execute("SELECT passId FROM myp_data WHERE userId = " + str(uid))
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
                des.destroy()

        pass_ls = passdget(uid)

        des = Toplevel()
        des.wm_attributes('-topmost', True)
        des.title("Confirmation")
        des.iconbitmap("images\\1.ico")
        des.configure(bg="#1e1e1e")

        lbl = Label(
            des, text="Master Password :", font=("", 13), bg="#1e1e1e", fg="white"
        )
        lbl.grid(row=1, column=1, padx=10, pady=10)

        ent = Entry(
            des, font=("", 13), show="•", bg="#28282E", fg="white", borderwidth=0
        )
        ent.grid(row=1, column=2, padx=10, pady=10)

        ent.bind("<Return>", mc_check)

    global psl
    global pass_btn
    psl = Tk()
    psl.title("Passwords")
    psl.config(bg="#1e1e1e")
    psl.state("zoomed")
    psl.iconbitmap("images\\1.ico")

    close = ImageTk.PhotoImage(Image.open("images\\2.png"))
    open_e = ImageTk.PhotoImage(Image.open("images\\3.png"))

    passwordmenu(psl, str(uid), close, open_e)

    menu = Menu(psl, fg="white", background="#1e1e1e", font=("", 20))
    psl.config(menu=menu)

    more = Menu(menu)
    more.add_command(label="Change Master Password", command=mstrchange)
    more.add_separator()
    more.add_command(label="Import data", command=imp_data)
    more.add_command(label="Export data", command=exp_data)
    more.add_separator()
    more.add_command(label="Delete User!!", command=deluser)

    menu.add_command(label="Add data", command=adddata)
    menu.add_command(label="Edit data", command=editdata)
    menu.add_command(label="Delete data", command=deletedata)
    menu.add_command(label="Sign out", command=signout)
    menu.add_cascade(label="•••", menu=more)

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
        bg_login = ImageTk.PhotoImage(file="images//8.png")
        lpg.title("Login")
        lpg.config(bg="#1e1e1e")
        lpg.geometry("450x300")
        lpg.resizable(0, 0)
        lpg.iconbitmap("images\\1.ico")
        Label(lpg, image=bg_login, borderwidth=0).place(x=0, y=0)
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
                        ch == True
                        ipass_ui()
                    else:
                        msgbox = messagebox.showwarning("ERROR", "WRONG PASSWORD!!")
                        if msgbox == "ok":
                            break
                pass_ls = []

        bk_arrow = ImageTk.PhotoImage(Image.open("images\\4.png"))
        ################# STYLES ##########################################
        cb_style = ttk.Style()
        cb_style.configure("R.TCheckbutton", foreground="white", background="#1e1e1e")

        ###WIDGETS
        usern_lbl = Label(
            lpg, text="Username:", font=("", 14), bg="#1e1e1e", fg="white"
        )
        pass_lbl = Label(lpg, text="Password:", font=("", 14), bg="#1e1e1e", fg="white")
        pass_ent = Entry(
            lpg,
            textvariable=passkey,
            show="•",
            font=("", 14),
            bg="#28282E",
            fg="white",
            borderwidth=0,
        )
        pass_ent.bind("<Return>", login)
        in_btn = Button(
            lpg,
            text="Sign In",
            command=login,
            font=("", 14),
            width=20,
            bg="#28282E",
            fg="white",
            borderwidth=0,
            activebackground="#28282E",
        )
        showpass_cb = ttk.Checkbutton(
            lpg,
            text="Show Password",
            variable=cbvar,
            onvalue=1,
            offvalue=0,
            command=lambda: shbtn(cbvar, pass_ent),
            style="R.TCheckbutton",
        )
        bk_btn = Button(
            lpg,
            image=bk_arrow,
            command=lbk_rootw,
            activebackground="#1e1e1e",
            borderwidth=0,
            bg="#1e1e1e",
        )

        # SHOWING THEM
        usern_lbl.place(relx=0.2, rely=0.3, anchor=CENTER)
        pass_lbl.place(relx=0.2, rely=0.45, anchor=CENTER)
        pass_ent.place(relx=0.7, rely=0.45, anchor=CENTER)
        showpass_cb.place(relx=0.85, rely=0.55, anchor=CENTER)
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
    spg.title("Sign Up")
    spg.config(bg="#1e1e1e")
    spg.geometry("450x600")
    spg.resizable(0, 0)
    spg.iconbitmap("images\\1.ico")

    lgp_bg1 = ImageTk.PhotoImage(file="images//9.png")
    lgp_bg2 = ImageTk.PhotoImage(file="images//10.png")

    passkey = StringVar()
    repasskey = StringVar()
    cbvar = IntVar(value=0)
    bk_arrow = ImageTk.PhotoImage(Image.open("images\\4.png"))

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
                    global urepass_ent
                    global upass_ent

                    js = eval(otp_ent.get())
                    if js == otp:

                        cb_style = ttk.Style()
                        cb_style.configure(
                            "R.TCheckbutton", foreground="white", background="#1e1e1e"
                        )

                        global upass_lbl
                        upass_lbl = Label(
                            spg,
                            text="Master Password:",
                            font=("", 14),
                            bg="#1e1e1e",
                            fg="white",
                        )
                        global upass_ent
                        upass_ent = Entry(
                            spg,
                            textvariable=passkey,
                            show="•",
                            font=("", 14),
                            bg="#28282E",
                            fg="white",
                            borderwidth=0,
                        )
                        global urepass_lbl
                        urepass_lbl = Label(
                            spg,
                            text="Re-Enter Password:",
                            font=("", 14),
                            bg="#1e1e1e",
                            fg="white",
                        )
                        global urepass_ent
                        urepass_ent = Entry(
                            spg,
                            textvariable=repasskey,
                            show="•",
                            font=("", 14),
                            bg="#28282E",
                            fg="white",
                            borderwidth=0,
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
                            style="R.TCheckbutton",
                        )
                        Label(spg, image=lgp_bg1, borderwidth=0).place(x=0, y=441)
                        global up_btn
                        up_btn = Button(
                            spg,
                            text="Sign Up",
                            command=signup,
                            font=("", 14),
                            width=16,
                            bg="#28282E",
                            fg="white",
                            borderwidth=0,
                            activebackground="#28282E",
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

                loading_screen(spg, 6000)
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
                        otp = otpmail(email_ent.get())
                        print(otp)
                        global otp_lbl
                        otp_lbl = Label(
                            spg,
                            text="OTP:      ",
                            font=("", 14),
                            bg="#1e1e1e",
                            fg="white",
                        )
                        global otp_ent
                        otp_ent = Entry(
                            spg, font=("", 14), bg="#28282E", fg="white", borderwidth=0
                        )
                        otp_ent.bind("<Return>", otpc)

                        otp_lbl.grid(row=7, column=1, padx=10, pady=10)
                        otp_ent.grid(row=7, column=2, padx=10, pady=10)

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
                    email_lbl = Label(
                        spg, text="E-Mail:   ", font=("", 14), bg="#1e1e1e", fg="white"
                    )
                    global email_ent
                    email_ent = Entry(
                        spg, font=("", 14), bg="#28282E", fg="white", borderwidth=0
                    )
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
                    cb_style = ttk.Style()
                    cb_style.configure(
                        "R.TCheckbutton", foreground="white", background="#1e1e1e"
                    )

                    global upass_lbl
                    upass_lbl = Label(
                        spg,
                        text="Master Password:",
                        font=("", 14),
                        bg="#1e1e1e",
                        fg="white",
                    )
                    global upass_ent
                    upass_ent = Entry(
                        spg,
                        textvariable=passkey,
                        show="•",
                        font=("", 14),
                        bg="#28282E",
                        fg="white",
                        borderwidth=0,
                    )
                    global urepass_lbl
                    urepass_lbl = Label(
                        spg,
                        text="Re-Enter Password:",
                        font=("", 14),
                        bg="#1e1e1e",
                        fg="white",
                    )
                    global urepass_ent
                    urepass_ent = Entry(
                        spg,
                        textvariable=repasskey,
                        show="•",
                        font=("", 14),
                        bg="#28282E",
                        fg="white",
                        borderwidth=0,
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
                        style="R.TCheckbutton",
                    )

                    Label(spg, image=lgp_bg2, borderwidth=0).place(x=0, y=345)
                    global up_btn
                    up_btn = Button(
                        spg,
                        text="Sign Up",
                        command=signup,
                        font=("", 14),
                        width=16,
                        bg="#28282E",
                        fg="white",
                        borderwidth=0,
                        activebackground="#28282E",
                    )

                    upass_lbl.grid(row=8, column=1, padx=10, pady=10)
                    upass_ent.grid(row=8, column=2, padx=10, pady=10)
                    urepass_lbl.grid(row=9, column=1, padx=10, pady=10)
                    urepass_ent.grid(row=9, column=2, padx=10, pady=10)
                    showpass_cb.grid(row=10, column=2, padx=10, sticky=E)
                    up_btn.grid(
                        row=11, column=1, columnspan=2, padx=10, pady=10, ipadx=100
                    )

    global f_name_ent
    f_name_lbl = Label(spg, text="First Name:", font=("", 14), bg="#1e1e1e", fg="white")
    f_name_ent = Entry(spg, font=("", 14), bg="#28282E", fg="white", borderwidth=0)
    global l_name_ent
    l_name_lbl = Label(spg, text="Last Name:", font=("", 14), bg="#1e1e1e", fg="white")
    l_name_ent = Entry(spg, font=("", 14), bg="#28282E", fg="white", borderwidth=0)
    global u_name_ent
    u_name_lbl = Label(
        spg, text="Create Username:", font=("", 14), bg="#1e1e1e", fg="white"
    )
    u_name_ent = Entry(spg, font=("", 14), bg="#28282E", fg="white", borderwidth=0)
    u_name_ent.bind("<Return>", unamec)

    bk_btn = Button(
        spg,
        image=bk_arrow,
        command=sbk_rootw,
        activebackground="#1e1e1e",
        borderwidth=0,
        bg="#1e1e1e",
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

    root = Tk()
    root.config(bg="#1e1e1e")
    root.title("Password Manager")
    root.iconbitmap("images\\1.ico")
    root.geometry("300x300")
    root.resizable(0, 0)
    backg = ImageTk.PhotoImage(file="images//7.png")
    Label(root, image=backg, borderwidth=0).place(x=0.5, y=0)

    signin_btn = Button(
        root,
        text="Sign In",
        command=login_page,
        bg="#28282E",
        fg="white",
        width=8,
        font=("", 14),
        borderwidth=0,
        activebackground="#28282E",
    )
    signup_btn = Button(
        root,
        text="Sign Up",
        command=signup_page,
        bg="#28282E",
        fg="white",
        width=8,
        font=("", 14),
        borderwidth=0,
        activebackground="#28282E",
    )
    exit_btn = Button(
        root,
        text="Exit",
        command=root.destroy,
        bg="#28282E",
        fg="white",
        width=8,
        font=("", 14),
        borderwidth=0,
        activebackground="#28282E",
    )

    signin_btn.place(
        relx=0.5,
        rely=0.35,
        anchor=CENTER,
    )
    signup_btn.place(relx=0.5, rely=0.5, anchor=CENTER)
    exit_btn.place(relx=0.5, rely=0.65, anchor=CENTER)

    root.mainloop()


########################## TKINTER MAIN ###############################

check = open("cache.txt", "r", newline="\n")
ls = check.readlines()
check.close()

try:
    check_n = ls[-1]
except IndexError:
    check_n = ""
if check_n == "":
    rootw()
else:
    ui(check_n)