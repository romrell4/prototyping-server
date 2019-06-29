import tkinter as tk
import os
import shutil

class GUI:

    def __init__(self):
        master = tk.Tk()

        self.widget_filenames = []
        self.widget_type_filenames = []

        master.title("Prototyping")

        tk.Label(master, text = "Welcome to our Prototyping System!").grid(row = 0, column = 0, columnspan = 2)

        # left area
        left = tk.Frame(master)
        left.grid(row = 1, column = 0, sticky = "nsew")

        tk.Label(left, text = "Widgets:").pack()

        self.widget_listbox = tk.Listbox(left)
        self.widget_listbox.pack()
        self.load_widgets_listbox()
        self.widget_listbox.bind("<<ListboxSelect>>", self.on_widget_selected)

        tk.Label(left, text = "Add New Widget:").pack()

        self.new_widget_name = tk.Entry(left)
        self.new_widget_name.pack()

        self.widget_type_listbox = tk.Listbox(left)
        self.widget_type_listbox.pack()
        self.load_widget_type_listbox()

        tk.Button(left, text = "Add", bg = "black", command = self.add_widget_pressed).pack()

        # right area
        right = tk.Frame(master, width = 500, height = 400)
        right.grid(row = 1, column = 1)

        tk.Label(right, text = "Code:").pack()

        self.code_text = tk.Text(right, borderwidth = 1, relief = "solid")
        self.code_text.pack()

        right_buttons = tk.Frame(right)
        tk.Button(right_buttons, text = "Save").grid(row = 0, column = 0)
        tk.Button(right_buttons, text = "Cancel").grid(row = 0, column = 1)
        right_buttons.pack()

        master.grid_rowconfigure(1, weight = 1)
        master.grid_columnconfigure(1, weight = 1)

        master.mainloop()

    def load_widgets_listbox(self):
        self.widget_filenames = get_filenames("widgets")
        self.widget_listbox.delete(0, tk.END)
        for filename in self.widget_filenames:
            self.widget_listbox.insert(tk.END, filename.replace(".py", ""))

    def load_widget_type_listbox(self):
        self.widget_type_filenames = get_filenames("templates")
        self.widget_type_listbox.delete(0, tk.END)
        for filename in self.widget_type_filenames:
            self.widget_type_listbox.insert(tk.END, filename.replace(".py", ""))

    def add_widget_pressed(self):
        new_widget_name = self.new_widget_name.get().strip()
        selected_index = self.widget_type_listbox.curselection()
        if len(new_widget_name) == 0 or len(selected_index) == 0:
            print("Invalid")
            return

        shutil.copy2("templates/{}".format(self.widget_type_filenames[selected_index[0]]), "widgets/{}.py".format(self.new_widget_name.get()))
        self.load_widgets_listbox()

    def on_widget_selected(self, event):
        try:
            with open("widgets/{}".format(self.widget_filenames[int(event.widget.curselection()[0])])) as f:
                code = f.read()

            self.code_text.delete("1.0", tk.END)
            self.code_text.insert(tk.END, code)
        except IndexError as e:
            print(e)

def get_filenames(dir_name):
    return sorted([file for file in os.listdir(dir_name) if not file.startswith("__")])