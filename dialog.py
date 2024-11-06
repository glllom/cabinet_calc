import json
import tkinter as tk
from tkinter import ttk
from tkinter.constants import GROOVE

from classes import EntryDigits


class BoxesWindow(tk.Toplevel):
    def __init__(self, parent, refresh, elements):
        super().__init__()
        self.elements = elements
        self.title("Add box/boxes")
        self.geometry("650x200")
        self.refresh = refresh

        box_options = []
        with open("box_types.json", "r") as f:
            self.boxes = json.load(f)
            box_options.extend(iter(self.boxes.keys()))

        self.lbl_name = ttk.Label(self, text="Name")
        self.lbl_name.grid(column=0, row=0)
        self.cmb_box = ttk.Combobox(self, values=box_options)
        self.cmb_box.bind('<<ComboboxSelected>>', self.update_depth_options)
        self.cmb_box.grid(column=0, row=2)
        self.lbl_quantity = ttk.Label(self,text="Quantity")
        self.lbl_quantity.grid(column=1, row=0)
        self.cmb_quantity = ttk.Combobox(self, values=['1', '2', '3', '4', '5'])
        self.cmb_quantity.current(0)
        self.cmb_quantity.grid(column=1, row=2)
        self.lbl_height = ttk.Label(self, text="Height")
        self.lbl_height.grid(column=2, row=0)
        self.tgl_top_height = tk.Button(self, text="To Top", command=self.toggle_top_height)
        self.tgl_top_height.grid(column=2, row=1)
        self.ent_height = EntryDigits(self, width=10)
        self.ent_height.grid(column=2, row=2)
        self.lbl_depth = ttk.Label(self, text="Depth")
        self.lbl_depth.grid(column=3, row=0)
        self.tgl_depth_auto = tk.Button(self, text="Max", command=self.toggle_box_depth, bg='SystemWindowFrame', fg='SystemHighlightText', relief=tk.SUNKEN)
        self.tgl_depth_auto.grid(column=3, row=1)
        self.cmb_depth = ttk.Combobox(self, values=[], state=tk.DISABLED)
        self.cmb_depth.grid(column=3, row=2)

        self.btn_cancel = ttk.Button(self, text="Cancel", command=self.close)
        self.btn_cancel.grid(column=5, row=5)
        self.btn_add = ttk.Button(self, text="Add", command=self.add_box)
        self.btn_add.grid(column=4, row=5)
    def update_depth_options(self, event):
        self.cmb_depth.delete(0, tk.END)
        self.cmb_depth.config(values=list(self.boxes[self.cmb_box.get()]['holes'].keys()))

    def toggle_top_height(self):
        # print(type(str(self.ent_height.cget('state'))), self.ent_height.cget('state') == 'normal')
        if str(self.ent_height.cget('state')) == 'normal':
            self.ent_height.delete(0, tk.END)
            self.ent_height.config(state=tk.DISABLED)
            self.tgl_top_height.config(bg='SystemWindowFrame', fg='SystemHighlightText', relief=tk.SUNKEN)
        else:
            self.ent_height.config(state=tk.NORMAL)
            self.tgl_top_height.config(bg='SystemButtonFace', fg='SystemButtonText', relief=tk.RAISED)

    def toggle_box_depth(self):
        if str(self.cmb_depth.cget('state')) == 'normal':
            self.cmb_depth.delete(0, tk.END)
            self.cmb_depth.config(state=tk.DISABLED)
            self.tgl_depth_auto.config(bg='SystemWindowFrame', fg='SystemHighlightText', relief=tk.SUNKEN)
        else:
            self.cmb_depth.config(state=tk.NORMAL)
            self.tgl_depth_auto.config(bg='SystemButtonFace', fg='SystemButtonText', relief=tk.RAISED)

    def close(self):
        self.grab_release()
        self.destroy()

    def add_box(self):
        # box = self.cmb_box.get()
        # print(type(box), box)
        if self.cmb_box.get() != "" and self.ent_height.validate():
            for _ in range(int(self.cmb_quantity.get())):
                self.elements.append(
                    {'type': 'box', 'name': self.cmb_box.get(), 'width': '550', 'height': self.ent_height.get(), })
            self.refresh()
            self.close()
