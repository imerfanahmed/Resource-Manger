import tkinter as tk
from tkinter import ttk, messagebox
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
    selected_tv_logo = os.path.join(selected_tv_logo, 'data')
    selected_scoreboard = os.path.join(selected_scoreboard, 'data')
    
    print(selected_scoreboard, selected_tv_logo)
    
    # Define source and destination directories
    source_tv_logo = os.path.join(tv_logo_directory, selected_tv_logo)
    source_scoreboard = os.path.join(scoreboard_directory, selected_scoreboard)
    destination_directory = "C:\\FC 25 Live Editor\\mods\\legacy"
    
    # Ensure the destination directory exists
    os.makedirs(destination_directory, exist_ok=True)
    
    # Copy the selected directories to the destination
    shutil.copytree(source_tv_logo, os.path.join(destination_directory, 'data'), dirs_exist_ok=True)
    shutil.copytree(source_scoreboard, os.path.join(destination_directory, 'data'), dirs_exist_ok=True)
    
    # Show success message
    messagebox.showinfo("Success", "Settings Applied and directories copied successfully")

def on_tv_select():
    selected_tv_logo = tv_options[tv_var.get()]
    print("TV Logo Selected:", selected_tv_logo)
    
    try:
        # Load and resize the preview image
        img_path = os.path.join(tv_logo_directory, selected_tv_logo, "preview.jpg")
        img = Image.open(img_path)
        img_tk = ImageTk.PhotoImage(img)
        
        # Update the preview label
        preview1.config(image=img_tk)
        preview1.image = img_tk
    except Exception as e:
        print(f"Error loading preview image: {e}")
        messagebox.showerror("Error", "Could not load preview image")
    
def on_scoreboard_select():
    selected_scoreboard = scoreboard_options[scoreboard_var.get()]
    print("Scoreboard Selected:", selected_scoreboard)
    
    try:
        # Load and resize the preview image
        img_path = os.path.join(scoreboard_directory, selected_scoreboard, "preview.jpg")
        img = Image.open(img_path)
        img_tk = ImageTk.PhotoImage(img)
        
        # Update the preview label
        preview2.config(image=img_tk)
        preview2.image = img_tk
    except Exception as e:
        print(f"Error loading preview image: {e}")
        messagebox.showerror("Error", "Could not load preview image")

# Top icons frame
top_frame = tk.Frame(root, bg="black")
top_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

icons = ["one.png", "two.png", "three.png", "four.png", "five.png"]
for icon in icons:
    icon_path = os.path.join("./assets", icon)
    img = Image.open(icon_path).resize((40, 40))
    img_tk = ImageTk.PhotoImage(img)
    label = tk.Label(top_frame, image=img_tk, bg="black")
    label.image = img_tk
    label.pack(side=tk.LEFT, padx=5)

# Separator between top icons and middle frame
separator_top = ttk.Separator(root, orient='horizontal')
separator_top.pack(fill='x', padx=20, pady=5)

# Middle frame with options and previews
middle_frame = tk.Frame(root, bg="black")
middle_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Left frame for options
left_frame = tk.Frame(middle_frame, bg="black")
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

# Scrollable area for TV Logos and Scoreboards
left_scroll_canvas = tk.Canvas(left_frame, bg="black", highlightthickness=0)
left_scroll_canvas.pack(side=tk.LEFT, fill=tk.Y, expand=True)

scrollbar_left = tk.Scrollbar(left_frame, orient="vertical", command=left_scroll_canvas.yview)
scrollbar_left.pack(side=tk.RIGHT, fill=tk.Y)

scrollable_left_frame = tk.Frame(left_scroll_canvas, bg="black")
left_scroll_canvas.create_window((0, 0), window=scrollable_left_frame, anchor="nw")
left_scroll_canvas.configure(yscrollcommand=scrollbar_left.set)

# TV Logos section
tv_logo_directory = "./resources/tv_logo"
tv_options = [name for name in os.listdir(tv_logo_directory) if os.path.isdir(os.path.join(tv_logo_directory, name))]
tv_var = tk.IntVar(value=0)  # Default to the first option

tv_label = tk.Label(scrollable_left_frame, text="TV Logos", fg="white", bg="black", anchor="w")
tv_label.pack(fill=tk.X)

for index, option in enumerate(tv_options):
    radio = tk.Radiobutton(scrollable_left_frame, text=option, variable=tv_var, value=index,
                           bg="black", fg="white", selectcolor="black", command=on_tv_select)
    radio.pack(anchor="w")

# Separator between TV Logos and Scoreboards
separator = ttk.Separator(scrollable_left_frame, orient='horizontal')
separator.pack(fill='x', pady=10)

# Scoreboards section
scoreboard_directory = "./resources/scoreboards"
scoreboard_options = [name for name in os.listdir(scoreboard_directory) if os.path.isdir(os.path.join(scoreboard_directory, name))]
scoreboard_var = tk.IntVar(value=0)  # Default to the first option

scoreboard_label = tk.Label(scrollable_left_frame, text="Scoreboards", fg="white", bg="black", anchor="w")
scoreboard_label.pack(fill=tk.X, pady=(10, 0))

for index, option in enumerate(scoreboard_options):
    radio = tk.Radiobutton(scrollable_left_frame, text=option, variable=scoreboard_var, value=index,
                           bg="black", fg="white", selectcolor="black", command=on_scoreboard_select)
    radio.pack(anchor="w")

# Configure scrolling for the left section
scrollable_left_frame.update_idletasks()
left_scroll_canvas.config(scrollregion=left_scroll_canvas.bbox("all"))

# Right frame for previews
right_frame = tk.Frame(middle_frame, bg="black")
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Scrollable area for previews
preview_canvas = tk.Canvas(right_frame, bg="black", highlightthickness=0)
preview_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar_right = tk.Scrollbar(right_frame, orient="vertical", command=preview_canvas.yview)
scrollbar_right.pack(side=tk.RIGHT, fill=tk.Y)

scrollable_right_frame = tk.Frame(preview_canvas, bg="black")
preview_canvas.create_window((0, 0), window=scrollable_right_frame, anchor="nw")
preview_canvas.configure(yscrollcommand=scrollbar_right.set)

# Add preview labels
preview1 = tk.Label(scrollable_right_frame, text="[BeIN Sports Preview]", fg="white", bg="black")
preview1.pack(pady=5)

# Add a separator
separator = ttk.Separator(scrollable_right_frame, orient='horizontal')
separator.pack(fill='x', pady=10)

preview2 = tk.Label(scrollable_right_frame, text="[Scoreboard Preview]", fg="white", bg="black")
preview2.pack(pady=5)

# Configure scrolling for the right section
scrollable_right_frame.update_idletasks()
preview_canvas.config(scrollregion=preview_canvas.bbox("all"))
# Apply button
apply_button = tk.Button(root, text="APPLY", bg="gray", fg="white", command=on_apply)
apply_button.pack(side=tk.BOTTOM, pady=10)

# Handle window close
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
