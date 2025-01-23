
import os
from tkinter import messagebox
import shutil
from urllib.request import urlopen
import tkinter as tk

#FTP Definitions
ftp_url = "https://luan.sternblick.ch"
ftp_path = "/ftp"
filename = "version.txt"


#Updater/Installer Definitions
current_dir = os.path.join(os.environ["USERPROFILE"], "FlappyKnight")
installer = "installer_update.exe"
installer_path = os.path.join(current_dir, installer)
game = "FlappyKnight.exe"
game_path = os.path.join(current_dir, game)
versionpath = os.path.join(current_dir, "Dependencies")
filepath = os.path.join(versionpath, "version.txt")

with open(filepath, 'r') as versionfile:
    local_version = float(versionfile.read())

#Installer Definitions
temp_path = os.path.join(os.environ["TEMP"], "FlappyTemp")
temp_file_path = os.path.join(temp_path, "installer_update.exe")

# Construct the FTP URL
ftp_full_path = ftp_url + ftp_path + "/" + filename

# Open the FTP URL and read the contents of the file
with urlopen(ftp_full_path) as response:
    server_version = float(response.read().decode('utf-8'))


def ask_update():
    def on_yes():
        global update
        update = True
        root.destroy()

    def on_no():
        global update
        update = False
        root.destroy()

    # Initialize Tkinter
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Create the messagebox
    result = messagebox.askyesno("Update available!", "There's an update available. Do you want to install it? If you havent exported your highscores, say no to the question, and export them by pressing RSHIFT in game. You can import them by pressing ENTER after the update.")

    # Process the result
    if result:
        on_yes()
    else:
        on_no()

if server_version > local_version:
    ask_update()
    if update == True:

        os.makedirs(temp_path, exist_ok=True)
        shutil.copy(installer_path, temp_path)
        os.system(temp_file_path)
    if update == False:
        os.system(game_path)
else:
    os.system(game_path)