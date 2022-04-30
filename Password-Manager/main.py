import io
from tkinter.font import BOLD
from urllib.request import urlopen

from database import *          #####IMPORTING OUR COUSTOM MODULES
from mypfuncs import *     
from tkinter import *   
from PIL import ImageTk, Image
from tkinter import messagebox  
import tkinter.ttk as ttk
from os import system
import webbrowser as wb
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

img2_url = "https://raw.githubusercontent.com/VarunAdhityaGB/Password-Manager-GUI/main/images/2.png"
img3_url = "https://raw.githubusercontent.com/VarunAdhityaGB/Password-Manager-GUI/main/images/3.png"
img4_url = "https://raw.githubusercontent.com/VarunAdhityaGB/Password-Manager-GUI/main/images/4.png"
img5_url = "https://raw.githubusercontent.com/VarunAdhityaGB/Password-Manager-GUI/main/images/5.png"
img6_url = "https://raw.githubusercontent.com/VarunAdhityaGB/Password-Manager-GUI/main/images/6.png"
img7_url = "https://raw.githubusercontent.com/VarunAdhityaGB/Password-Manager-GUI/main/images/7.png"
img8_url = "https://raw.githubusercontent.com/VarunAdhityaGB/Password-Manager-GUI/main/images/8.png"
img9_url = "https://raw.githubusercontent.com/VarunAdhityaGB/Password-Manager-GUI/main/images/9.png"
img10_url = "https://raw.githubusercontent.com/VarunAdhityaGB/Password-Manager-GUI/main/images/10.png"

p2, p3, p4, p5, p6, p7, p8, p9, p10 = urlopen(img2_url), urlopen(img3_url), urlopen(img4_url), urlopen(img5_url), urlopen(img6_url), urlopen(img7_url), urlopen(img8_url), urlopen(img9_url), urlopen(img10_url)

