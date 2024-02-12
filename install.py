# entry point of the installation process
# displays the picker to select an script to install
# and the installation progress


# import the required modules
# import os
# import sys
# import time
import subprocess
import pkgutil
# import tkinter as tk
# from tkinter import filedialog
# from tkinter import messagebox

# display a picker to choose which file to import using whiptail
# example
# from install_script import pihole
# from install_script import homeassistant

apps = []
for _, name, _ in pkgutil.iter_modules(['install_script']):
    apps.append(name)
    apps.append('install {}'.format(name))
def picker():
    a = subprocess.run([('whiptail'), '--title', 'Install Script', '--menu', 'Choose an application to install', '15', '50', '5'] + apps, stderr = subprocess.PIPE)
    a= a.stderr.decode('utf-8').strip()
    app = getattr(__import__('install_script.{}'.format(a)), a)
    config = app.config()
    config.menu()
picker()