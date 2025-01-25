import tkinter as tk
from tkinter import ttk,messagebox
from PIL import Image, ImageTk
import os
import shutil

# Create the main window
root = tk.Tk()
root.title("KO's Resource Manager")
root.geometry("800x800")
root.configure(bg="black")

def on_apply():
    selected_tv_logo = tv_options[tv_var.get()]
    selected_scoreboard = scoreboard_options[scoreboard_var.get()]
    #get to the data folder
    selected_tv_logo = os.path.join(selected_tv_logo, 'data')
    selected_scoreboard = os.path.join(selected_scoreboard, 'data')
    
    print(selected_scoreboard,selected_tv_logo)
    
    # Define source and destination directories
    source_tv_logo = os.path.join(tv_logo_directory, selected_tv_logo)
    source_scoreboard = os.path.join(scoreboard_directory, selected_scoreboard)
    destination_directory = "C:\FC 25 Live Editor\mods\legacy"
    
    # Ensure the destination directory exists
    os.makedirs(destination_directory, exist_ok=True)
    
    # Copy the selected directories to the destination
    shutil.copytree(source_tv_logo, os.path.join(destination_directory, 'data'), dirs_exist_ok=True)
    shutil.copytree(source_scoreboard, os.path.join(destination_directory, 'data'), dirs_exist_ok=True)
    
     # Show success message
    messagebox.showinfo("Success", "Settings Applied and directories copied successfully")

def on_tv_select():
    selected_tv_logo = tv_options[tv_var.get()]
    #show the preview image of the selected tv logo
    print("TV Logo Selected:", selected_tv_logo)
    # Replace with actual paths to your images
    img = Image.open(os.path.join(tv_logo_directory, selected_tv_logo, "preview.png")).resize((200, 200))
    img_tk = ImageTk.PhotoImage(img)
    preview1.config(image=img_tk)
    preview1.image = img_tk  # Keep a reference to avoid garbage collection
    

def on_scoreboard_select():
    selected_scoreboard = scoreboard_options[scoreboard_var.get()]
    print("Scoreboard Selected:", selected_scoreboard)

def on_icon_left_click(event):
    print("Icon left-clicked")

def on_icon_right_click(event):
    print("Icon right-clicked")

# Top icons frame
top_frame = tk.Frame(root, bg="black")
top_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

icons = ["one.png", "two.png", "three.png", "four.png", "five.png"]
for icon in icons:
    # Replace with actual paths to your images
    img = Image.open(icon).resize((40, 40))
    img_tk = ImageTk.PhotoImage(img)
    label = tk.Label(top_frame, image=img_tk, bg="black")
    label.image = img_tk  # Keep a reference to avoid garbage collection
    label.pack(side=tk.LEFT, padx=5)
    label.bind("<Button-1>", on_icon_left_click)
    label.bind("<Button-3>", on_icon_right_click)

# Middle frame with options
middle_frame = tk.Frame(root, bg="black")
middle_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Left frame for options
left_frame = tk.Frame(middle_frame, bg="black")
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

# TV Logos section
tv_label = tk.Label(left_frame, text="TV Logos", fg="white", bg="black", anchor="w")
tv_label.pack(fill=tk.X)

tv_logo_directory = "./resources/tv_logo"

tv_options = [name for name in os.listdir(tv_logo_directory) if os.path.isdir(os.path.join(tv_logo_directory, name))]
print(tv_options)
tv_var = tk.IntVar(value=0)  # Default to the first option

for index, option in enumerate(tv_options):
    radio = tk.Radiobutton(left_frame, text=option, variable=tv_var, value=index, bg="black", fg="white", selectcolor="black", command=on_tv_select)
    radio.pack(anchor="w")

# Scoreboards section
scoreboard_label = tk.Label(left_frame, text="Scoreboards", fg="white", bg="black", anchor="w")
scoreboard_label.pack(fill=tk.X, pady=(10, 0))
scoreboard_directory = "./resources/scoreboards"
scoreboard_options = [name for name in os.listdir(scoreboard_directory) if os.path.isdir(os.path.join(scoreboard_directory, name))]
scoreboard_var = tk.IntVar(value=1)  # Default to the first option

for index, option in enumerate(scoreboard_options):
    radio = tk.Radiobutton(left_frame, text=option, variable=scoreboard_var, value=index, bg="black", fg="white", selectcolor="black", command=on_scoreboard_select)
    radio.pack(anchor="w")

# Right frame for previews
right_frame = tk.Frame(middle_frame, bg="black")
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Add preview images
preview1 = tk.Label(right_frame, text="[BeIN Sports Preview]", fg="white", bg="black")
preview1.pack(pady=5)

preview2 = tk.Label(right_frame, text="[Scoreboard Preview]", fg="white", bg="black")
preview2.pack(pady=5)

# Apply button
apply_button = tk.Button(root, text="APPLY", bg="gray", fg="white", command=on_apply)
apply_button.pack(side=tk.BOTTOM, pady=10)


#tkinter on close fire a function
def on_close():
    try:
        shutil.rmtree(r"C:\FC 25 Live Editor\mods\legacy\data\ui\game")
    except:
        print("No data to delete")
    root.destroy()
    print("Closing the application")

root.protocol("WM_DELETE_WINDOW", on_close)

# Start the main loop
root.mainloop()