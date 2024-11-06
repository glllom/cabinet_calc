import tkinter as tk
import json
from tkinter import ttk, messagebox


class Window(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.resizable(False, False)
        self.grab_set()
        self.frm = ttk.Frame(self, borderwidth=1, relief=tk.GROOVE, padding=[5, 5])
        self.frm.pack(fill=tk.BOTH, expand=1)
        self.btn_add = ttk.Button(self, text="Add", command=self.add_element)
        self.btn_add.pack(anchor=tk.E, expand=1)

    def add_element(self):
        print(f"{self} added")
        self.destroy()

class ShelvesWindow(Window):
    def __init__(self):
        super().__init__()
        self.title('Shelves')
        self.geometry('400x400')

        self.options = [str(num) for num in range(1, 6)]
        self.quantity = ttk.Combobox(self.frm, values=self.options, justify='left', state='readonly')
        self.quantity.set("1")
        self.quantity.pack(anchor=tk.W)
        self.height = ttk.Entry(self.frm, justify='left')
        self.height.pack(anchor=tk.W)

    def __str__(self):
        return "shelf/shelves"

    def add_element(self):
        with open("piece.json", "r", encoding='utf-8') as f:
            piece = json.load(f)
            if "elements" not in piece:
                piece["elements"] = []
            if self.quantity.get() == "1" and self.height.get().isnumeric():
                piece["elements"].append({"name": "shelf", "height": self.height.get()})
            else:
                piece["elements"].append({"name": "shelves", "quantity": self.quantity.get()})
        with open("piece.json", "w") as f:
            json.dump(piece, f, indent=4)
        super().add_element()





class BoxesWindow(Window):
    def __init__(self):
        super().__init__()
        self.title('Boxes')
        self.geometry('400x400')

    def __str__(self):
        return "box/boxes"


class EntryDigits(ttk.Entry):
    def __init__(self, parent, *args, **kwargs):
        ttk.Entry.__init__(self, parent, *args, **kwargs)
        vcmd = self.register(self.validate)
        ivcmd = (self.register(self.on_invalid))
        self.config(validate='focusout', validatecommand=vcmd, invalidcommand=ivcmd)

    def validate_numbers(self):
        if not self.get().isnumeric():
            self.delete(0, tk.END)
            messagebox.showwarning("Error", "Please enter a number.")
            return False

    def validate(self):
        print("validate")
        if not self.get().isnumeric():
            print("not good")
            return False
        print("good")
        return True

    def on_invalid(self):
        pass
