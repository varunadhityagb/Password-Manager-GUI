from database import *
from mypfuncs import *

########################## CHECKING AND CREATING DATABASE #############################
mycur.execute('SHOW SCHEMAS;')
db_ls = []
for i in mycur:
    db_ls.extend(i)
    
if 'MYP' in db_ls:
    mycur.execute("USE MYP;")
elif 'myp' in db_ls:
    mycur.execute("USE MYP;")
else:
    createDB()
    mycur.execute("USE MYP;")

########################## CHECKING AND CREATING TABLES ###############################
mycur.execute('SHOW TABLES;')
tb_ls = []

for i in mycur:
    tb_ls.extend(i)
if tb_ls == []:
    createTbls()
else:
    pass

login_page()
post_login()