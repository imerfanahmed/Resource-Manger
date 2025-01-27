import tkinter as tk
from tkinter import ttk, messagebox,filedialog, StringVar, OptionMenu
from PIL import Image, ImageTk
import os
import shutil
import json

class ResourceManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KO's Resource Manager")
        #maximize window
        self.root.geometry("1100x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#F0F0F0")

        # Directories
        self.tv_logo_directory = "./resources/tv_logo"
        self.scoreboard_directory = "./resources/scoreboards"
        self.destination_directory = "C:\\FC 25 Live Editor\\mods\\legacy"

        # Variables
        self.tv_var = tk.IntVar(value=-1)
        self.scoreboard_var = tk.IntVar(value=-1)
        self.load_config()
        # Widgets
        self.setup_ui()
        
        

    def load_config(self):
        with open('./config.json', 'r') as f:
            self.config = json.load(f)

    def save_config(self):
        with open('config.json', 'w') as f:
            json.dump(self.config, f, indent=4)
            
    def setup_ui(self):
        self.create_top_frame()
        self.create_middle_frame()
        # self.create_apply_button()

        self.tv_var.trace("w", self.enable_apply_button)
        self.scoreboard_var.trace("w", self.enable_apply_button)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_top_frame(self):
        self.top_frame = tk.Frame(self.root, bg="#F0F0F0")
        self.top_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

        # Top icons
        # self.add_reset_icon()
        self.add_program_icons()
        
        self.create_apply_button()

        # Separator
        separator = ttk.Separator(self.root, orient='horizontal')
        separator.pack(fill='x', padx=20, pady=5)

    def add_reset_icon(self):
        icon_path = os.path.join("./assets", "reset.png")
        img = Image.open(icon_path).resize((40, 40))
        img_tk = ImageTk.PhotoImage(img)
        label = tk.Label(self.top_frame, image=img_tk, bg="#F0F0F0")
        label.image = img_tk
        label.pack(side=tk.LEFT, padx=5)
        label.bind("<Button-1>", lambda e: self.reset())

    def add_program_icons(self):
        # Clear existing icons
        for widget in self.top_frame.winfo_children():
            widget.destroy()
        
        self.add_reset_icon()

        for key, value in self.config.items():
            icon_path, exe_path = value["icon"], value["path"]
            img = Image.open(icon_path).resize((40, 40))
            img_tk = ImageTk.PhotoImage(img)
            label = tk.Label(self.top_frame, image=img_tk, bg="#F0F0F0")
            label.image = img_tk
            label.pack(side=tk.LEFT, padx=5)
            label.bind("<Button-1>", lambda e, exe_path=exe_path: self.open_exe(exe_path))
            label.bind("<Button-3>", lambda e, key=key: self.select_executable(key))
            
    def select_executable(self, key):
        file_path = filedialog.askopenfilename(title="Select Executable", filetypes=[("Executable Files", "*.exe")])
        if file_path:
            self.config[key]["path"] = file_path
            self.save_config()
            self.load_config()
            self.add_program_icons()
            self.create_apply_button()
            
    def create_middle_frame(self):
        self.middle_frame = tk.Frame(self.root, bg="#F0F0F0")
        self.middle_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.create_left_frame()
        self.create_right_frame()

    def create_left_frame(self):
        left_frame = tk.Frame(self.middle_frame, bg="#F0F0F0")
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        self.add_scrollable_options(left_frame)

    def add_scrollable_options(self, parent):
        canvas = tk.Canvas(parent, bg="#F0F0F0", highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.Y, expand=True)

        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        frame = tk.Frame(canvas, bg="#F0F0F0")
        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        self.add_tv_logo_options(frame)
        self.add_scoreboard_options(frame)

        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def add_tv_logo_options(self, parent):
        tv_label = tk.Label(parent, text="TV Logos", fg="black", bg="#F0F0F0", anchor="w", font=("Helvetica", 16))
        tv_label.pack(fill=tk.X)

        self.tv_options = [name for name in os.listdir(self.tv_logo_directory)
                           if os.path.isdir(os.path.join(self.tv_logo_directory, name))]

        for index, option in enumerate(self.tv_options):
            radio = tk.Radiobutton(parent, text=option, variable=self.tv_var, value=index,
                                   bg="#F0F0F0", fg="black", selectcolor="#F0F0F0", command=self.on_tv_select)
            radio.pack(anchor="w")

    def add_scoreboard_options(self, parent):
        separator = ttk.Separator(parent, orient='horizontal')
        separator.pack(fill='x', pady=10)

        scoreboard_label = tk.Label(parent, text="Scoreboards", fg="black", bg="#F0F0F0", anchor="w",font=("Helvetica", 16))
        scoreboard_label.pack(fill=tk.X, pady=(10, 0))

        self.scoreboard_options = [name for name in os.listdir(self.scoreboard_directory)
                                    if os.path.isdir(os.path.join(self.scoreboard_directory, name))]

        for index, option in enumerate(self.scoreboard_options):
            radio = tk.Radiobutton(parent, text=option, variable=self.scoreboard_var, value=index,
                                   bg="#F0F0F0", fg="black", selectcolor="#F0F0F0", command=self.on_scoreboard_select)
            radio.pack(anchor="w")

    def create_right_frame(self):
        right_frame = tk.Frame(self.middle_frame, bg="#F0F0F0")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Create a canvas and a scrollbar
        canvas = tk.Canvas(right_frame, bg="#F0F0F0")
        scrollbar = tk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#F0F0F0")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        title1 = tk.Label(scrollable_frame, text="TV Logo Preview", fg="black", bg="#F0F0F0", font=("Helvetica", 16))
        title1.pack(pady=5)

        self.preview1 = tk.Label(scrollable_frame, text="[TV Logo Preview]", fg="black", bg="#F0F0F0")
        self.preview1.pack(pady=5)

        separator = ttk.Separator(scrollable_frame, orient='horizontal')
        separator.pack(fill='x', pady=10)
        title2 = tk.Label(scrollable_frame, text="Scoreboard Preview", fg="black", bg="#F0F0F0", font=("Helvetica", 16))
        title2.pack(pady=5)
        self.preview2 = tk.Label(scrollable_frame, text="[Scoreboard Preview]", fg="black", bg="#F0F0F0")
        self.preview2.pack(pady=5)

    def create_apply_button(self):
        self.apply_button = tk.Button(
            self.top_frame, 
            text="Apply", 
            command=self.on_apply, 
            state=tk.DISABLED,
            font=("Helvetica", 14, "bold"),  # Larger font
            bg="#F0F0F0",  # Background color
            fg="black"  # Foreground (text) color
        )
        self.apply_button.pack(side=tk.RIGHT, padx=10)

    def enable_apply_button(self, *args):
        if self.tv_var.get() >= 0 or self.scoreboard_var.get() >= 0:
            self.apply_button.config(state=tk.NORMAL)
        else:
            self.apply_button.config(state=tk.DISABLED)

    def reset(self):
        try:
            shutil.rmtree(os.path.join(self.destination_directory, "data", "ui", "game"))
        except FileNotFoundError:
            pass
        messagebox.showinfo("Success", "Reset successful")

    def on_apply(self):
        if self.tv_var.get() >= 0:
            self.apply_resource(self.tv_logo_directory, self.tv_options[self.tv_var.get()])

        if self.scoreboard_var.get() >= 0:
            self.apply_resource(self.scoreboard_directory, self.scoreboard_options[self.scoreboard_var.get()])

    def apply_resource(self, base_directory, selected_option):
        source = os.path.join(base_directory, selected_option, "data")
        destination = os.path.join(self.destination_directory, "data")
        os.makedirs(destination, exist_ok=True)
        shutil.copytree(source, destination, dirs_exist_ok=True)
        messagebox.showinfo("Success", f"{selected_option} applied successfully!")

    def on_tv_select(self):
        self.update_preview(self.tv_logo_directory, self.tv_options[self.tv_var.get()], self.preview1)

