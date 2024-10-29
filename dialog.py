import json
import tkinter as tk
from tkinter import ttk
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
            boxes = json.load(f)
            for box in boxes:
                box_options.append(box["name"])
        self.cmb_box = ttk.Combobox(self, values=box_options)
        self.cmb_box.pack(fill=tk.NONE, expand=False, side=tk.LEFT, anchor=tk.NW)
        self.cmb_quantity = ttk.Combobox(self, values=['1', '2', '3', '4', '5'])
        self.cmb_quantity.current(0)
        self.cmb_quantity.pack(fill=tk.NONE, expand=False, side=tk.LEFT, anchor=tk.NW)
        self.ent_height = EntryDigits(self, width=10)
        self.ent_height.pack(fill=tk.NONE, expand=False, side=tk.LEFT, anchor=tk.NW)



        self.btn_cancel = ttk.Button(self, text="Cancel", command=self.close)
        self.btn_cancel.pack(anchor=tk.SW)
        self.btn_add = ttk.Button(self, text="Add box", command=self.add_box)
        self.btn_add.pack(anchor=tk.SW)


    def close(self):
        self.grab_release()
        self.destroy()

    def add_box(self):
        for quantity in range(int(self.cmb_quantity.get())):
            self.elements.append({'type': 'box', 'name': self.cmb_box.get(), 'width': '550', 'height': self.ent_height.get(),})
        self.refresh()
        self.close()