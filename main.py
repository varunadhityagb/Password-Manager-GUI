#from database import *
import os
from mypfuncs import *
from getpass import getpass
import sys

print(''' -----------MENU-----------
1. Login
2. Sign Up
3. Exit''')

opt = int(input(""))
os.system('clear')
if opt == 1:
    pass
elif opt == 2:
    w = 't'
    fName = input("Enter your first name:")
    lName = input("Enter your first name:")
    uName = input("Enter your first name:")
    eMail = input("Enter your first name:")
    while w == 't':
        masterPass = getpass("New Password: ")
        masterPass_check = getpass("Re-enter Password: ")
        if masterPass_check == masterPass:    
            #insintousers(fName, lName, uName, eMail, masterPass)
            break
        else:
            print("Your passwords don't match!")
elif opt == 3:
    sys.exit