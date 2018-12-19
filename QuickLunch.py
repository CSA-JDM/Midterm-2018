# Jacob Meadows
# Computer Programming, 6th Period
# 19 December 2018
"""
QuickLunch.py - the Computer Programming, 6th Period's midterm assigned program

Copyright (C) 2018 Jacob Meadows

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
import tkinter as tk
from tkinter import ttk


class App(tk.Frame):
    def __init__(self, master):
        self.master = master
        self.master.config(width=1280, height=720)
        self.master.title("QuickLunch")
        super().__init__(self.master, width=1280, height=720)
        self.pack()
        self.grid_propagate(0)

        self.widgets = dict()
        self.vars = dict()

        self.widgets["main_menu"] = tk.Menu(self.master)
        self.master.config(menu=self.widgets["main_menu"])

        self.widgets["file_menu"] = tk.Menu(self.widgets["main_menu"], tearoff=0)
        self.widgets["file_menu"].add_command(label="Exit", command=self.quit)
        self.widgets["main_menu"].add_cascade(label="File", menu=self.widgets["file_menu"])

        self.widgets["help_menu"] = tk.Menu(self.widgets["main_menu"], tearoff=0)
        self.widgets["help_menu"].add_command(label="Instructions", command=self.instructions_command)
        self.widgets["help_menu"].add_command(label="About", command=self.about_command)
        self.widgets["main_menu"].add_cascade(label="Help", menu=self.widgets["help_menu"])

        self.widgets["drinks_label"] = tk.Label(self, text="Drinks")
        self.widgets["drinks_label"].grid(row=0, column=0, sticky="w", pady=10)

        self.vars["drinks_dict"] = {"Soda": 1.00, "Tea": 1.00, "Milk": 1.75, "Juice": 1.25, "Bottled Water": 1.00}
        self.vars["drinks_str_var"] = tk.StringVar(value="None")
        self.widgets["drinks_window"] = tk.PanedWindow(self, orient="vertical", relief="sunken")
        self.widgets["drinks_window"].grid(row=1, column=0, sticky="nw", padx=10)

        drink_num = 0
        for drink in self.vars["drinks_dict"]:
            self.widgets[f"{drink}_radio_button"] = tk.Radiobutton(
                self.widgets["drinks_window"], text=drink, value=drink,
                variable=self.vars["drinks_str_var"]
            )
            self.widgets["drinks_window"].add(self.widgets[f"{drink}_radio_button"], sticky="w")
            drink_num += 1

        self.widgets["entrees_label"] = tk.Label(self, text="Entrees")
        self.widgets["entrees_label"].grid(row=0, column=1, sticky="w")

        self.vars["entrees_dict"] = {"Sandwich": 3.00, "Pizza": 4.00, "Chicken Nuggets": 3.75, "Chicken": 4.00,
                                     "Tofu": 15.00, "Clam Chowder (Gluten/Soy/Shellfish Free)": 20.00}
        self.vars["entrees_str_var"] = tk.StringVar(value=list(self.vars["entrees_dict"].keys()))
        self.widgets["entrees_listbox"] = tk.Listbox(self, listvariable=self.vars["entrees_str_var"], width=40,
                                                     height=9)
        self.widgets["entrees_listbox"].grid(row=1, column=1, sticky="n")

        self.widgets["day_spinbox"] = tk.Spinbox(self, values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                                                 state="readonly", width=15)
        self.widgets["day_spinbox"].grid(row=2, column=0, sticky="w", pady=10)

        self.widgets["payment_combobox"] = tk.ttk.Combobox(self, values=["Credit", "Check", "Cash"], state="readonly",
                                                           width=13)
        self.widgets["payment_combobox"].grid(row=3, column=0, sticky="w")

        self.widgets["employee_frame"] = tk.Frame(self)
        self.widgets["employee_frame"].grid(row=3, column=1, sticky="w")

        self.widgets["employee_label"] = tk.Label(self.widgets["employee_frame"], text="Employee ID     ")
        self.widgets["employee_label"].grid(row=0, column=0, sticky="w")

        self.widgets["employee_entry"] = tk.Entry(self.widgets["employee_frame"])
        self.widgets["employee_entry"].grid(row=0, column=1)

        self.widgets["calculate_button"] = tk.Button(self, text="CALCULATE", command=self.calculate_command)
        self.widgets["calculate_button"].grid(row=4, column=0, sticky="w", pady=10)

        self.widgets["price_label"] = tk.Label(self, text="Price: $0.00")
        self.widgets["price_label"].grid(row=4, column=1, sticky="w")

        self.widgets["checkout_button"] = tk.Button(self, text="CHECKOUT", command=self.checkout_command)
        self.widgets["checkout_button"].grid(row=5, column=0, sticky="w")

        self.widgets["program_progress_bar"] = tk.ttk.Progressbar(self, maximum=4, orient="vertical", length=210)
        self.widgets["program_progress_bar"].grid(row=1, column=2, rowspan=4, sticky="n", padx=10)

        self.after(1, self.widget_loop)

    def widget_loop(self):
        progress_bar_value = 0
        if self.widgets["price_label"].cget("text") != "Price: $0.00":
            progress_bar_value += 1
        if self.vars["drinks_str_var"].get() != "None" or self.widgets["entrees_listbox"].curselection() != ():
            progress_bar_value += 1
        if self.widgets["employee_entry"].get() != "":
            progress_bar_value += 1
        if self.widgets["payment_combobox"].get() != "":
            progress_bar_value += 1
        self.widgets["program_progress_bar"].config(value=progress_bar_value)
        self.after(1, self.widget_loop)

    def instructions_command(self):
        pass

    def about_command(self):
        pass

    def calculate_command(self):
        total_price = 0.00
        if self.vars["drinks_str_var"].get() != "None":
            total_price += self.vars["drinks_dict"][self.vars["drinks_str_var"].get()]
        if self.widgets["entrees_listbox"].curselection() != ():
            total_price += self.vars["entrees_dict"][self.widgets["entrees_listbox"].get([self.widgets["entrees_listbox"].curselection()])]
        self.widgets["price_label"].config(text=f"Price: ${total_price}")

    def checkout_command(self):
        try:
            quicklunch_file_txt = open("quicklunch_file.txt", "a")
        except FileNotFoundError:
            quicklunch_file_txt = open("quicklunch_file.txt", "w")
        quicklunch_file_txt.write(
            self.widgets["employee_entry"].get() + self.widgets["price_label"].cget("text").split("$")[1] + "\n"
        )


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
