import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import shutil
import os

class GUI:
    def __init__(self, reload_widget_func):
        self.reload_widget_func = reload_widget_func

        master = tk.Tk()

        self.widget_filenames = []
        self.widget_type_filenames = []

        master.title("Prototyping")

        tk.Label(master, text = "Welcome to our Prototyping System!").grid(row = 0, column = 0, columnspan = 2)

        # left area
        left = tk.Frame(master)
        left.grid(row = 1, column = 0, sticky = "nsew")

        tk.Label(left, text = "Widgets:").pack()

        self.widget_listbox = tk.Listbox(left, exportselection = False)
        self.widget_listbox.pack()
        self.load_widgets_listbox()
        self.widget_listbox.bind("<<ListboxSelect>>", self.on_widget_selected)

        new_widget_label = tk.Label(left, text = "Add New Widget:")

        self.new_widget_name = tk.Entry(left)

        self.widget_type_listbox = tk.Listbox(left)
        self.load_widget_type_listbox()

        add_button = tk.Button(left, text = "Add", command = self.add_widget_pressed)

        add_button.pack(side = tk.BOTTOM)
        self.widget_type_listbox.pack(side = tk.BOTTOM)
        self.new_widget_name.pack(side = tk.BOTTOM)
        new_widget_label.pack(side = tk.BOTTOM)

        # right area
        right = tk.Frame(master)
        right.grid(row = 1, column = 1)

        tk.Label(right, text = "Code:").pack()

        self.code_text = ScrolledText(right, borderwidth = 1, relief = "solid", width = 100, height = 40)
        self.code_text.pack()

        tk.Button(right, text = "Save", command = self.save_pressed).pack()

        master.grid_rowconfigure(1, weight = 1)
        master.grid_columnconfigure(1, weight = 1)

        master.mainloop()

    def load_widgets_listbox(self):
        self.widget_filenames = load_listbox(self.widget_listbox, "widgets")

    def load_widget_type_listbox(self):
        self.widget_type_filenames = load_listbox(self.widget_type_listbox, "templates")

    def add_widget_pressed(self):
        new_widget_name = self.new_widget_name.get().strip()
        selected_index = self.widget_type_listbox.curselection()
        if len(new_widget_name) == 0 or len(selected_index) == 0:
            print("Invalid")
            return

        shutil.copy2("templates/{}".format(self.widget_type_filenames[selected_index[0]]), "widgets/{}.py".format(self.new_widget_name.get()))
        self.load_widgets_listbox()

    def save_pressed(self):
        selected_index = self.widget_listbox.curselection()
        if len(selected_index) == 0:
            print("Invalid")
            return

        filename = self.widget_filenames[selected_index[0]]
        with open("widgets/{}".format(filename), "w") as f:
            f.write(self.code_text.get("1.0", tk.END))

        self.reload_widget_func(filename.replace(".py", ""))

    def on_widget_selected(self, event):
        try:
            with open("widgets/{}".format(self.widget_filenames[int(event.widget.curselection()[0])])) as f:
                code = f.read()

            self.code_text.delete("1.0", tk.END)
            self.code_text.insert(tk.END, code)
        except IndexError as e:
            print(e)

def load_listbox(listbox, directory):
    filenames = get_filenames(directory)
    listbox.delete(0, tk.END)
    for filename in filenames:
        listbox.insert(tk.END, filename.replace(".py", ""))
    return filenames

def get_filenames(dir_name):
    return sorted([file for file in os.listdir(dir_name) if not file.startswith("__")])