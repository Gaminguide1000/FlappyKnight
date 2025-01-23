import urllib.request
import os
from tkinter import messagebox
from tqdm import tqdm
from pathlib import Path
import zipfile
from win32com.client import Dispatch
import time
import ctypes
import platform
import shutil

platfrm = platform.system()

messagebox.showinfo("Download & Install in progress...", "The Download & Install has started! If something goes wrong, restart your PC and try again. If it does not work after multiple tries, DM @Gaminguide1000 on Discord. It will take some time, so be patient. Enjoy!")

def download_file_with_progress(url, destination):
    
            response = urllib.request.urlopen(url)
            total_size = int(response.headers['Content-Length']) if 'Content-Length' in response.headers else None
            start_time = time.time()
            with tqdm(unit='B', unit_scale=True, miniters=1, desc="Downloading", leave=False, total=total_size) as tqdm_instance, open(destination, 'wb') as out_file:
                data = response.read(1024)
                while data:
                    out_file.write(data)
                    tqdm_instance.update(len(data))
                    data = response.read(1024)
                    if time.time() - start_time > 200:
                        break

            return  # Download successful, exit the loop


additional_file_url = "http://luan.sternblick.ch/ftp/game.zip"
if platfrm == "Windows":
    install_dir = Path(os.path.join(os.environ["USERPROFILE"], "FlappyKnight"))
elif platfrm == "Darwin":
    home_directory = os.path.expanduser("~")
    file_path = os.path.join(home_directory, "FlappyKnight")

os.system("taskkill /f /im  updater.exe")
shutil.rmtree(install_dir)
os.makedirs(install_dir, exist_ok=True)

additional_file_destination = os.path.join(install_dir, "game.zip")
max_retries = 5
def unzip():
    for attempt in range(1, max_retries + 1):
        try:
            download_file_with_progress(additional_file_url, additional_file_destination)

            with zipfile.ZipFile(additional_file_destination, 'r') as zip_ref:
                zip_ref.extractall(install_dir)
            
            return
        except Exception as e:
            print(f"Error downloading file (Attempt {attempt}/{max_retries}): {e}")
            messagebox.showerror("Download Failed!", "The Download failed, retrying 3 seconds after closing this Window...")
            time.sleep(3)  # Wait for 5 seconds before retrying

unzip()

os.remove(additional_file_destination)


os.chdir(install_dir)

ftp_url = "luan.sternblick.ch"
ftp_path = "/ftp"
filename = "downloads.txt"




start_exe_path = os.path.join(install_dir, "updater.exe")
CSIDL_DESKTOPDIRECTORY = 0x10
desktop_path_buf = ctypes.create_unicode_buffer(260)
ctypes.windll.shell32.SHGetFolderPathW(0, CSIDL_DESKTOPDIRECTORY, 0, 0, desktop_path_buf)
desktop_path = Path(desktop_path_buf.value)
desktop = desktop_path
shell = Dispatch("WScript.Shell")
shortcut = shell.CreateShortCut(os.path.join(desktop, "FlappyKnight.lnk"))
shortcut.Targetpath = os.path.join(start_exe_path)
shortcut.save()

messagebox.showinfo("Download & Install Complete", "Download & Install complete!")
