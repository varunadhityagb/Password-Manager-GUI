from database import *          #####IMPORTING OUR COUSTOM MODULES
from mypfuncs import *     
from tkinter import *   
from PIL import ImageTk, Image
from tkinter import messagebox  
import tkinter.ttk as ttk
########################## CHECKING AND CREATING DATABASE #############################
mycur.execute('SHOW SCHEMAS;')
db_ls = []

for i in mycur:
    db_ls.extend(i)
#ProjectbyVarunAdhityaGB    
if 'myp' in db_ls:
    mycur.execute("USE myp;")
elif 'myp' in db_ls:
    mycur.execute("USE myp;")
else:
    createDB()
    mycur.execute("USE myp;")

########################## CHECKING AND CREATING TABLES ###############################
mycur.execute('SHOW TABLES;')
tb_ls = []
 
for i in mycur:
    tb_ls.extend(i)
if tb_ls == []:
    createTbls()
else:
    pass

########################## FUNCTOINS ###############################


def login_page():
    root.destroy()
    global lpg
    lpg = Tk()
    lpg.config(bg="#26242f")
    lpg.title("Login")
    lpg.geometry("400x300")
    lpg.resizable(0,0)
    lpg.iconbitmap(r"images/icon.ico")

    clicked = StringVar()
    passkey = StringVar()
    cbvar = IntVar(value=0)
    mycur.execute("SELECT userName FROM myp_users") 
    data_ls = mycur.fetchall()
    ls = ['Select a Username']

    for i in data_ls:
        ls.extend(i)
        
    def shbtn():
        if (cbvar.get())== 1:
            pass_ent.config(show='')
        else:
            pass_ent.config(show='*')

    def pass_ui():
        lpg.destroy()
        global psl
        psl = Tk()
        psl.mainloop()


    def login():
        global lpg
        mydb = sqlc.connect(host='localhost', user='root', passwd='root',)
        mycur = mydb.cursor()

        global user
        mycur.execute("USE myp;")
        
        uname_srch = usern_dm.get()
        print(uname_srch)
        if uname_srch == 'Select a Username':
            messagebox.showinfo("Info","No users found!!")
        else:
            mycur.execute(f"SELECT userId FROM myp_users WHERE userName = '{uname_srch}';")   
            user_ls = []
            for i in mycur:
                    user_ls.extend(i)

            try:
                user = user_ls[0]
            except IndexError:
                war = Label(root, text="Select a user", font=("",10)).grid(row=2, column=2)
            mycur.execute(f"SELECT masterPass FROM myp_users WHERE userName = '{uname_srch}';")
            pass_ls = []
            for i in mycur:
                pass_ls.extend(i)

            ch = False
            while ch == False:
                masterPass_check_hash = hashcrypt(passkey.get())
                if masterPass_check_hash == pass_ls[0]:
                    ch == True
                    pass_ui()
                else:
                    msgbox = messagebox.showwarning("ERROR","WRONG PASSWORD!!")
                    if msgbox == 'ok':
                        break
            pass_ls = []

    def bk_rootw():
        global lpg
        lpg.destroy()
        rootw()

    bk_arrow = ImageTk.PhotoImage(Image.open("images/backarrow.png"))
    ################# STYLES ##########################################
    cb_style = ttk.Style()
    cb_style.configure('R.TCheckbutton', foreground='white', background='#26242f')
    
    
    ###WIDGETS
    usern_lbl = Label(lpg, text="Username:", font=('', 14), bg='#26242f', fg="white")
    pass_lbl = Label(lpg, text="Password:", font=('', 14), bg='#26242f', fg="white")
    pass_ent = Entry(lpg, textvariable=passkey, show="*", font=('', 14), bg='#26242f', fg="white")
    in_btn = Button(lpg, text="Sign In",command=login, font=('', 14), width=20, bg='#26242f', fg="white")
    showpass_cb = ttk.Checkbutton(lpg, text="Show Password", variable=cbvar, onvalue=1, offvalue=0, command=shbtn, style='R.TCheckbutton' )
    bk_btn = Button(lpg, image=bk_arrow, command=bk_rootw, activebackground='#26242f', borderwidth=0, bg='#26242f')

    #SHOWING THEM
    usern_lbl.place(relx=0.2, rely=0.3, anchor=CENTER)
    pass_lbl.place(relx=0.2, rely=0.45, anchor=CENTER)
    pass_ent.place(relx=0.7, rely=0.45, anchor=CENTER)
    showpass_cb.place(relx=0.85, rely=0.55, anchor=CENTER)
    in_btn.place(relx=0.5, rely=0.7, anchor=CENTER)
    bk_btn.place(relx=0.1, rely=0.1, anchor=CENTER)

    if ls == []:
        response = messagebox.showinfo("Info","No users found!!")
        Label(lpg, text=response).pack()
    else:
        usern_dm = ttk.Combobox(lpg, value=ls, font=('',14))
        usern_dm.current(0)
        usern_dm.place(relx=0.7, rely=0.3, anchor=CENTER)

    lpg.mainloop()
    
def signup_page():
    root.destroy()
    global spg
    spg = Tk()
    spg.title("Sign Up")
    spg.config(bg='#26242f')
    spg.geometry("600x400")
    spg.resizable(0,0)
    spg.iconbitmap(r"images/icon.ico")
    spg.mainloop()

########################## TKINTER MAIN ###############################

def rootw():
    global root
    root = Tk()
    root.config(bg="#26242f")
    root.title("Password Manager")
    root.iconbitmap(r"images/icon.ico")
    root.geometry("300x300")
    root.resizable(0,0)

    signin_btn = Button(root, text = "Sign In", command=login_page, bg='#26242f', fg='white', width=10, font=('',14))
    signup_btn = Button(root, text = "Sign Up", command=signup_page, bg='#26242f', fg='white', width=10, font=('',14))
    exit_btn = Button(root, text = "Exit", command=root.destroy, bg='#26242f', fg='white',width=10, font=('',14))

    signin_btn.place(relx=0.5, rely=0.35, anchor=CENTER)
    signup_btn.place(relx=0.5, rely=0.5, anchor=CENTER)
    exit_btn.place(relx=0.5, rely=0.65, anchor=CENTER)

    root.mainloop()

rootw()