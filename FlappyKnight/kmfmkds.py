import urllib.request
import os
from tkinter import filedialog, Tk
from tqdm import tqdm
from pathlib import Path
import shutil
from tkinter import messagebox
import zipfile
from win32com.client import Dispatch
import time



install_dir = os.path.join(os.environ["USERPROFILE"], "FlappyKnight")
print(install_dir)

# Create the installation directory if it doesn't exist
os.makedirs(install_dir, exist_ok=True)

# Destination paths for the files
additional_file_destination = os.path.join(install_dir, "game.zip")
dependencies_folder = os.path.join(install_dir, "Dependencies")







# Show a message box indicating the completion of the download and installation
messagebox.showinfo("Download & Install is beginning", "The Downloading and installing process has started. If it does not work or gets stuck, try restarting your PC and try again. If this doesnt work, DM @Gaminguide1000 on Discord. Enjoy!")

# Optionally, create a shortcut on the desktop (requires the `pywin32` module)
# Uncomment the following lines if you want to create a desktop shortcut
print(1)


from ftplib import FTP

def download_file_from_ftp(ftp_url, ftp_path, filename, local_path, username, password):
    try:
        # Connect to the FTP server
        ftp = FTP(ftp_url)
        ftp.login(user=username, passwd=password)

        # Change to the directory where the file is located
        ftp.cwd(ftp_path)

        # Download the file to the specified local path
        local_file_path = f"{local_path}/{filename}"
        with open(local_file_path, 'wb') as local_file:
            ftp.retrbinary('RETR ' + filename, local_file.write)

        print(f"File {filename} downloaded successfully to {local_file_path}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # Close the FTP connection
        ftp.quit()


def increment_and_update_ftp_file(ftp_url, ftp_path, filename, username, password):     # Connect to the FTP server
    ftp = FTP(ftp_url)
    ftp.login(user=username, passwd=password)

    # Change to the directory where the file is located
    ftp.cwd(ftp_path)

     # Read the current content of the file
    with open(filename, 'wb') as local_file:
        ftp.retrbinary('RETR ' + filename, local_file.write)

    # Increment the value
    with open(filename, 'r') as local_file:
        current_value = int(local_file.read())
        new_value = current_value + 1

        # Write the updated value back to the file
    with open(filename, 'w') as local_file:
        local_file.write(str(new_value))

        # Upload the modified file back to the FTP server
    with open(filename, 'rb') as local_file:
        ftp.storbinary('STOR ' + filename, local_file)

    ftp.quit()

# Example usage:
ftp_url = "luan.sternblick.ch"
ftp_path = "/ftp"
filename = "game.zip"
username = "luanftp.sternblick.ch"
password = "Luan-Ftp12"  # Replace with a more secure method in a production environment

print(2)

download_file_from_ftp(ftp_url, ftp_path, filename, install_dir, username, password)

with zipfile.ZipFile(additional_file_destination, 'r') as zip_ref:
    zip_ref.extractall(dependencies_folder)
filename = "downloads.txt"

print(3)

increment_and_update_ftp_file(ftp_url, ftp_path, filename, username, password)
print(4)
os.remove(additional_file_destination)
print(5)
start_exe_path = os.path.join(install_dir, "Dependencies", "start.exe")
desktop = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
shell = Dispatch("WScript.Shell")
shortcut = shell.CreateShortCut(os.path.join(desktop, "FlappyKnight.lnk"))
shortcut.Targetpath = os.path.join(start_exe_path)
shortcut.save()
