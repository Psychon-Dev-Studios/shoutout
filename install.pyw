import os, sys, subprocess, time
from threading import Thread as td
import tkinter as tk
from tkinter import messagebox
from zipfile import ZipFile

WINDRIVE = str(os.environ['WINDIR'].split(":\\")[0])
PATH = sys.path[0]
DoNotInstallShoutout = False
readme = """By clicking "install", you grant us permission to:
- Create and edit folders on your device
- Create, edit, and delete game files on your device
- Install additional required software
- Create a shortcut on your desktop

If you do not wish to grant us these permissions, please close the installer."""
installable = []
installed = []

if os.path.isfile(PATH + "/so.dat"):installable.append("Shoutout")

BLUE = "\u001b[34;1m" # The color blue
YELLOW = "\u001b[33;1m" # The color yellow
RED = "\u001b[31;1m" # The color red
GREEN = "\u001b[32;1m"
NORMAL = "\u001b[0m" # Reset to default color

def on_enter(e):e.widget['background'] = 'lightgreen'
def on_leave(e):e.widget['background'] = 'SystemButtonFace'

def RENDER():
    for widgets in root.winfo_children():
        widgets.destroy()
    tk.Label(root, text=readme, wraplength=950, justify="center", background="lightgray").pack()
    tk.Label(root, text=" ", background="lightgray").pack(pady=3)
    inst_main = tk.Button(root, text="Install Shoutout", command=installShoutout_strap, width="35")
    dn_inst_main = tk.Button(root, text="Can't Install: so.dat not found", width="35", state="disabled")
    inst_mpex = tk.Button(root, text="Install Multiplayer Extension", command=installMPEX_strap, width="35")

    inst_main.bind("<Enter>", on_enter)
    inst_main.bind("<Leave>", on_leave)
    inst_mpex.bind("<Enter>", on_enter)
    inst_mpex.bind("<Leave>", on_leave)
    
    if ("Shoutout" in installable):inst_main.pack()
    else:dn_inst_main.pack()
    if ("mpex" in installable):inst_mpex.pack()

    if (len(installable) == 0 and len(installed) > 0):
        cleanup()

def cleanup():
    os.remove(__file__)
    messagebox.showinfo("Shoutout", "Nothing left to install!")
    os.abort()

def nothing_available():
    messagebox.showinfo("Shoutout", "Nothing installable found. Make sure the .dat files are in the same directory as this installer.")
    os.abort()

def installShoutout_strap():
    td(name="_installer", target=installShoutout).start()
    root.wm_title("Installing...")
    messagebox.showinfo("Installer", "Please wait while we install Shoutout. Don't close the installer.")
def installMPEX_strap():
    # td(name="_installer", target=installMPEX).start()
    # root.wm_title("Installing...")
    # messagebox.showinfo("Installer", "Please wait while we install the Multiplayer Extension. Don't close the installer.")
    messagebox.showinfo("Installer", "Although the installer still checks for the existence of the multiplayer extension package, we do not ship it with Shoutout. We only distribute a multiplayer extension for Freddy's Hall, which is incompatible with CamX. This installer will not permit the installation of the multiplayer extension.")

def installShoutout():
    global installable

    try:
        from win32com.client import Dispatch
        dispatch_needed = False
    except: dispatch_needed = True

    if (dispatch_needed):
        print(YELLOW + "Step 1\nInstalling Dispatch")
        subprocess.call("pip install pywin32")
        os.startfile(__file__)
        os.abort()

    else:print(YELLOW + "Skipping step 1: requirement already met!")
    time.sleep(0.7)

    print(YELLOW + "Step 2\nCreating directories")
    time.sleep(0.3)
    try:os.mkdir(WINDRIVE + ":/ProgramData/shoutout")
    except:print(RED + "Warning: directory already exists. The current installation will be overwritten.\n")

    os.system("cls")

    print(YELLOW + "Step 3\nUnpacking Shoutout")
    try:
        with ZipFile(sys.path[0] + "/so.dat") as data:
            data.extractall(WINDRIVE + ":/ProgramData/shoutout")
            data.close()

    except:
        print(RED + "\nError: so.dat could not be opened. The file may be corrupted.")
        messagebox.showerror("Shoutout", "An error occured while opening so.dat. The file may be corrupted.")
        time.sleep(999)
        os.abort()
    time.sleep(1.5)

    time.sleep(1.5)
    os.system("cls")

    time.sleep(0.7)
    os.system("cls")
    print(YELLOW + "Step 5\nCreating desktop shortcut(s)...")

    target = WINDRIVE + ":/ProgramData/shoutout/client.py"
    wDir = WINDRIVE + ":/ProgramData/shoutout/"
    icon = "%s:/ProgramData/shoutout/chat-bubble-color.ico"%WINDRIVE
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(WINDRIVE + ":/Users/" + os.getlogin() + "/Desktop/Shoutout.lnk")
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = wDir
    shortcut.description = "A simple same-network chat client"
    shortcut.IconLocation = icon
    shortcut.save()

    installable.remove("Shoutout")
    installed.append("Shoutout")
    os.remove(PATH + "/so.dat")
    root.wm_title("Shoutout - Installer")
    RENDER()

if ("Project" in sys.path[0] or "VisualStudioCode" in sys.path[0]):
    print(RED + "abort" + NORMAL)
    os.abort()

if not os.path.isfile(sys.path[0] + "/so.dat"):
    DoNotInstallCXR = True
print("\n")

## Create screen ##
root = tk.Tk()
root.wm_geometry("600x200")
root.grid_anchor("center")
root.wm_title("Shoutout - Installer")
root.wm_resizable(width=False, height=False)
root.config(background="lightgray")

if not ("nt" in os.name):
    messagebox.showinfo("CXR Installer", "Shoutout is only properly supported on Windows")
    root.wm_title("Exiting...")
    os.abort()

RENDER()

if (__name__ == "__main__"):
    # root.eval('tk::PlaceWindow . left')
    root.mainloop()