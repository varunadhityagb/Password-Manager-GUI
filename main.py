from database import *
from mypfuncs import *


########################## CHECKING AND CREATING DATABASE #############################
mycur.execute('SHOW SCHEMAS;')
db_ls = []
for i in mycur:
    db_ls.append(i)

if ('MYP',) not in db_ls:
    createDB()
    mycur.execute("USE MYP;")
else:
    mycur.execute("USE MYP;")

########################## CHECKING AND CREATING TABLES ###############################
mycur.execute('SHOW TABLES;')
tb_ls = []
for i in mycur:
    tb_ls.append()
if tb_ls == []:
    createTbls()
else:
    pass

login_page()
