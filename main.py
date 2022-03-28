import random
from string import ascii_letters, ascii_uppercase, digits, ascii_lowercase
#characters
lcase, ucase, num, alpha, pun = list(ascii_lowercase), list(ascii_uppercase),\
     list(digits), list(ascii_letters), ['!','@','#','$','%','^','&','*','-','_','/']

#defining encryption variables
lcase_crypt = ['M','L','W','U','Z','C','H','A','N','J','O','P','I','S','T','D','G','K','X','E','B','Y','R','Q','V','F']
ucase_crypt = ['m','w','f','l','s','n','o','i','d','a','g','e','u','h','p','r','y','k','q','c','x','b','v','z','j','t']
num_crypt = ['net', 'enin', 'thgie', 'neves', 'xis', 'evif', 'ruof', 'eerht', 'owt', 'eno']
#done

def shuffle(strg):
    ls = list(strg)
    random.shuffle(ls)
    
def password(n : int):
    char = [lcase, ucase, num, alpha, pun]

    #generating the password
    passwd = random.choice(pun) +  random.choice(lcase) +  random.choice(ucase) + random.choice(alpha) +  random.choice(num) 
    for i in range(n-6):
        passwd += random.choice(random.choice(char))

    #Seperating the password AND Checking
    passwd_l = list(passwd)
    
    if pun not in passwd_l:
        passwd_l.append(random.choice(pun))
    elif ucase not in passwd_l:
        passwd_l.append(random.choice(ucase))
    elif num not in passwd_l:
        passwd_l.append(random.choice(num))
    
    #Joining the password
    passwd = ''.join(passwd_l)

    #shuffling the password    
    shuffle(passwd)
    
    return passwd

def encrypt(strg : str):
    str_ls = list(strg)
    for i in str_ls:
        pass
    
        
def decrypt(strg : str):
    pass