# ...existing code...

    def on_scoreboard_select(self):
        selected_option = self.scoreboard_options[self.scoreboard_var.get()]
        base_directory = os.path.join(self.scoreboard_directory, selected_option)
        preview_path = os.path.join(base_directory, "preview.jpg")
        
        if not os.path.exists(preview_path):
            self.show_variation_select(base_directory)
        else:
            self.update_preview(self.scoreboard_directory, selected_option, self.preview2)

    def show_variation_select(self, base_directory):
        """Display a separate window for variation selection."""
        variations = [d for d in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, d))]
        if variations:
            # Create a modal window
            variation_window = tk.Toplevel(self.root)
            variation_window.title("Select Variation")
            variation_window.geometry("300x200")
            variation_window.resizable(False, False)
            variation_window.configure(bg="#F0F0F0")

            tk.Label(variation_window, text="Choose a Variation:", font=("Helvetica", 14), bg="#F0F0F0").pack(pady=10)

            # Create a dropdown for variations
            self.variation_var = StringVar(variation_window)
            self.variation_var.set(variations[0])  # Set the default variation
            variation_menu = OptionMenu(variation_window, self.variation_var, *variations)
            variation_menu.pack(pady=5)

            # Confirm button
            confirm_button = tk.Button(
                variation_window, 
                text="Confirm", 
                command=lambda: self.on_variation_select(base_directory, variation_window),
                font=("Helvetica", 12),
                bg="#4CAF50",
                fg="white"
            )
            confirm_button.pack(pady=10)
        else:
            messagebox.showerror("Error", "No variations found.")

    def on_variation_select(self, base_directory, variation_window):
        """Handle variation selection and update preview."""
        selected_variation = self.variation_var.get()
        variation_path = os.path.join(base_directory, selected_variation)
        preview_path = os.path.join(variation_path, "preview.jpg")

        # Update preview
        if os.path.exists(preview_path):
            self.update_preview(variation_path, "preview.jpg", self.preview2)
        else:
            messagebox.showerror("Error", "Preview image not found for the selected variation.")
        
        variation_window.destroy()  # Close the variation selection window

    def update_preview(self, base_directory, selected_option, preview_label):
        try:
            img_path = os.path.join(base_directory, selected_option)
            print(img_path)
            if os.path.isdir(img_path):
                img_path = os.path.join(img_path, "preview.jpg")
            else:
                img_path = os.path.join(base_directory, selected_option)
            img = Image.open(img_path)
            img_tk = ImageTk.PhotoImage(img)
            preview_label.config(image=img_tk)
            preview_label.image = img_tk
        except Exception as e:
            messagebox.showerror("Error", f"Could not load preview image: {e}")


    def open_exe(self, file_path):
        os.startfile(file_path)

    def on_close(self):
        self.reset()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ResourceManagerApp(root)
    root.mainloop()
