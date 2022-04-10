from database import *          #####IMPORTING OUR COUSTOM MODULES
from mypfuncs import *          
#ProjectbyVarunAdhityaGB
########################## CHECKING AND CREATING DATABASE #############################
mycur.execute('SHOW SCHEMAS;')
db_ls = []
#ProjectbyVarunAdhityaGB
for i in mycur:
    db_ls.extend(i)
#ProjectbyVarunAdhityaGB    
if 'MYP' in db_ls:
    mycur.execute("USE MYP;")
elif 'myp' in db_ls:
    mycur.execute("USE MYP;")
else:
    createDB()
    mycur.execute("USE MYP;")
#ProjectbyVarunAdhityaGB
########################## CHECKING AND CREATING TABLES ###############################
mycur.execute('SHOW TABLES;')
tb_ls = []
#ProjectbyVarunAdhityaGB 
for i in mycur:
    tb_ls.extend(i)
if tb_ls == []:
    createTbls()
else:
    pass
#ProjectbyVarunAdhityaGB
login_page()