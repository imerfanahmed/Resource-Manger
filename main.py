import tkinter as tk
from tkinter import ttk, messagebox, filedialog, StringVar, OptionMenu
from PIL import Image, ImageTk
import os
import shutil
import json

class ResourceManagerApp:
    def __init__(self, root):
        self.root = root
         # Bind F1 and F2 keys
        self.root.bind('<F1>', self.restore_window)
        self.root.bind('<F2>', self.minimize_window)

        self.root.title("KO's Resource Manager")
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
        self.variation_var = StringVar()

        self.load_config()
        self.setup_ui()

    def restore_window(self, event):
        self.root.deiconify()
    
    def minimize_window(self, event):
        self.root.iconify()
    
    def load_config(self):
        with open('./config.json', 'r') as f:
            self.config = json.load(f)

    def save_config(self):
        with open('config.json', 'w') as f:
            json.dump(self.config, f, indent=4)

    def reset(self):
        try:
            shutil.rmtree(os.path.join(self.destination_directory, "data", "ui", "game"))
        except FileNotFoundError:
            pass
        messagebox.showinfo("Success", "Reset successful")

    def setup_ui(self):
        self.create_top_frame()
        self.create_middle_frame()

        self.tv_var.trace_add(['write'], self.enable_apply_button)
        self.scoreboard_var.trace_add(['write'], self.enable_apply_button)
        self.scoreboard_var.trace_add(['write'], self.update_variation_dropdown)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_top_frame(self):
        self.top_frame = tk.Frame(self.root, bg="#F0F0F0")
        self.top_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

        self.add_program_icons()
        

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
        for widget in self.top_frame.winfo_children():
            widget.destroy()

        self.add_reset_icon()
        self.create_apply_button()
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

    def create_middle_frame(self):
        self.middle_frame = tk.Frame(self.root, bg="#F0F0F0")
        self.middle_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.create_left_frame()
        self.create_right_frame()

    def update_preview(self, base_directory, selected_option, preview_label):
        try:
            # Construct the image path
            img_path = os.path.join(base_directory, selected_option, "preview.jpg")
            
            # Check if the preview image exists
            if not os.path.exists(img_path):
                img_path = os.path.join(base_directory, "preview.jpg")
            
            if os.path.exists(img_path):
                # Load and display the image
                img = Image.open(img_path)  # Resize for better fit
                img_tk = ImageTk.PhotoImage(img)
                preview_label.config(image=img_tk)
                preview_label.image = img_tk
            else:
                # No preview image found
                preview_label.config(text="", image="", compound="none")
        except Exception as e:
            # Handle errors and fallback
            messagebox.showerror("Error", f"Could not load preview image: {e}")
            preview_label.config(text="[No Preview Available]", image="", compound="none")

    def create_left_frame(self):
            left_frame = tk.Frame(self.middle_frame, bg="#F0F0F0")
            left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)
            self.add_scrollable_options(left_frame)

    def add_scrollable_options(self, parent):
        canvas = tk.Canvas(parent, bg="#F0F0F0", highlightthickness=0, width=200)
        canvas.pack(side=tk.LEFT, fill=tk.Y, expand=True)

        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview, bg="black", activebackground="black", troughcolor="black", highlightbackground="black", highlightcolor="black")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=True)

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

        scoreboard_label = tk.Label(parent, text="Scoreboards", fg="black", bg="#F0F0F0", anchor="w", font=("Helvetica", 16))
        scoreboard_label.pack(fill=tk.X, pady=(10, 0))

        self.scoreboard_options = [name for name in os.listdir(self.scoreboard_directory)
                                    if os.path.isdir(os.path.join(self.scoreboard_directory, name))]

        for index, option in enumerate(self.scoreboard_options):
            radio = tk.Radiobutton(parent, text=option, variable=self.scoreboard_var, value=index,
                                   bg="#F0F0F0", fg="black", selectcolor="#F0F0F0", command=self.on_scoreboard_select)
            radio.pack(anchor="w")

    def create_right_frame(self):
        self.right_frame = tk.Frame(self.middle_frame, bg="#F0F0F0")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        title1 = tk.Label(self.right_frame, text="TV Logo Preview", fg="black", bg="#F0F0F0", font=("Helvetica", 16))
        title1.pack(pady=5)

        self.preview1 = tk.Label(self.right_frame, text="[TV Logo Preview]", fg="black", bg="#F0F0F0")
        self.preview1.pack(pady=5)

        separator = ttk.Separator(self.right_frame, orient='horizontal')
        separator.pack(fill='x', pady=10)

        title2 = tk.Label(self.right_frame, text="Scoreboard Preview", fg="black", bg="#F0F0F0", font=("Helvetica", 16))
        title2.pack(pady=5)

        self.preview2 = tk.Label(self.right_frame, text="[Scoreboard Preview]", fg="black", bg="#F0F0F0")
        self.preview2.pack(pady=5)

        self.variation_dropdown = OptionMenu(self.right_frame, self.variation_var, "")
        self.variation_dropdown.pack_forget()
        
        self.variation_var.trace_add(['write'], self.update_scoreboard_preview)
    

    def create_apply_button(self):
        self.apply_button = tk.Button(self.top_frame, text="Apply", command=self.on_apply, state=tk.DISABLED,
                                       font=("Helvetica", 14, "bold"), bg="#F0F0F0", fg="black")
        self.apply_button.pack(side=tk.RIGHT, padx=10)
        
        #message beside apply button
        self.applied_message = tk.Label(self.top_frame, text="", fg="black", bg="#F0F0F0", font=("Helvetica", 12))
        self.applied_message.pack(side=tk.RIGHT, padx=10)

    def enable_apply_button(self, *args):
        if self.tv_var.get() >= 0 or self.scoreboard_var.get() >= 0:
            self.apply_button.config(state=tk.NORMAL)
        else:
            self.apply_button.config(state=tk.DISABLED)

    def update_variation_dropdown(self, *args):
        self.variation_dropdown.pack(pady=10)
        self.variation_dropdown.config(state=tk.NORMAL)
        selected_index = self.scoreboard_var.get()
        if selected_index < 0:
            self.variation_dropdown.pack_forget()
            self.variation_var.set("")
            return

        selected_option = self.scoreboard_options[selected_index]
        base_directory = os.path.join(self.scoreboard_directory, selected_option)
        variations = [d for d in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, d))]

        if variations != ["data"]:
            menu = self.variation_dropdown["menu"]
            menu.delete(0, "end")
            for variation in variations:
                menu.add_command(label=variation, command=lambda v=variation: self.variation_var.set(v))

            self.variation_var.set(variations[0])
            self.variation_dropdown.pack(pady=10)  # Ensure the dropdown is shown
            self.variation_dropdown.config(state=tk.NORMAL)
        else:
            self.variation_dropdown.pack_forget()  # Hide the dropdown if no variations
            self.variation_var.set("")


