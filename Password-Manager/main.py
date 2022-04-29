from database import *          #####IMPORTING OUR COUSTOM MODULES
from mypfuncs import *     
from tkinter import *   
from PIL import ImageTk, Image
from tkinter import messagebox  
import tkinter.ttk as ttk
from os import system
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
##############################################################################
open('cache.txt', 'a')
shp_count = 0

########################## FUNCTOINS ###############################
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
    ui(user)


def ui(uid):
    def signout():
        psl.destroy()
        open('cache.txt', 'w')
        rootw()
    
    def showpass():
        global iclick
        iclick += 1

        if iclick%2 == 0:
            showpass_btn.configure(image=close)
            uidls1 = []
            for i in uiddata:
                uidls1.extend(i)

            uls1 = []

            for uidn in uidls:
                mycur.execute("SELECT website, loginName, loginPass, passId FROM myp_data WHERE passId="+str(uidn))
                for data in (mycur.fetchall()):
                    uls1.append(data)
                for i in range(len(uls)):
                    p2 = decrypt(str(uls[i][2]))
                    text1 = Entry(master_frm, font=('',12), fg='black', show='•')
                    text1.grid(row=i+1, column=6, padx=120, pady=10)
                    text1.insert(0,(p2))
                    text1.configure(state='readonly')    
        else:
            showpass_btn.configure(image=open_e)

            uidls1 = []
            for i in uiddata:
                uidls1.extend(i)

            uls1 = []

            for uidn in uidls:
                mycur.execute("SELECT website, loginName, loginPass, passId FROM myp_data WHERE passId="+str(uidn))
                for data in (mycur.fetchall()):
                    uls1.append(data)
                for i in range(len(uls)):
                    p1 = decrypt(str(uls[i][2]))
                    text2 = Entry(master_frm, font=('',12), fg='black')
                    text2.grid(row=i+1, column=6, padx=120, pady=10)
                    text2.insert(0,(p1))
                    text2.configure(state='readonly')
                    
                      
                
    global iclick
    global psl
    global pass_btn
    psl = Tk()
    psl.title("Passwords")
    psl.config(bg='#26242f')
    psl.state('zoomed')
    psl.resizable(0,1)
    psl.iconbitmap(r"images/1.ico")

    serch_img = ImageTk.PhotoImage(Image.open("images/2.png"))
    close = ImageTk.PhotoImage(Image.open("images/6.png"))
    open_e = ImageTk.PhotoImage(Image.open("images/7.png"))
    

    maincanva = Canvas(psl, width = 1920, height=1)
    maincanva.place(relx= 0, rely= 0.25)
    
    iclick = 0

    ########## SEARCH BOX ###############################
    search_ent = Entry(psl, font=('',15, 'bold'), bg='#26242f', fg='white', borderwidth=2, width=30)
    search_ent.place(relx=0.375, rely=0.03)
    
    search_btn = Button(psl, image=serch_img, bg='#26242f', activebackground='#26242f',
        borderwidth=2)
    search_btn.place(relx=0.65, rely=0.032)

    ########## WEBSITE HEAD ###############################    
    site_frm = Frame(psl, width = 20, background='#26242f')
    site_frm.place(relx=0.05, rely=0.15)

    site_head = Label(site_frm, text='Website', bg='#26242f', fg='white', borderwidth=0, font=('',12,'bold underline'))
    site_head.grid(row=1, column=1, padx=10, pady=20)

    ########## USER NAME HEAD ###############################
    uname_frm = Frame(psl, width = 20, background='#26242f')
    uname_frm.place(relx=0.25, rely=0.15 )

    uname_head = Label(uname_frm, text='Username', bg='#26242f', fg='white', borderwidth=0, font=('',12,'bold underline'))
    uname_head.grid(row=1, column=1, padx=10, pady=20)

    ########## PASSWORD HEAD ###############################
    pass_frm = Frame(psl, width = 20, background='#26242f')
    pass_frm.place(relx=0.5, rely=0.15 )

    pass_head = Label(pass_frm, text='Password', bg='#26242f', fg='white', borderwidth=0, font=('',12,'bold underline'))
    pass_head.grid(row=1, column=1, padx=10, pady=20)

    ########## MAIN FRAME ###############################
    master_frm = Frame(psl, background='#26242f')
    master_frm.place(relx=0.05, rely=0.35)
    #####################################################
    mycur.execute("SELECT passId FROM myp_data WHERE userId="+str(uid))
    uiddata = mycur.fetchall()
    uidls = []
    for i in uiddata:
        uidls.extend(i)

    uls = []
    
    for uidn in uidls:
        mycur.execute("SELECT website, loginName, loginPass, passId FROM myp_data WHERE passId="+str(uidn))
        for data in (mycur.fetchall()):
            uls.append(data)

        for i in range(len(uls)):
            p = decrypt(str(uls[i][2]))
            p_len=len(str(uls[i][2]))

            site_lbl = Label(master_frm, text=uls[i][0], font=('',12), fg='white', bg='#26242f')
            indent_lbl = Label(master_frm, text='                        ', font=('',12), fg='white', bg='#26242f')
            uname_l = Label(master_frm, text=uls[i][1], font=('',12), fg='white', bg='#26242f')
            indent_lbl1= Label(master_frm, text='                        ', font=('',12), fg='white', bg='#26242f')
            pass_ent = Entry(master_frm, font=('',12), fg='black', borderwidth=1, show='•')
            

            site_lbl.grid(row=i+1, column=2, padx=10, pady=10, sticky=W)
            indent_lbl.grid(row=i+1, column=3, padx=10, pady=10, sticky=W)
            uname_l.grid(row=i+1, column=4, padx=30, pady=10, sticky=W)
            indent_lbl1.grid(row=i+1, column=5, padx=10, pady=10, sticky=W)
            pass_ent.grid(row=i+1, column=6, padx=120, pady=10)
            

            pass_ent.insert(0,(p))
            pass_ent.configure(state='readonly')

            can1 = Canvas(psl, height=1080, width=1)
            can1.place(relx=0.2, rely=0.15)    

            can2 = Canvas(psl, height=1080, width=1)
            can2.place(relx=0.45, rely=0.15)

    j = (len(uls) + 1)
    adddata_btn = Button(master_frm, text='Add entry...', font=('',11, 'bold'), fg='white', bg='#26242f', activebackground='#26242f') 
    deletedata_btn = Button(master_frm, text="Delete data!!", font=('',12), fg='white', bg='grey', relief='raised',
                activebackground='grey', borderwidth=2)    
    showpass_btn = Button(master_frm, image=close, borderwidth=0, bg='#26242f', activebackground='#26242f',command=showpass)
    
    adddata_btn.grid(row=j, column=2, padx=10, pady=10)
    deletedata_btn.grid(row=j+1, column=7, padx=0, pady=10)
    

    if len(uls) == 0:
        showpass_btn.configure(state='disabled')
        #showpass_btn.grid(row=1, column=7, padx=10, pady=10)
    else:
        showpass_btn.grid(row=1, column=7, rowspan=5, padx=10, pady=10)

    status_frm = Frame()   
    out_btn = Button(psl, text='Sign Out', bg='#26242f', fg='white', borderwidth=0, font=('',12), command=signout)
    out_btn.place(relx=0.95, rely=0.95)

    

    psl.mainloop()

