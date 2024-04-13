#!/usr/bin/env python3
# F20PA Dissertation Ransomware Test
# **NOTE** THIS IS ONLY FOR DOCUMENTATION AND RESEARCH PURPOSES. THIS CODE SHALL NOT BE USED FOR PERSONAL USE OR MALICIOUS INTENTIONS INORDER TO MEET ETHICAL REQUIREMENTS. PLEASE DO NOT USE TRY THIS
# Owner: apv2@hw.ac.uk Aswin Valsalan 

import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox
import logging
import csv
from datetime import datetime
import platform
import random
import string
import shutil
import threading
import subprocess
import sqlite3
import os
# import pyPDF2


# Function to generate a random string (for unique playbook filename)
def random_string(length=6):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


# Setup logging
log_filename = 'threat_detection.log'
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(message)s')


# Function to clear previous logs
def clear_previous_logs():
    # Clears the content of the log file
    with open(log_filename, 'w'):
        pass


# Function to initialize playbook
def initialize_playbook():
    playbook_filename = f"incident_response_playbook.md"
    with open(playbook_filename, "w") as playbook_file:
        playbook_file.write("# Incident Response Playbook\n\n")


# Function to generate the incident response playbook
def generate_playbook(filepath, action):
    playbook_filename = f"incident_response_playbook.md"
    if not os.path.exists(playbook_filename):
        initialize_playbook()

    with open(playbook_filename, "a") as playbook_file:
        playbook_file.write("## New Incident\n\n")
        playbook_file.write("### Incident Details\n\n")
        playbook_file.write(f"- File Path: {filepath}\n")
        playbook_file.write(f"- Action: {action}\n")
        playbook_file.write("\n")


# Function to generate UML class diagram using Pyreverse
def generate_class_diagram():
    try:
        # Execute Pyreverse command to generate UML class diagram
        subprocess.run(["pyreverse", "finalAPV.py", "-o", "png"])
    except Exception as e:
        logging.error(f"Error in generating UML class diagram: {e}")


# Function to generate UML sequence diagram using Pyreverse
def generate_sequence_diagram():
    try:
        # Execute Pyreverse command to generate UML sequence diagram
        subprocess.run(["pyreverse", "finalAPV.py", "-o", "png"])
    except Exception as e:
        logging.error(f"Error in generating UML sequence diagram: {e}")


# Function to delete a selected file
def delete_file(filepath):
    try:
        os.remove(filepath)
        logging.warning(f"Deleted file: {filepath}")
        messagebox.showinfo("File Deleted", f"File deleted successfully: {filepath}")
        generate_playbook(filepath, "Deleted")
    except Exception as e:
        logging.error(f"Error in deleting file: {e}")
        messagebox.showerror("Error", f"Failed to delete file: {filepath}")


# Function to quarantine a selected file
def quarantine_file(filepath):
    # Add your quarantine logic here
    logging.warning(f"Quarantined file: {filepath}")
    messagebox.showinfo("File Quarantined", f"File quarantined: {filepath}")
    generate_playbook(filepath, "Quarantined")


# Function to open file dialog and start threat detection
def browse_files():
    filename = filedialog.askopenfilename(initialdir="/", title="Select File", filetypes=(("All files", "*.*"),))
    if filename:
        # Start threat detection process
        threading.Thread(target=analyze_file, args=(filename,)).start()


# Function to analyze files for potential threats
def analyze_file(filepath):
    try:
        # Implement threat detection logic here
        if contains_threat(filepath):
            logging.warning(f"Suspicious file detected: {filepath}")
            # Update playbook with incident details
            generate_playbook(filepath, "Detected")

            # Show detection in GUI
            add_to_detected_list(filepath)

            # Log analysis result to CSV
            log_to_csv(filepath, "Detected")

            # Generate UML sequence diagram
            generate_sequence_diagram()
    except Exception as e:
        logging.error(f"Error in analyzing file: {e}")


# Function to check if a file contains a threat
def contains_threat(filepath):
    threat_extensions = [".py", ".java", ".json", ".html", ".js", ".pdf"]
    threat_keywords = ["ransom", "malware", "trojan", "keylogger"]
    _, file_extension = os.path.splitext(filepath)
    if file_extension.lower() in threat_extensions:
        return True
    filename = os.path.basename(filepath)
    for keyword in threat_keywords:
        if keyword in filename.lower():
            return True
    return False


