import random
from string import ascii_letters, ascii_uppercase, digits, ascii_lowercase

def shuffle(strg):
    ls = list(strg)
    random.shuffle(ls)
    
def password(n : int):
    #list of characters
    lcase, ucase, num, alpha, pun = list(ascii_lowercase), list(ascii_uppercase), list(digits), list(ascii_letters), ['!','@','#'] 
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

def encrypt(strg):
    str_ls = list(strg)
    for i in str_ls:
        pass
    
        
def decrypt(strg : str):
    pass