img2, img3, img4, img5, img6, img7, img8, img9, img10 = io.BytesIO(p2.read()), io.BytesIO(p3.read()), io.BytesIO(p4.read()), io.BytesIO(p5.read()), io.BytesIO(p6.read()), io.BytesIO(p7.read()), io.BytesIO(p8.read()), io.BytesIO(p9.read()), io.BytesIO(p10.read())

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
                    text1 = Entry(second_frame, font=('',12), fg='black', show='•')
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
                    text2 = Entry(second_frame, font=('',12), fg='black')
                    text2.grid(row=i+1, column=6, padx=120, pady=10)
                    text2.insert(0,(p1))
                    text2.configure(state='readonly')
                    
    def deletedata():
        ddk = Tk()
        ddk.title("Delete Data")
        ddk.mainloop()

                
    global iclick
    global psl
    global pass_btn
    psl = Tk()
    psl.title("Passwords")
    psl.config(bg='#26242f')
    psl.state('zoomed')
    psl.iconbitmap("1.ico")

    serch_img = ImageTk.PhotoImage(Image.open(img2))
    close = ImageTk.PhotoImage(Image.open(img6))
    open_e = ImageTk.PhotoImage(Image.open(img7))
    

    main_frame = Frame(psl, width=1340, height=650, background="#26242f", borderwidth=0)
    main_frame.grid(row=1, column=0)

    main_canvas = Canvas(main_frame, borderwidth=0, background="#26242f", width=1340, height=650)
    main_canvas.pack(side=LEFT, fill=BOTH, expand=YES)
    
    scroll = Scrollbar(main_frame, orient=VERTICAL, command=main_canvas.yview, bg='#26242f',highlightthickness=0, troughcolor='#26242f')
    scroll.pack(side=RIGHT, fill=Y)

    main_canvas.configure(yscrollcommand=scroll.set)
    main_canvas.bind('<Configure>', lambda e: main_canvas.configure(scrollregion= main_canvas.bbox("all")))


    second_frame = Frame(main_canvas, borderwidth=0, background="#26242f", width=1340, height=650)
    main_canvas.create_window((0,0), window=second_frame)
    
    num_header = Label(second_frame, text="Id", font=('', 14, BOLD), bg='#26242f', fg="white")
    site_header = Label(second_frame, text='Website', font=('',14, BOLD), bg='#26242f', fg='white')
    indent_header = Label(second_frame, text='', font=('                        ',14), bg='#26242f', fg='white')
    uname_header = Label(second_frame, text='Username', font=('',14,BOLD), bg='#26242f', fg='white')
    indent_header2 = Label(second_frame, text='', font=('                        ',14), bg='#26242f', fg='white')
    pass_header = Label(second_frame, text='Password', font=('',14, BOLD), bg='#26242f', fg='white')
    
    num_header.grid(row=0, column=1, padx=20, pady=10, sticky=E)
    site_header.grid(row=0, column=2, padx=10, pady=10, sticky=W)
    indent_header.grid(row=0, column=3, padx=10, pady=10, sticky=W)
    uname_header.grid(row=0, column=4, padx=30, pady=10, sticky=W)
    indent_header2.grid(row=0, column=5, padx=10, pady=10, sticky=W)
    pass_header.grid(row=0, column=6, padx=120, pady=10)

    iclick = 0

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

            num_lbl = Label(second_frame, text=i+1, font=('', 12), fg='white', bg='#26242f', borderwidth=0)
            site_lbl = Label(second_frame, text=uls[i][0], font=('',12), fg='white', bg='#26242f', borderwidth=0)
            indent_lbl = Label(second_frame, text='                        ', font=('',12), fg='white', bg='#26242f')
            uname_l = Label(second_frame, text=uls[i][1], font=('',12), fg='white', bg='#26242f')
            indent_lbl1= Label(second_frame, text='                        ', font=('',12), fg='white', bg='#26242f')
            pass_ent = Entry(second_frame, font=('',12), fg='black', borderwidth=1, show='•')
            
            num_lbl.grid(row=i+1, column=1, padx=20, pady=10, sticky=E)
            site_lbl.grid(row=i+1, column=2, padx=10, pady=10, sticky=W)
            indent_lbl.grid(row=i+1, column=3, padx=10, pady=10, sticky=W)
            uname_l.grid(row=i+1, column=4, padx=30, pady=10, sticky=W)
            indent_lbl1.grid(row=i+1, column=5, padx=10, pady=10, sticky=W)
            pass_ent.grid(row=i+1, column=6, padx=120, pady=10)
            

            pass_ent.insert(0,(p))
            pass_ent.configure(state='readonly')

    j = (len(uls) + 1)
        
    showpass_btn = Button(second_frame, image=close, borderwidth=0, bg='#26242f', activebackground='#26242f',command=showpass)

    if len(uls) == 0:
        showpass_btn.configure(state='disabled')
    else:
        showpass_btn.grid(row=1, column=7, rowspan=5, padx=10, pady=10)

    status_frm = Frame(psl, background="#26242f", width = 1340, height=30)   
    
    out_btn = Button(status_frm, text='Sign Out', bg='#26242f', fg='white', borderwidth=0, font=('',12), command=signout)
    adddata_btn = Button(status_frm, text='Add entry...', font=('',12), fg='white', bg='#26242f',
         activebackground='#26242f', borderwidth=0) 
    deletedata_btn = Button(status_frm, text="Delete data!!", font=('',12), fg='white', bg='#26242f', borderwidth=0, command=deletedata)

    adddata_btn.grid(row=0, column=2, padx=10, pady=10)
    deletedata_btn.grid(row=0, column=7, padx=0, pady=10)
    out_btn.grid(row=0, column=10, padx=10, pady=10)

    status_frm.grid(row=2, column=0, sticky=W)



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
    lpg.iconbitmap("1.ico")

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

    bk_arrow = ImageTk.PhotoImage(Image.open(img10))
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
    spg.iconbitmap("1.ico")
    
    passkey = StringVar()
    repasskey = StringVar()
    cbvar = IntVar(value=0)
    bk_arrow = ImageTk.PhotoImage(Image.open(img10))

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
    root.iconbitmap("1.ico")
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