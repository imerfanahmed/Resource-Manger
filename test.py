import tkinter as tk
from PIL import Image, ImageTk

# Create the main window
root = tk.Tk()
root.title("Image Button Click Example")
root.geometry("400x300")

# Load an image for the button (ensure the image exists in the same directory)
image = Image.open("one.png").resize((100, 50))  # Resize as needed
button_image = ImageTk.PhotoImage(image)

# Function to handle left click
def on_left_click(event):
    label.config(text="Left Click on the Button!")

# Function to handle right click
def on_right_click(event):
    label.config(text="Right Click on the Button!")

# Create a button with an image
button = tk.Label(root, image=button_image, cursor="hand2")
button.pack(pady=20)

# Bind events to the button
button.bind("<Button-1>", on_left_click)  # Left click
button.bind("<Button-3>", on_right_click)  # Right click

# Label to display click messages
label = tk.Label(root, text="Click the button above", font=("Arial", 14))
label.pack(pady=20)

# Run the application
root.mainloop()
