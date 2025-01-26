import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import shutil

class ResourceManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KO's Resource Manager")
        #maximize window
        self.root.state('zoomed')
        self.root.configure(bg="black")

        # Directories
        self.tv_logo_directory = "./resources/tv_logo"
        self.scoreboard_directory = "./resources/scoreboards"
        self.destination_directory = "C:\\FC 25 Live Editor\\mods\\legacy"

        # Variables
        self.tv_var = tk.IntVar(value=-1)
        self.scoreboard_var = tk.IntVar(value=-1)

        # Widgets
        self.setup_ui()

    def setup_ui(self):
        self.create_top_frame()
        self.create_middle_frame()
        self.create_apply_button()

        self.tv_var.trace("w", self.enable_apply_button)
        self.scoreboard_var.trace("w", self.enable_apply_button)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_top_frame(self):
        self.top_frame = tk.Frame(self.root, bg="black")
        self.top_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

        # Top icons
        self.add_reset_icon()
        self.add_program_icons()

        # Separator
        separator = ttk.Separator(self.root, orient='horizontal')
        separator.pack(fill='x', padx=20, pady=5)

    def add_reset_icon(self):
        icon_path = os.path.join("./assets", "reset.png")
        img = Image.open(icon_path).resize((40, 40))
        img_tk = ImageTk.PhotoImage(img)
        label = tk.Label(self.top_frame, image=img_tk, bg="black")
        label.image = img_tk
        label.pack(side=tk.LEFT, padx=5)
        label.bind("<Button-1>", lambda e: self.reset())

    def add_program_icons(self):
        icons = {
            "EA": ("./assets/ea.png", r"C:\\Program Files\\Electronic Arts\\EA Desktop\\EA Desktop\\EALauncher.exe"),
            "steam": ("./assets/steam.png", r"C:\\Program Files (x86)\\Steam\\Steam.exe"),
            "mm": ("./assets/mm.png", r""),
            "le": ("./assets/le.png", r""),
        }

        for _, (path, exe) in icons.items():
            img = Image.open(path).resize((40, 40))
            img_tk = ImageTk.PhotoImage(img)
            label = tk.Label(self.top_frame, image=img_tk, bg="black")
            label.image = img_tk
            label.pack(side=tk.LEFT, padx=5)
            label.bind("<Button-1>", lambda e, exe_path=exe: self.open_exe(exe_path))

    def create_middle_frame(self):
        self.middle_frame = tk.Frame(self.root, bg="black")
        self.middle_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.create_left_frame()
        self.create_right_frame()

    def create_left_frame(self):
        left_frame = tk.Frame(self.middle_frame, bg="black")
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        self.add_scrollable_options(left_frame)

    def add_scrollable_options(self, parent):
        canvas = tk.Canvas(parent, bg="black", highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.Y, expand=True)

        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        frame = tk.Frame(canvas, bg="black")
        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        self.add_tv_logo_options(frame)
        self.add_scoreboard_options(frame)

        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def add_tv_logo_options(self, parent):
        tv_label = tk.Label(parent, text="TV Logos", fg="white", bg="black", anchor="w")
        tv_label.pack(fill=tk.X)

        self.tv_options = [name for name in os.listdir(self.tv_logo_directory)
                           if os.path.isdir(os.path.join(self.tv_logo_directory, name))]

        for index, option in enumerate(self.tv_options):
            radio = tk.Radiobutton(parent, text=option, variable=self.tv_var, value=index,
                                   bg="black", fg="white", selectcolor="black", command=self.on_tv_select)
            radio.pack(anchor="w")

    def add_scoreboard_options(self, parent):
        separator = ttk.Separator(parent, orient='horizontal')
        separator.pack(fill='x', pady=10)

        scoreboard_label = tk.Label(parent, text="Scoreboards", fg="white", bg="black", anchor="w")
        scoreboard_label.pack(fill=tk.X, pady=(10, 0))

        self.scoreboard_options = [name for name in os.listdir(self.scoreboard_directory)
                                    if os.path.isdir(os.path.join(self.scoreboard_directory, name))]

        for index, option in enumerate(self.scoreboard_options):
            radio = tk.Radiobutton(parent, text=option, variable=self.scoreboard_var, value=index,
                                   bg="black", fg="white", selectcolor="black", command=self.on_scoreboard_select)
            radio.pack(anchor="w")

    def create_right_frame(self):
        right_frame = tk.Frame(self.middle_frame, bg="black")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.preview1 = tk.Label(right_frame, text="[TV Logo Preview]", fg="white", bg="black")
        self.preview1.pack(pady=5)

        separator = ttk.Separator(right_frame, orient='horizontal')
        separator.pack(fill='x', pady=10)

        self.preview2 = tk.Label(right_frame, text="[Scoreboard Preview]", fg="white", bg="black")
        self.preview2.pack(pady=5)

    def create_apply_button(self):
        self.apply_button = tk.Button(self.root, text="Apply", command=self.on_apply, state=tk.DISABLED)
        self.apply_button.pack(side=tk.BOTTOM, pady=10)

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

    def on_scoreboard_select(self):
        self.update_preview(self.scoreboard_directory, self.scoreboard_options[self.scoreboard_var.get()], self.preview2)

    def update_preview(self, base_directory, selected_option, preview_label):
        try:
            img_path = os.path.join(base_directory, selected_option, "preview.jpg")
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
