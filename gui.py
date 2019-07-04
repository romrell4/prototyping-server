import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import shutil
import utils

class GUI:
    def __init__(self):
        master = tk.Tk()

        self.widget_filenames = []
        self.widget_type_filenames = []

        master.title("Prototyping")

        tk.Label(master, text = "Welcome to our Prototyping System!").grid(row = 0, column = 0, columnspan = 2)

        # top left area
        left = tk.Frame(master)
        left.grid(row = 1, column = 0, sticky = "nsew")

        tk.Label(left, text = "Widgets:").pack()

        self.widget_listbox = tk.Listbox(left, exportselection = False)
        self.widget_listbox.pack()
        self.load_widgets_listbox()
        self.widget_listbox.bind("<<ListboxSelect>>", self.on_widget_selected)

        # bottom left area

        divider = tk.Frame(left, height = 1, bg = "black")

        new_widget_label = tk.Label(left, text = "Add New Widget:")

        self.new_widget_name = tk.Entry(left)

        self.widget_type_listbox = tk.Listbox(left)
        self.load_widget_type_listbox()

        add_button = tk.Button(left, text = "Add", command = self.add_widget_pressed)

        add_button.pack(side = tk.BOTTOM)
        self.widget_type_listbox.pack(side = tk.BOTTOM)
        self.new_widget_name.pack(side = tk.BOTTOM)
        new_widget_label.pack(side = tk.BOTTOM)
        divider.pack(side = tk.BOTTOM, fill = "x")

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
        # Strip whitespace from the widget name to keep it clean
        new_widget_name = self.new_widget_name.get().strip()
        selected_index = get_selected_index(self.widget_type_listbox)

        # To add a widget, you have to have a valid name and template
        if new_widget_name == "" or selected_index is None:
            print("Invalid")
            return

        # Copy the template into the widgets with the new filename
        shutil.copy2("templates/{}".format(self.widget_type_filenames[selected_index]), "widgets/{}.py".format(self.new_widget_name.get()))

        # Reload the widgets
        self.load_widgets_listbox()

    def save_pressed(self):
        selected_index = get_selected_index(self.widget_listbox)

        # To save, you have to have a widget selected
        if selected_index is None:
            print("Invalid")
            return

        # Trim newlines from the code to keep it clean
        code = self.code_text.get("1.0", tk.END).rstrip("\n")

        # Rewrite the file with the new code
        with open("widgets/{}".format(self.widget_filenames[selected_index]), "w") as f:
            f.write(code)

    def on_widget_selected(self, event):
        selected_index = get_selected_index(self.widget_listbox)

        if selected_index is None:
            print("Invalid")
            return

        # Read the code from the selected widget's file
        with open("widgets/{}".format(self.widget_filenames[selected_index])) as f:
            code = f.read()

        # Write the code out to the text field
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert(tk.END, code)

def load_listbox(listbox, directory):
    filenames = utils.get_filenames(directory)

    # Clear the listbox, and insert an entry for each file in the directory
    listbox.delete(0, tk.END)
    for filename in filenames:
        listbox.insert(tk.END, filename.replace(".py", ""))
    return filenames

def get_selected_index(listbox):
    # curselection() is a tuple with all of the selections (because of multi-select). If the length is not zero, there is a valid selection
    return next(iter(listbox.curselection()), None)