# ...existing code...

    def update_scoreboard_preview(self, *args):
        selected_index = self.scoreboard_var.get()
        selected_variation = self.variation_var.get()

        if selected_index < 0:
            self.preview2.config(text="[Scoreboard Preview]", image="", compound="none")
            return

        selected_option = self.scoreboard_options[selected_index]
        variation_path = os.path.join(self.scoreboard_directory, selected_option, selected_variation, "preview.jpg")
        # Check if the selected option has variations
        if not selected_variation:
            variations_dir = os.path.join(self.scoreboard_directory, selected_option)
            if os.path.isdir(variations_dir):
                variations = os.listdir(variations_dir)
                if variations:
                    self.variation_var.set(variations[0])  # Set to the first variation
                    variation_path = os.path.join(variations_dir, variations[0], "preview.jpg")

        if os.path.exists(variation_path):
            img = Image.open(variation_path)
            img_tk = ImageTk.PhotoImage(img)
            self.preview2.config(image=img_tk, compound="top")
            self.preview2.image = img_tk
        else:
            self.preview2.config(text="[No Preview Available]", image="", compound="none")
# ...existing code...

    def on_tv_select(self):
        self.update_preview(self.tv_logo_directory, self.tv_options[self.tv_var.get()], self.preview1)

    def on_scoreboard_select(self):
        selected_option = self.scoreboard_options[self.scoreboard_var.get()]
        base_directory = os.path.join(self.scoreboard_directory, selected_option)
        self.update_preview(base_directory, "", self.preview2)

    def on_apply(self):
        if self.tv_var.get() >= 0:
            self.apply_resource(self.tv_logo_directory, self.tv_options[self.tv_var.get()])

        if self.scoreboard_var.get() >= 0:
            selected_option = self.scoreboard_options[self.scoreboard_var.get()]
            selected_variation = self.variation_var.get()
            #if the selected variation is data it means its not a variation
            if selected_variation == "data":
                self.apply_resource(self.scoreboard_directory, selected_option)
            else:
                base_directory = os.path.join(self.scoreboard_directory, selected_option)
                self.apply_resource(base_directory, selected_variation)


    def has_variations(self, base_directory, selected_option):
        #if the selected has no preview image, it has variations
        return not os.path.exists(os.path.join(base_directory, selected_option, "preview.jpg"))
    def apply_resource(self, base_directory, selected_option):
        source = os.path.join(base_directory, selected_option, "data")
        destination = os.path.join(self.destination_directory, "data")
        os.makedirs(destination, exist_ok=True)
        shutil.copytree(source, destination, dirs_exist_ok=True)
        self.applied_message.config(text="Applied Successfully!!",fg="green")

    def open_exe(self, file_path):
        os.startfile(file_path)

    def on_close(self):
        self.reset()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ResourceManagerApp(root)
    root.mainloop()
