import json
import tkinter as tk
from tkinter import ttk


class BoxesWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()

        self.title("Add box/boxes")
        self.geometry("250x200")

        box_options = []
        with open("box_types.json", "r") as f:
            boxes = json.load(f)
            for box in boxes:
                box_options.append(box["name"])
        self.cmb_box = ttk.Combobox(self, values=box_options)
        self.cmb_box.pack(fill=tk.NONE, expand=False, side=tk.LEFT, anchor=tk.NW)
        self.cmb_quantity = ttk.Combobox(self, values=['1', '2', '3', '4', '5'])
        self.cmb_quantity.pack(fill=tk.NONE, expand=False, side=tk.LEFT, anchor=tk.NW)

        self.button = ttk.Button(self, text="Cancel", command=self.close)
        self.button.pack(anchor="center", expand=1)

    def close(self):
        self.grab_release()
        self.destroy()