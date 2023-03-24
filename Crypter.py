import base64 as b64
import argparse
from cryptography.fernet import Fernet
import subprocess
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import string
import random
import sys
import shutil


def encrypter(text):
    salt = os.urandom(16)
    paswd = (''.join(random.choices(string.ascii_lowercase,k=6)))
    password = bytes(paswd,'utf-8')
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )

    key = b64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)
    s = f.encrypt(text)
    #print(key)
    return (s,salt,paswd)

def swapc(text):
    return text.swapcase()

parser = argparse.ArgumentParser(
    description='something ahahha')
parser.add_argument('input', type=str,
                    help='Input filename or full path')
parser.add_argument('--out', default='hacked.bin', type=str,
                    help='Output filename or full path')

args = parser.parse_args()

file = open(args.input,'rb')
f = file.read()

#obfuscation part
y,key,passw = encrypter(f)
#print(key)
#print(type(key))


'''with open(args.out, 'wb') as output:
    output.write(y)
with open('key.bin','wb') as k:
    k.write(key)
k.close()
    #k.write()
with open('pass.bin','wb') as p:
    p.write(passw)
p.close()'''

#python code
code1 = '''import base64 as b64
from cryptography.fernet import Fernet
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import sys
import shutil
'''

code2 = '''
#k = open('key.bin','rb')
#salt = k.read()
#k.close()
#os.remove('key.bin')
#p = open('pass.bin','rb')
#password = p.read()
#p.close()
#os.remove('pass.bin')
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=390000,
)

key = b64.urlsafe_b64encode(kdf.derive(password))
#print(key)
#f = open('hacked.bin','rb')
#s = f.read()
#f.close()
g = open('original.exe','wb')
h = Fernet(key)
s = h.decrypt(s)
g.write(s)
g.close()

#os.remove('c4.bin')
#os.remove('hacked.bin')
os.startfile("original.exe")
#os.remove('sys.argv[0]')
'''
gum = open('fenny.txt','w')
gum.write(str(y))
gum.close()
rev = open('crypted.py','w')
rev.write(code1)
rev.write('\nsalt = '+str(key)+'\n')
rev.write("password = bytes('"+passw+"','utf-8')\n")
rev.write('s = '+str(y)+'\n')
rev.write(code2)
rev.close()

command = ["pyinstaller","--onefile","crypted.py"]
subprocess.run(command)

#exec(open('original.py').read())
os.remove('crypted.py')
os.system('copy dist\crypted.exe')
#os.system('rmdir /Q dist')
#os.system('rmdir /Q build')
shutil.rmtree('dist')
shutil.rmtree('build')
os.remove('crypted.spec')
#os.startfile("original.exe")





