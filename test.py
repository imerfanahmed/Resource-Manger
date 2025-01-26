import tkinter as tk
from tkinter import PhotoImage
import os

def open_exe(file_path):
    os.startfile(file_path)

def create_icon_button(root, image_path, exe_path):
    icon = PhotoImage(file=image_path)
    button = tk.Button(root, image=icon, command=lambda: open_exe(exe_path))
    button.image = icon  # Keep a reference to avoid garbage collection
    button.pack(side=tk.LEFT)

root = tk.Tk()
root.title("Icon Launcher")

# Example usage
create_icon_button(root, "./assets/ea.png", "C:\Program Files\Electronic Arts\EA Desktop\EA Desktop\EALauncher.exe")
# create_icon_button(root, "path/to/icon2.png", "path/to/exe2.exe")
# create_icon_button(root, "path/to/icon3.png", "path/to/exe3.exe")

root.mainloop()