# Function to check for file anomalies, masked file extensions, file metadata, and MD5 hashes
def check_file_anomalies(filepath):
    try:
        # Get file size
        size = os.path.getsize(filepath)

        # Get file extension
        _, file_extension = os.path.splitext(filepath)

        # Get file permissions
        file_metadata = os.stat(filepath)
        file_permissions = file_metadata.st_mode

        # Get MD5 hash
        md5_hash = calculate_md5(filepath)

        # Log file anomalies
        logging.info(f"File Anomalies: "
                     f"File: {filepath}, "
                     f"Size: {size}, "
                     f"Extension: {file_extension}, "
                     f"Permissions: {file_permissions}, "
                     f"MD5 Hash: {md5_hash}")
    except Exception as e:
        logging.error(f"Error in checking file anomalies: {e}")


# Function to calculate MD5 hash of a file
def calculate_md5(filepath):
    with open(filepath, 'rb') as f:
        file_hash = hashlib.md5()
        while chunk := f.read(4096):
            file_hash.update(chunk)
    return file_hash.hexdigest()


# Function to check suspicious websites visited using Microsoft Edge browser
def check_suspicious_websites():
    try:
        # Path to Microsoft Edge browser history database file
        edge_history_path = os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Edge', 'User Data', 'Default',
                                         'History')

        # Connect to the Edge browser history database
        conn = sqlite3.connect(edge_history_path)
        cursor = conn.cursor()

        # Query to retrieve browsing history
        cursor.execute("SELECT url FROM urls")

        # Fetch all URLs from browsing history
        urls = cursor.fetchall()

        # Log suspicious websites
        for url in urls:
            logging.info(f"Suspicious website visited: {url[0]}")

        # Close database connection
        conn.close()
    except Exception as e:
        logging.error(f"Error in checking suspicious websites: {e}")


# Function to add detected file to the GUI list
def add_to_detected_list(filepath):
    listbox.insert(tk.END, filepath)


# Function to handle delete action on selected file in GUI list
def handle_delete_file():
    selected_index = listbox.curselection()
    if selected_index:
        selected_file = listbox.get(selected_index)
        delete_file(selected_file)


# Function to handle quarantine action on selected file in GUI list
def handle_quarantine_file():
    selected_index = listbox.curselection()
    if selected_index:
        selected_file = listbox.get(selected_index)
        quarantine_file(selected_file)

def quarantine_file(file_path):
    quarantine_dir = 'D:/Quarantine/'
    shutil.move(file_path, quarantine_dir)


# Function to handle cancel action on selected file in GUI list
def handle_cancel_action():
    window.destroy()


# Function to log analysis result to CSV
def log_to_csv(filepath, action):
    csv_filename = 'threat_analysis.csv'
    with open(csv_filename, mode='a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), filepath, action])


# Function to monitor file system changes for Windows
def monitor_file_system_windows():
    try:
        # List of drive letters to monitor on Windows
        drives = ['C:', 'D:', 'E:', 'F:', 'G:', 'H:']
        for drive in drives:
            # Recursively walk through each directory and file in the drive
            for root, dirs, files in os.walk(drive):
                for file in files:
                    # Construct full file path
                    filepath = os.path.join(root, file)
                    # Perform analysis on the file
                    analyze_file(filepath)
                    # Check file anomalies
                    check_file_anomalies(filepath)
    except Exception as e:
        logging.error(f"Error in monitoring file system: {e}")


# Function to monitor file system changes for Linux
def monitor_file_system_linux():
    try:
        # Recursively walk through each directory and file in the root directory '/'
        for root, dirs, files in os.walk('/'):
            for file in files:
                # Construct full file path
                filepath = os.path.join(root, file)
                # Perform analysis on the file
                analyze_file(filepath)
                # Check file anomalies
                check_file_anomalies(filepath)
    except Exception as e:
        logging.error(f"Error in monitoring file system: {e}")


# Create GUI window
window = tk.Tk()
window.title("Threat Detection Tool")

# Create GUI components
label = tk.Label(window, text="Detected Threats:")
label.pack(pady=10)

listbox = tk.Listbox(window, selectmode=tk.SINGLE, width=70)
listbox.pack(pady=5)

frame = tk.Frame(window)
frame.pack(pady=5)

delete_button = tk.Button(frame, text="Delete", command=handle_delete_file)
delete_button.pack(side=tk.LEFT, padx=5)

quarantine_button = tk.Button(frame, text="Quarantine", command=handle_quarantine_file)
quarantine_button.pack(side=tk.LEFT, padx=5)

cancel_button = tk.Button(frame, text="Cancel", command=handle_cancel_action)
cancel_button.pack(side=tk.LEFT, padx=5)

# Run appropriate file system monitoring function based on the operating system
if platform.system() == 'Windows':
    threading.Thread(target=monitor_file_system_windows).start()
    check_suspicious_websites()  # Check suspicious websites visited using Microsoft Edge
else:
    threading.Thread(target=monitor_file_system_linux).start()

# Run GUI application
window.mainloop()
