import os
import time
import threading
import logging
import platform
import random
import string
import sys

# Function to generate a random string (for unique playbook filename)
def random_string(length=6):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

# Setup logging
log_filename = 'ransomware_detection.log'
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(message)s')

# Function to clear previous logs
def clear_previous_logs():
    with open(log_filename, 'w'):
        pass

# Flag to track whether playbook has been generated
playbook_generated = False

# Function to monitor file system changes for Windows
def monitor_file_system_windows():
    try:
        drives = ['C:', 'D:']
        for drive in drives:
            for root, dirs, files in os.walk(drive + '\\'):
                for file in files:
                    filepath = os.path.join(root, file)
                    # Perform analysis on the file
                    analyze_file(filepath)

        # Terminate Python execution after potential ransomware/malware are deleted
        sys.exit()

    except Exception as e:
        logging.error(f"Error in monitoring file system: {e}")

# Function to monitor file system changes for Linux
def monitor_file_system_linux():
    try:
        import pyinotify

        class EventHandler(pyinotify.ProcessEvent):
            def process_default(self, event):
                filepath = event.pathname
                # Perform analysis on the file
                analyze_file(filepath)

        wm = pyinotify.WatchManager()
        handler = EventHandler()
        notifier = pyinotify.Notifier(wm, handler)
        wdd = wm.add_watch('/', pyinotify.IN_CLOSE_WRITE, rec=True)

        notifier.loop()

    except Exception as e:
        logging.error(f"Error in monitoring file system: {e}")

# Function to analyze files for ransomware behavior
def analyze_file(filepath):
    global playbook_generated

    try:
        # Implement ransomware detection logic here
        if is_ransomware(filepath):
            logging.warning(f"Potential ransomware detected: {filepath}")
            if not playbook_generated:
                generate_playbook(filepath)
                playbook_generated = True
            block_ransomware(filepath)

    except Exception as e:
        logging.error(f"Error in analyzing file: {e}")

# Function to check if a file exhibits ransomware-like behavior
def is_ransomware(filepath):
    # List of ransomware file extensions
    ransomware_extensions = [".lock", ".crypt", ".encrypt"]

    # Check if the file exists and has any of the ransomware extensions
    if any(ext in filepath.lower() for ext in ransomware_extensions):
        return True
    
    # Check if the file is a Python file
    _, file_extension = os.path.splitext(filepath)
    if file_extension.lower() == ".py":
        return True

    return False

# Function to take action to block ransomware
def block_ransomware(filepath):
    try:
        # Check if the file is a Python file and not myAPV.py
        _, filename = os.path.split(filepath)
        if filename.lower() == "myapv.py":
            logging.warning(f"Skipped deleting whitelisted file: {filepath}")
            return

        # Check if the file is a Python file
        _, file_extension = os.path.splitext(filepath)
        if file_extension.lower() == ".py":
            os.remove(filepath)
            logging.warning(f"Deleted potential ransomware/malware Python file: {filepath}")
        else:
            logging.warning(f"Skipped deleting non-malicious file: {filepath}")
    except Exception as e:
        logging.error(f"Error in deleting file: {e}")

# Function to generate the incident response playbook
def generate_playbook(filepath):
    playbook_filename = f"ransomware_incident_response_playbook_{random_string()}.md"
    with open(playbook_filename, "w") as playbook_file:
        playbook_file.write("# Ransomware Incident Response Playbook\n\n")
        playbook_file.write("## 1. Initial Detection and Assessment\n\n")
        playbook_file.write("- Monitor file system for ransomware-like behavior.\n")
        playbook_file.write("- Identify indicators of ransomware infection.\n\n")
        playbook_file.write("## 2. Incident Response\n\n")
        playbook_file.write("- Isolate affected systems to prevent further spread.\n")
        playbook_file.write("- Disable network connections to contain the threat.\n")
        playbook_file.write("- Coordinate with cybersecurity team for further analysis.\n\n")
        playbook_file.write("## 3. Data Recovery and Restoration\n\n")
        playbook_file.write("- Identify backup solutions for affected data.\n")
        playbook_file.write("- Restore systems from clean backups.\n\n")
        playbook_file.write("## 4. Post-Incident Activities\n\n")
        playbook_file.write("- Communicate incident details to stakeholders.\n")
        playbook_file.write("- Conduct a post-incident review to identify improvements.\n\n")
        playbook_file.write("## 5. Continuous Improvement\n\n")
        playbook_file.write("- Enhance security measures to prevent future ransomware attacks.\n")
        playbook_file.write("- Educate employees on recognizing and reporting ransomware threats.\n\n")
        playbook_file.write("### Incident Details\n\n")
        playbook_file.write(f"- File Path: {filepath}\n")

# Main function
if __name__ == "__main__":
    # Clear previous logs
    clear_previous_logs()

    # Create a separate thread for monitoring the file system
    if platform.system() == "Windows":
        file_system_thread = threading.Thread(target=monitor_file_system_windows)
    elif platform.system() == "Linux":
        file_system_thread = threading.Thread(target=monitor_file_system_linux)

    file_system_thread.daemon = True  # Set as daemon thread to stop monitoring when the main thread exits
    file_system_thread.start()

    # Main thread continues for other tasks or can exit if needed
    try:
        while True:
            time.sleep(1)
            # Main thread can perform other tasks if needed
    except KeyboardInterrupt:
        logging.info("Ransomware detection stopped by user.")
