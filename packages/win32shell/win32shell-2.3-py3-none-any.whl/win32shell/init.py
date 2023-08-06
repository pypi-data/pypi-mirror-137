import requests , subprocess , sys , time
from bs4 import BeautifulSoup

start_time = time.time()
 
htmldata = requests.get("https://pypi.org/project/win32shell/")
soup = BeautifulSoup(htmldata.text, 'html.parser')
lv = soup.find("h1" , class_="package-header__name").text.strip()[11:]

from importlib.metadata import version
ov = version('win32shell')

if lv == ov:
    pass
else:
    update_pip = 'pip install --upgrade win32shell'
    subprocess.call(update_pip, shell=True,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)





import subprocess , sys

try:
    from cryptography.fernet import Fernet
    
except:
    update_pip = 'pip install cryptography'
    subprocess.call(update_pip, shell=True,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)





try:
    from obscure_password import obscure
    
except:
    update_pip = 'pip install obscure-password'
    subprocess.call(update_pip, shell=True,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)




try:
    from AesEverywhere import aes256
    
except:
    update_pip = 'pip install aes-everywhere'
    subprocess.call(update_pip, shell=True,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)




from functools import reduce
from AesEverywhere import aes256 as aes256bit
from obscure_password import obscure as vigenere_cipher
from obscure_password import unobscure as bytes
from cryptography.fernet import Fernet as salt
base85 = salt.generate_key()
caesar_cipher = salt(base85)



GCM = 'utf-8'
CBC = 'utf-8'
EAX = 'utf-8'
SIV = 'utf-8'
OCB = 'utf-8'




