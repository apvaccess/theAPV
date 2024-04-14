#!/usr/bin/env python3
# F20PA Dissertation Ransomware Test
# **NOTE** THIS IS ONLY FOR DOCUMENTATION AND RESEARCH PURPOSES. THIS CODE SHALL NOT BE USED FOR PERSONAL USE OR MALICIOUS INTENTIONS INORDER TO MEET ETHICAL REQUIREMENTS. PLEASE DO NOT USE TRY THIS
# Owner: apv2@hw.ac.uk Aswin Valsalan 


import os
import hashlib
import smtplib
import logging
import tkinter as tk
import datetime
import csv
import shutil
from tkinter import messagebox
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Set up logging
logging.basicConfig(filename='incident_response.log', level=logging.INFO)

def send_email(subject, message, to_email):
    from_email = "apv2@hw.ac.uk"
    password = "IdliNQU0"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('pro.turbo-smtp.com', 587)
    server.starttls()
    server.login(from_email, password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()

def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def quarantine_file(file_path):
    quarantine_dir = 'D:/Quarantine/'
    shutil.move(file_path, quarantine_dir)

def detect_incident():
    # Define a set of known safe MD5 hashes
    safe_hashes = set()

    # Define a set of suspicious file extensions
    suspicious_extensions = {'.exe', '.dll', '.scr', '.bat', '.py', '.java', '.html', '.js'}

    # Define a list of directories to scan
    directories_to_scan = ['D:\\', 'E:\\', 'F:\\', 'G:\\', 'H:\\']  # For Windows
    if os.name == 'posix':  # For Linux
        directories_to_scan = ['/']

    for directory in directories_to_scan:
        for foldername, subfolders, filenames in os.walk(directory):
            for filename in filenames:
                if os.path.splitext(filename)[1] in suspicious_extensions:
                    file_path = os.path.join(foldername, filename)
                    file_hash = calculate_md5(file_path)
                    file_size = os.path.getsize(file_path)
                    if file_hash not in safe_hashes:
                        logging.info(f'Suspicious file detected: {file_path}')
                        return file_path, file_size, file_hash

    return None, None, None

def write_report(file_path, action_taken, severity, file_size, file_hash):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('incident_report.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, file_path, action_taken, severity, file_size, file_hash])

def main(to_email):
    suspicious_file, file_size, file_hash = detect_incident()
    if suspicious_file:
        root = tk.Tk()
        root.withdraw()
        MsgBox = tk.messagebox.askquestion ('Delete File','Suspicious file detected: ' + suspicious_file + '. Do you want to delete this file?',icon = 'warning')
        if MsgBox == 'yes':
            os.remove(suspicious_file)
            logging.info("Suspicious file deleted.")
            write_report(suspicious_file, 'Deleted', 'High', file_size, file_hash)
        else:
            MsgBox = tk.messagebox.askquestion ('Quarantine File','Do you want to quarantine this file?',icon = 'warning')
            if MsgBox == 'yes':
                quarantine_file(suspicious_file)
                logging.info("Suspicious file quarantined.")
                write_report(suspicious_file, 'Quarantined', 'Medium', file_size, file_hash)
            else:
                logging.info("User chose not to delete or quarantine the suspicious file.")
                write_report(suspicious_file, 'No action taken', 'Low', file_size, file_hash)
        send_email("Incident Detected", "A suspicious file was detected on your system.", to_email)
        root.destroy()
    else:
        logging.info("No incident detected.")

if __name__ == "__main__":
    to_email = "aswinvalsalan2016@gmail.com"  # Replace with the recipient's email address
    main(to_email)
