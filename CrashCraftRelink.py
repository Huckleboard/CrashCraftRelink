#  © 2023 Huckleboard. All rights reserved.
#  This file is part of the CrashCraft Relink project.
#
#  CrashCraft Relink is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Please note that logos, branding, and other creative assets found 
#  in the "resources" folder are proprietary content of CrashCraft and 
#  its creator. These assets are not covered by the GNU General Public License
#  and you are not permitted to use them without explicit permission.
#
#  CrashCraft Relink is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with CrashCraft Relink. If not, see <https://www.gnu.org/licenses/>.
#
#  If you fork, give credit where it is due! (GPL)
#  Thanks!


import tkinter as tk
from tkinter import PhotoImage
from tkinter import messagebox
import subprocess
import webbrowser
import os
import sys
import platform


def open_url(event):
    webbrowser.open_new("https://github.com/Huckleboard/CrashCraftRelink")
def run_commands():
    current_os = platform.system().lower()

    if current_os == 'windows':
        commands = [
            ('Flushing Old Domains...', 'ipconfig /flushdns'),
            ('Releasing...', 'ipconfig /release'),
            ('Renewing...', 'ipconfig /renew'),
            ('Resetting default settings...', 'netsh int ip reset'),
            ('Deleting old caches...', 'netsh interface ip delete arpcache')
        ]
    elif current_os == 'darwin':
        commands = [
            ('Flushing Old Domains...', 'sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder'),
            ('Releasing...', 'sudo ipconfig set en0 NONE'),  
            ('Renewing...', 'sudo ipconfig set en0 DHCP'),
        ]
        text.insert(tk.END, 'Note: CrashCraft Relink is running in compatibility mode (MacOS). You may be prompted to enter your password to run fixes.\n')
    elif current_os == 'linux':
        commands = [
            ('Flushing Old Domains...', 'sudo systemd-resolve --flush-caches'),  
            ('Releasing...', 'sudo dhclient -r'),  
            ('Renewing...', 'sudo dhclient'),  
        ]
        text.insert(tk.END, 'Note: CrashCraft Relink is running in compatibility mode (Linux). You may be prompted to enter your password to run fixes.\n')
    else:
        text.insert(tk.END, f'Sorry, but the CrashCraft Relink tool cannot run on {current_os}\n')
        return

    for message, command in commands:
        try:
            text.insert(tk.END, message + '\n')
            app.update_idletasks()

            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            output, error = process.communicate()

            if process.returncode == 0:
                text.insert(tk.END, 'Success!\n')
            else:
                text.insert(tk.END, f'Error: {error}\n')

            text.insert(tk.END, '-'*50 + '\n')
        except Exception as e:
            text.insert(tk.END, f'Exception: {str(e)}\n')

        text.see(tk.END)

    text.insert(tk.END, 'All Done!! Try and join the server now!\n\nIf Errors showed up here, dont worry! Try to connect to the server.\n\nStill having issues? DM me!')
    text.see(tk.END)

#get image path
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


app = tk.Tk()
app.title('CrashCraft Relink')
app.resizable(False, False)

bg_color = '#2C2F33'
fg_color = '#FFFFFF'
button_color = '#7289DA'
app.configure(bg=bg_color)

title = tk.Label(app, text='CrashCraft Relink', font=('Arial', 16), fg=fg_color, bg=bg_color)
title.pack(pady=10)

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

logo_img = PhotoImage(file=resource_path('resources/CClogosmall.png'))
resized_logo = logo_img.subsample(3, 3)  
logo = tk.Label(app, image=resized_logo, bg=bg_color)  
logo.pack(pady=2)

#imgs
logo_img = PhotoImage(file=resource_path('resources/CClogosmall.png'))
app.iconbitmap(resource_path('resources/icon.ico'))


explanation_text_font = ('Arial', 12)  
explanation_text = 'This utility will reload some networking settings to get you back on the server! \n\nOne of the most common ways your PC cannot connect to the server is due to an out-dated Domain Cache remembering an old IP that goes nowhere.\nThis program will fix that issue and hopefully get you playing again!\n\nThis tool also supports Linux and Mac, however it is primarily designed and                 developed for windows.\nIf you are using a windows .EXE emulator to run this on Mac or Linux, please              download the appropriate version based on your OS. \n(There will be no effect if you run this in a VM or emulator!!!)\n '
text_box = tk.Text(app, height=7, width=65, bg=bg_color, fg=fg_color, font=explanation_text_font)
text_box.insert(tk.END, explanation_text)
text_box.config(state=tk.DISABLED) 
text_box.pack(pady=10)

button_size = {'height': 2, 'width': 20} 
run_button = tk.Button(app, text='Run', command=run_commands, bg=button_color, fg=fg_color, **button_size)
run_button.pack(pady=20)



text = tk.Text(app, height=10, width=80, bg=bg_color, fg=fg_color)
text.pack(pady=20)
text.insert(tk.END, 'Click the button to run...\n')


watermark = tk.Label(app, text="About", fg="gray", cursor="hand2", bg=bg_color)
watermark.pack(side="bottom")
watermark.bind("<Button-1>", open_url)

current_os = platform.system().lower()
if current_os == 'darwin':
    messagebox.showinfo("Compatibility Mode", "CrashCraft Relink is running in compatibility mode for macOS. Some features may differ or require additional permissions")
elif current_os == 'linux':
    messagebox.showinfo("Compatibility Mode", "CrashCraft Relink is running in compatibility mode for Linux. Some features may differ or require additional permissions.")


app.mainloop()
