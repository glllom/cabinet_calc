import tkinter as tk
import json
from tkinter import ttk, Label, IntVar
from tkinter import messagebox

import functions
from functions import *
from classes import *


def redraw(event):
    print("redraw")


def close_window():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

def open_error(message):
    messagebox.showerror(title="Error", message=message)

def new_file():
    if messagebox.askyesno(message="New file?", title="New file?"):
        with open("piece.json", "w") as f:
            json.dump({"height": "", "top_panel": "1",
                       "bottom_panel": "1",
                       "elements": []}, f, indent=4)

def add_shelves():
    window = ShelvesWindow()
    print("next step")

def add_boxes():
    window = BoxesWindow()


def generate_code():
    width = ent_width.get()
    height = ent_height.get()
    if width.isnumeric() and height.isnumeric():
        print(int(width), int(height))
    else:
        open_error("Wrong width or height")
        return
    with open("piece.json", "r") as f:
        data = json.load(f)



root = tk.Tk()
root.option_add("*tearOff", False)
root.geometry("1000x750+50+10")
root.resizable(False, False)
root.title("G-code generator")
icon = tk.PhotoImage(file ="res/images/icon/favicon.png")
root.iconphoto(False, icon)

main_menu = tk.Menu()
file_menu = tk.Menu()
macros_menu = tk.Menu()
main_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Save")
file_menu.add_command(label="Open")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=close_window)

macros_menu.add_command(label="Create new macros")

main_menu.add_cascade(label="File", menu=file_menu)
main_menu.add_cascade(label="Macros", menu=macros_menu)
main_menu.add_cascade(label="View")

root.config(menu=main_menu)


frm_sizes = ttk.Frame(borderwidth=1, relief=tk.GROOVE, padding=[5, 5])
lbl_width = Label(frm_sizes, text="Width: ")
lbl_width.grid(row=0, column=0)
ent_width = tk.Entry(frm_sizes)
ent_width.grid(row=0, column=1)
lbl_height = Label(frm_sizes, text="Height: ")
lbl_height.grid(row=1, column=0)
ent_height = tk.Entry(frm_sizes)
ent_height.grid(row=1, column=1)


frm_top_panel = ttk.LabelFrame(frm_sizes, text="Top Panel", padding=[2])
frm_top_panel.grid(row=0, column=2, rowspan=2, padx=10, pady=10, sticky=tk.NSEW)

frm_bottom_panel = ttk.LabelFrame(frm_sizes, text="Bottom Panel", padding=[2])
frm_bottom_panel.grid(row=0, column=3, rowspan=2, pady=10, sticky=tk.NSEW)

top_panel = IntVar(value=1)
bottom_panel = IntVar(value=1)
rbtn_top_panel_1 = ttk.Radiobutton(frm_top_panel, text="Inside", variable=top_panel, value=1, width=8)
rbtn_top_panel_2 = ttk.Radiobutton(frm_top_panel, text="Outside", variable=top_panel, value=2, width=8)
rbtn_top_panel_1.grid(row=0, column=0)
rbtn_top_panel_2.grid(row=1, column=0)
rbtn_bottom_panel_1 = ttk.Radiobutton(frm_bottom_panel, text="Inside", variable=bottom_panel, value=1, width=8)
rbtn_bottom_panel_2 = ttk.Radiobutton(frm_bottom_panel, text="Outside", variable=bottom_panel, value=2, width=8)
rbtn_bottom_panel_1.grid(row=0, column=0)
rbtn_bottom_panel_2.grid(row=1, column=0)
frm_sizes.pack(anchor=tk.N, padx=5, pady=5)

frm_main = ttk.Frame(borderwidth=0)
frm_main.pack(fill=tk.BOTH, expand=True, anchor=tk.N)
for c in range(2): frm_main.columnconfigure(index=c, weight=2)


btn_add_shelves = ttk.Button(frm_main, text="Add Shelves", command=add_shelves)
btn_add_boxes = ttk.Button(frm_main, text="Add Boxes", command=add_boxes)


btn_add_shelves.pack()
btn_add_boxes.pack()
canvas = tk.Canvas(bg="white", master=frm_main, width=300, height=540, borderwidth=0)
canvas.place(anchor=tk.NE, relx=1, rely=0, x=-5)
canvas.update()




btn_generate = ttk.Button(root, text="Generate", command=generate_code)
btn_generate.pack()

root.mainloop()

