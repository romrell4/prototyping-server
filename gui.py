import tkinter as tk
import os

class GUI:

    def __init__(self):
        self.files = self.get_files()

        master = tk.Tk()
        master.title("Prototyping")

        tk.Label(master, text = "Welcome to our Prototyping System!").grid(row = 0, column = 0, columnspan = 2)

        # left area
        left = tk.Frame(master)
        left.grid(row = 1, column = 0, sticky = "nsew")

        tk.Label(left, text = "Widgets:").pack()

        listbox = tk.Listbox(left)
        listbox.pack()
        for file in self.files:
            listbox.insert(tk.END, file.rstrip(".py"))

        listbox.bind("<<ListboxSelect>>", self.on_listbox_selected)

        tk.Button(left, text = "Add Widget", bg = "black", command = lambda: print("hello")).pack()

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





        # tk.mainloop()

    def get_files(self):
        return [file for file in os.listdir("widgets") if not file.startswith("__")]

    def on_listbox_selected(self, event):
        file = self.files[int(event.widget.curselection()[0])]
        with open("widgets/{}".format(file)) as f:
            code = f.read()

        self.code_text.delete("1.0", tk.END)
        self.code_text.insert(tk.END, code)