def login_page():
    root.destroy()
    global lpg
    global user
    lpg = Tk()
    lpg.title("Login")
    lpg.config(bg="#26242f")
    lpg.geometry("400x300")
    lpg.resizable(0,0)
    lpg.iconbitmap(r"images/1.ico")

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

    def login(*event):
        global lpg
        mydb = sqlc.connect(host='localhost', user='root', passwd='root',)
        mycur = mydb.cursor()

        mycur.execute("USE myp;")
        
        uname_srch = usern_dm.get()
        if uname_srch == 'Select a Username':
            messagebox.showerror("User Not Selected", "Select an user from the dropdown menu.")
        else:
            mycur.execute(f"SELECT userId FROM myp_users WHERE userName = '{uname_srch}';")   
            user_ls = []
            for i in mycur:
                    user_ls.extend(i)

            global user
            user = user_ls[0]
            with open("cache.txt",'a') as fileerite:
                fileerite.write(str(user))
                fileerite.write('\n')

            mycur.execute(f"SELECT masterPass FROM myp_users WHERE userName = '{uname_srch}';")
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
                    msgbox = messagebox.showwarning("ERROR","WRONG PASSWORD!!")
                    if msgbox == 'ok':
                        break
            pass_ls = []

    bk_arrow = ImageTk.PhotoImage(Image.open("images/10.png"))
    ################# STYLES ##########################################
    cb_style = ttk.Style()
    cb_style.configure('R.TCheckbutton', foreground='white', background='#26242f')
    
    
    ###WIDGETS
    usern_lbl = Label(lpg, text="Username:", font=('', 14), bg='#26242f', fg="white")
    pass_lbl = Label(lpg, text="Password:", font=('', 14), bg='#26242f', fg="white")
    pass_ent = Entry(lpg, textvariable=passkey, show="*", font=('', 14), bg='#26242f', fg="white")
    pass_ent.bind("<Return>",login)
    in_btn = Button(lpg, text="Sign In",command=login, font=('', 14), width=20, bg='#26242f', fg="white")
    showpass_cb = ttk.Checkbutton(lpg, text="Show Password", variable=cbvar, onvalue=1, offvalue=0, command=shbtn, style='R.TCheckbutton' )
    bk_btn = Button(lpg, image=bk_arrow, command=lbk_rootw, activebackground='#26242f', borderwidth=0, bg='#26242f')

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
    spg.geometry("400x600")
    spg.resizable(0,0)
    spg.iconbitmap(r"images/1.ico")
    
    passkey = StringVar()
    repasskey = StringVar()
    cbvar = IntVar(value=0)
    bk_arrow = ImageTk.PhotoImage(Image.open("images/10.png"))

    def signup(*event):

        def upass_ui():
            insintousers(str(f_name_ent.get()), str(l_name_ent.get()), str(u_name_ent.get()), str(email_ent.get()), str(upass_ent.get()) )
            messagebox.showinfo("Successfully Signed Up", "You have successfull created your account")
            okres = messagebox.showinfo("Reload Required", "Click ok to reload.")
            if okres == 'ok':
                spg.destroy()
                system("python password-manager/main.py")
                
                
                

            f_name_ent.delete(0, END)
            l_name_ent.delete(0, END)
            u_name_ent.delete(0, END)
            upass_ent.delete(0, END)
            urepass_ent.delete(0, END)
            urepass_lbl.destroy()
            upass_lbl.destroy()
            upass_ent.destroy()
            urepass_ent.destroy()
            otp_ent.destroy()
            otp_lbl.destroy()
            email_ent.destroy()
            up_btn.destroy()
            showpass_cb.destroy()
            email_lbl.destroy()
            

        if urepass_ent.get() != upass_ent.get():
            messagebox.showerror("Password Mismatch","PLease make sure that your passwords match.")
        elif len(upass_ent.get()) < 8:
            messagebox.showerror("Password Not Satisfying Requirements","The password should be atleast a minimum of 8 characters.")
        
        else:
            upass_ui()

    def unamec(*event):
        def emailc(*event):
            def otpc(*event):
                global urepass_ent
                global upass_ent

                def cbshow():
                    if (cbvar.get())== 1:
                        upass_ent.config(show='')
                        urepass_ent.config(show='')
                    else:
                        upass_ent.config(show='*')
                        urepass_ent.config(show='*')

                js = eval(otp_ent.get())
                if js == otp:

                    cb_style = ttk.Style()
                    cb_style.configure('R.TCheckbutton', foreground='white', background='#26242f')

                    global upass_lbl
                    upass_lbl = Label(spg, text='Master Password:', font=('',14), bg='#26242f', fg='white')
                    global upass_ent
                    upass_ent = Entry(spg, textvariable=passkey, show="*", font=('', 14), bg='#26242f', fg="white")
                    global urepass_lbl
                    urepass_lbl = Label(spg, text='Re-Enter Password:', font=('',14), bg='#26242f', fg='white')
                    global urepass_ent
                    urepass_ent = Entry(spg, textvariable=repasskey, show="*", font=('', 14), bg='#26242f', fg="white")
                    urepass_ent.bind("<Return>", signup)
                    global showpass_cb
                    showpass_cb = ttk.Checkbutton(spg, text="Show Password", variable=cbvar, onvalue=1, offvalue=0, 
                        command=cbshow, style='R.TCheckbutton' )
                    global up_btn
                    up_btn = Button(spg, text="Sign Up",command=signup, font=('', 14), width=20, bg='#568943', fg="white")

                    upass_lbl.grid(row=8, column=1, padx=10, pady=10)
                    upass_ent.grid(row=8, column=2, padx=10, pady=10)
                    urepass_lbl.grid(row=9, column=1, padx=10, pady=10)
                    urepass_ent.grid(row=9, column=2, padx=10, pady=10)
                    showpass_cb.grid(row=10, column=2, padx=10, sticky=E)
                    up_btn.grid(row=11, column=1, columnspan=2, padx=10, pady=10, ipadx=100)
                else:
                    messagebox.showerror("Wrong OTP", "The entered otp is wrong.\nPlease check again.")

            res = emailvalidation(email_ent.get())
            if res == False:
                messagebox.showerror("Invalid E-Mail", "This is not an valid e-mail address.")
            else:
                ress = emailcheck(email_ent.get())
                if ress == False:
                    messagebox.showinfo("Duplicate Found", "This is email address is assosiated with another user.")
                else:
                    otp = otpmail(email_ent.get())
                    print(otp)
                    global otp_lbl
                    otp_lbl = Label(spg, text='OTP:      ', font=('',14), bg='#26242f', fg='white')
                    global otp_ent
                    otp_ent = Entry(spg, font=('', 14), bg='#26242f', fg="white")
                    otp_ent.bind("<Return>", otpc)

                    otp_lbl.grid(row=7, column=1, padx=10, pady=10)
                    otp_ent.grid(row=7, column=2, padx=10, pady=10)

        res = unamecheck(u_name_ent.get())
        if res == False:
            messagebox.showerror("Duplicate found", "This username already exits!")
        else:
            if (f_name_ent.get() == ''):
                messagebox.showerror("Fill Everything", "Please enter a First name.")
            elif (u_name_ent.get() == ''):
                messagebox.showerror("Fill Everything", "Please enter a username.")
            else:
                
                global email_lbl
                email_lbl = Label(spg, text='E-Mail:   ', font=('',14), bg='#26242f', fg='white')
                global email_ent
                email_ent = Entry(spg, font=('', 14), bg='#26242f', fg="white")
                email_ent.bind("<Return>", emailc)

                email_lbl.grid(row=6, column=1, padx=10, pady=10)
                email_ent.grid(row=6, column=2, padx=10, pady=10)

    global f_name_ent
    f_name_lbl = Label(spg, text="First Name:", font=('', 14), bg='#26242f', fg="white")
    f_name_ent = Entry(spg, font=('', 14), bg='#26242f', fg="white")
    global l_name_ent
    l_name_lbl = Label(spg, text="Last Name:", font=('', 14), bg='#26242f', fg="white")
    l_name_ent = Entry(spg, font=('', 14), bg='#26242f', fg="white")
    global u_name_ent
    u_name_lbl = Label(spg, text='Create Username:', font=('',14), bg='#26242f', fg='white')
    u_name_ent = Entry(spg, font=('', 14), bg='#26242f', fg="white")
    u_name_ent.bind("<Return>", unamec)
    
    bk_btn = Button(spg, image=bk_arrow, command=sbk_rootw, activebackground='#26242f', borderwidth=0, bg='#26242f')

    f_name_lbl.grid(row=3, column=1, padx=10, pady=10)
    l_name_lbl.grid(row=4, column=1, padx=10, pady=10)
    u_name_lbl.grid(row=5, column=1, padx=10, pady=10)

    f_name_ent.grid(row=3, column=2, padx=10, pady=10)
    l_name_ent.grid(row=4, column=2, padx=10, pady=10)
    u_name_ent.grid(row=5, column=2, padx=10, pady=10)
    bk_btn.grid(row=1, column=1, padx=10, pady=20)

    spg.mainloop()

########################## TKINTER MAIN ###############################

def rootw():
    global root
    
    root = Tk()
    root.config(bg="#26242f")
    root.title("Password Manager")
    root.iconbitmap(r"images/1.ico")
    root.geometry("300x300")
    root.resizable(0,0)

    signin_btn = Button(root, text = "Sign In", command=login_page, bg='#26242f', fg='white', width=10, font=('',14))
    signup_btn = Button(root, text = "Sign Up", command=signup_page, bg='#26242f', fg='white', width=10, font=('',14))
    exit_btn = Button(root, text = "Exit", command=root.destroy, bg='#26242f', fg='white',width=10, font=('',14))

    signin_btn.place(relx=0.5, rely=0.35, anchor=CENTER)
    signup_btn.place(relx=0.5, rely=0.5, anchor=CENTER)
    exit_btn.place(relx=0.5, rely=0.65, anchor=CENTER)

    root.mainloop()

check = open('cache.txt','r', newline='\n')
ls = check.readlines()
check.close()

try:
    check_n = ls[-1]
except IndexError:
    check_n = ''
if check_n == '':
    rootw()
else:
    ui(check_n)